"""Talking to the Vero CLI.

Three calls, cheapest first (Vero CLI 2.3.x, integration guide section 3):
  vero version   -> installed, version text                      (free)
  vero config    -> configured provider / model / region         (free)
  vero task --json -t <s> -c <empty dir> [-m <model>] <prompt>   (2 small model calls, ~1 min)
                 -> available when a `completion_result` event arrives; `modelInfo` names the model
                    that actually answered. `api_req_started` holds the full prompt: never kept.
Parsers are pure functions; `run` is the only place that starts a process.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

NO_WINDOW = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW: never flash a console
PROMPT = "Reply with exactly: OK"
DETAIL_MAX = 160
_SECRET = re.compile(r"(?i)(bearer\s+\S+|token[=:]\s*\S+|password[=:]\s*\S+|aws_secret\S*)")


@dataclass(frozen=True)
class Proc:
    started: bool
    code: Optional[int]
    out: str
    err: str
    seconds: float
    timed_out: bool


def clean(text: str) -> str:
    """One short line; anything that looks like a credential is masked."""
    return _SECRET.sub("[hidden]", " ".join(text.split()))[:DETAIL_MAX]


def find_vero(configured: str = "") -> Optional[str]:
    """Configured path, else `vero` on PATH (vero.cmd on Windows), else the npm default folder."""
    for candidate in (configured, "vero"):
        if candidate:
            found = shutil.which(candidate) or (candidate if Path(candidate).is_file() else None)
            if found:
                return found
    appdata = os.environ.get("APPDATA")
    if appdata:
        npm = Path(appdata) / "npm" / "vero.cmd"
        if npm.is_file():
            return str(npm)
    return None


def _kill_tree(proc: subprocess.Popen[bytes]) -> None:
    with contextlib.suppress(OSError):
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, creationflags=NO_WINDOW, check=False
            )
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    with contextlib.suppress(OSError):
        proc.kill()


def run(args: Sequence[str], timeout_s: float, cwd: Optional[str] = None) -> Proc:
    """Start a process without a window, collect output, kill the whole tree on timeout."""
    t0 = time.perf_counter()
    try:
        proc = subprocess.Popen(
            list(args),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            creationflags=NO_WINDOW,
            start_new_session=os.name != "nt",
        )
    except OSError as e:
        return Proc(False, None, "", f"cannot start {Path(args[0]).name}: {e}", 0.0, False)
    stdout, stderr = proc.stdout, proc.stderr
    if stdout is None or stderr is None:
        _kill_tree(proc)
        return Proc(False, None, "", "no output pipes", 0.0, False)
    out: List[bytes] = []
    err: List[bytes] = []
    readers = [
        threading.Thread(target=lambda: out.append(stdout.read()), daemon=True),
        threading.Thread(target=lambda: err.append(stderr.read()), daemon=True),
    ]
    for r in readers:
        r.start()
    timed_out = False
    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_tree(proc)
        proc.wait()
    seconds = time.perf_counter() - t0
    for r in readers:
        r.join(timeout=5)
    stdout.close()
    stderr.close()
    return Proc(
        True,
        proc.returncode,
        b"".join(out).decode("utf-8", "replace"),
        b"".join(err).decode("utf-8", "replace"),
        seconds,
        timed_out,
    )


# ---- pure parsers ---------------------------------------------------------------


def parse_version(text: str) -> str:
    first = (text.strip().splitlines() or [""])[0]
    return clean(first)[:60]


CONFIG_KEYS = {
    "actModeApiModelId": "model",
    "actModeApiProvider": "provider",
    "awsRegion": "region",
    "planModeApiModelId": "plan_model",
}


def parse_config(text: str) -> Dict[str, str]:
    """`vero config` output -> {model, provider, region, plan_model}. Accepts JSON or `key : value` lines."""
    found: Dict[str, str] = {}
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            for key, name in CONFIG_KEYS.items():
                if isinstance(data.get(key), (str, int, float)):
                    found[name] = str(data[key])
            return found
    except json.JSONDecodeError:
        pass
    for line in text.splitlines():
        m = re.match(r"^\s*[\"']?(\w+)[\"']?\s*[:=]\s*[\"']?([^\"',]+)[\"']?,?\s*$", line)
        if m and m.group(1) in CONFIG_KEYS:
            found[CONFIG_KEYS[m.group(1)]] = m.group(2).strip()
    return found


@dataclass(frozen=True)
class TaskStream:
    answer: Optional[str]
    provider: Optional[str]
    model: Optional[str]
    error: Optional[str]
    events: int
    task_id: Optional[str] = None


def parse_task_stream(lines: Iterable[str]) -> TaskStream:
    answer = provider = model = error = task_id = None
    events = 0
    for raw in lines:
        raw = raw.strip()
        if not raw.startswith("{"):
            continue
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(ev, dict):
            continue
        events += 1
        if ev.get("type") == "task_started" and ev.get("taskId") is not None:
            task_id = str(ev["taskId"])
        info = ev.get("modelInfo")
        if isinstance(info, dict):
            provider = info.get("providerId") or provider
            model = info.get("modelId") or model
        if ev.get("partial") is True:
            continue
        if ev.get("say") == "completion_result":
            answer = str(ev.get("text") or "")
        elif ev.get("say") in ("error", "api_req_failed") or ev.get("type") == "error":
            error = clean(str(ev.get("text") or ev.get("message") or "error"))
    return TaskStream(answer, provider, model, error, events, task_id)


def task_args(exe: str, model: str, timeout_s: int, workdir: Path, prompt: str = PROMPT) -> List[str]:
    args = [exe, "task", "--json", "-t", str(timeout_s), "-c", str(workdir)]
    if model:
        args += ["-m", model]
    return [*args, prompt]  # never --yolo: the probe needs no file or shell access
