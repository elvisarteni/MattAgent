"""Your own Vero sessions (Vero CLI in a terminal, Vero in VS Code): latency and the model in use.

How: Vero writes every task's event log to `tasks/<taskId>/ui_messages.json` (integration guide 3.5):
a JSON list of events with `ts` (ms), `type`/`say` and `modelInfo`. Each model request starts with a
`say: "api_req_started"` event; the first later event is the model's first response. The difference
is the request latency, measured with Vero's own clock. Nothing is injected into Vero.

Privacy: only timestamps, event kinds, modelInfo and the token counts inside `api_req_started` are read.
Prompt and answer text are never kept. The files are only read, never changed.
"""

from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .vero import NO_WINDOW, PROMPT

OPEN_WINDOW_S = 10 * 60  # a session with activity in the last 10 minutes counts as open
SCAN_EVERY_S = 15
MAX_TASK_AGE_S = 7 * 86400
MAX_LATENCY_S = 30 * 60  # longer gaps are pauses (waiting for the user), not latency
NOT_RESPONSES = {"api_req_started", "api_req_retried", "api_req_finished"}


@dataclass(frozen=True)
class Request:
    start: float  # epoch seconds
    seconds: float  # time to the model's first response
    tokens_in: Optional[int]
    tokens_out: Optional[int]
    failed: bool


@dataclass
class TaskSummary:
    task_id: str
    source: str  # "CLI" or "VS Code"
    first_prompt_is_probe: bool
    model: Optional[str] = None
    provider: Optional[str] = None
    last_activity: float = 0.0
    waiting_since: Optional[float] = None  # a request is running right now
    requests: List[Request] = field(default_factory=list)


def _int(value: Any) -> Optional[int]:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def parse_ui_messages(events: Sequence[Any], task_id: str, source: str, now: Optional[float] = None) -> TaskSummary:
    """Pure: the event list of one task -> its model and request latencies."""
    evs = sorted((e for e in events if isinstance(e, dict) and isinstance(e.get("ts"), (int, float))), key=lambda e: e["ts"])
    first_text = next((str(e.get("text") or "") for e in evs if e.get("say") == "task"), "")
    summary = TaskSummary(task_id, source, first_prompt_is_probe=first_text.strip() == PROMPT)
    now = time.time() if now is None else now
    for i, ev in enumerate(evs):
        info = ev.get("modelInfo")
        if isinstance(info, dict):
            summary.model = info.get("modelId") or summary.model
            summary.provider = info.get("providerId") or summary.provider
        summary.last_activity = max(summary.last_activity, ev["ts"] / 1000)
        if ev.get("say") != "api_req_started":
            continue
        start = ev["ts"] / 1000
        nxt = next((e for e in evs[i + 1 :] if e.get("say") not in NOT_RESPONSES), None)
        if nxt is None:
            if now - start < MAX_LATENCY_S:
                summary.waiting_since = start
            continue
        seconds = nxt["ts"] / 1000 - start
        if not 0 <= seconds <= MAX_LATENCY_S:
            continue
        tokens: Dict[str, Any] = {}
        try:  # only token counts; the "request" field (full prompt) is dropped immediately
            info_text = json.loads(ev.get("text") or "{}")
            if isinstance(info_text, dict):
                tokens = {k: info_text.get(k) for k in ("tokensIn", "tokensOut")}
        except (TypeError, ValueError):
            pass
        failed = nxt.get("say") in ("api_req_failed", "error") or nxt.get("ask") == "api_req_failed"
        summary.requests.append(
            Request(start, round(seconds, 2), _int(tokens.get("tokensIn")), _int(tokens.get("tokensOut")), failed)
        )
    return summary


def percentile(values: Sequence[float], pct: float) -> Optional[float]:
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * pct / 100
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 1)


# ---- where Vero keeps its task logs -----------------------------------------------


def default_roots() -> List[Tuple[str, str]]:
    """(glob pattern of a `tasks` folder, source label). CLI path measured; VS Code paths follow the
    VS Code extension storage convention and are matched by an extension folder containing 'vero'."""
    home = Path.home()
    roots = [(str(home / ".vero" / "data" / "tasks"), "CLI")]
    code_storage = [
        Path(os.environ.get("APPDATA", home / "AppData" / "Roaming")) / "Code" / "User" / "globalStorage",
        home / ".config" / "Code" / "User" / "globalStorage",
        home / "Library" / "Application Support" / "Code" / "User" / "globalStorage",
    ]
    for base in code_storage:
        roots.append((str(base / "*vero*" / "tasks"), "VS Code"))
        roots.append((str(base / "*Vero*" / "tasks"), "VS Code"))
    return roots


def find_task_files(roots: Iterable[Tuple[str, str]], now: float) -> List[Tuple[Path, str]]:
    seen = set()
    found: List[Tuple[Path, str]] = []
    for pattern, source in roots:
        for tasks_dir in glob.glob(pattern):
            for f in glob.glob(os.path.join(glob.escape(tasks_dir), "*", "ui_messages.json")):
                p = Path(f)
                try:
                    if now - p.stat().st_mtime > MAX_TASK_AGE_S or p in seen:
                        continue
                except OSError:
                    continue
                seen.add(p)
                found.append((p, source))
    return found


# ---- is a Vero CLI open right now? -----------------------------------------------

_TOKEN = re.compile(r'"[^"]*"|\S+')
_VERO_SCRIPT = re.compile(r"(^|[\\/])(@[^\\/]+[\\/])?vero([\\/]|\.js$|$)", re.I)
VERO_EXES = {"vero", "vero.cmd", "vero.exe"}
NODE_EXES = {"node", "node.exe"}
ADMIN_COMMANDS = {"version", "--version", "-v", "config", "history", "h", "auth", "mcp", "token", "update", "dev", "--help", "-h"}


def is_interactive_vero(cmdline: str, ignore: Sequence[str]) -> bool:
    """True for a user's Vero CLI: the program is vero(.cmd/.exe), or node running a script in a `vero`
    package. Not our own checks (ignore list), not admin calls like `vero version`."""
    tokens = [t.strip('"') for t in _TOKEN.findall(cmdline or "")]
    if not tokens:
        return False
    exe = re.split(r"[\\/]", tokens[0])[-1].lower()
    if exe in VERO_EXES:
        args = tokens[1:]
    elif exe in NODE_EXES and len(tokens) > 1 and _VERO_SCRIPT.search(tokens[1]):
        args = tokens[2:]
    else:
        return False
    low = cmdline.lower()
    if any(x and x.lower() in low for x in ignore):
        return False
    return not (args and args[0].lower() in ADMIN_COMMANDS)


def process_command_lines() -> List[str]:
    """Command lines of node / vero processes. Windows: one hidden PowerShell call."""
    try:
        if sys.platform == "win32":
            ps = (
                "Get-CimInstance Win32_Process -Filter \"Name='node.exe' OR Name='vero.exe'\" | ForEach-Object { $_.CommandLine }"
            )
            r = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                capture_output=True,
                text=True,
                timeout=15,
                creationflags=NO_WINDOW,
                check=False,
            )
        else:
            r = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True, timeout=10, check=False)
        return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
    except (OSError, subprocess.SubprocessError):
        return []


# ---- the scanner -------------------------------------------------------------------


class Scanner:
    """Re-reads changed task logs at most every SCAN_EVERY_S seconds (cached by file mtime)."""

    def __init__(
        self,
        roots: Optional[List[Tuple[str, str]]] = None,
        ignore_processes: Sequence[str] = (),
        list_processes: Any = process_command_lines,
    ) -> None:
        self.roots = roots if roots is not None else default_roots()
        self.ignore_processes = list(ignore_processes)
        self.list_processes = list_processes
        self._cache: Dict[Path, Tuple[float, TaskSummary]] = {}
        self._last_scan = 0.0
        self._result: Dict[str, Any] = {}
        self._lock = threading.Lock()

    @property
    def result(self) -> Dict[str, Any]:
        return self._result

    def state(self, own_task_ids: Iterable[str] = (), now: Optional[float] = None, force: bool = False) -> Dict[str, Any]:
        now = time.time() if now is None else now
        with self._lock:
            if not force and self._result and now - self._last_scan < SCAN_EVERY_S:
                return self._result
            self._last_scan = now
            self._result = self._scan(set(own_task_ids), now)
            return self._result

    def _scan(self, own: Set[str], now: float) -> Dict[str, Any]:
        tasks: List[TaskSummary] = []
        live = set()
        for path, source in find_task_files(self.roots, now):
            live.add(path)
            try:
                mtime = path.stat().st_mtime
                cached = self._cache.get(path)
                if cached and cached[0] == mtime:
                    summary = cached[1]
                else:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    summary = parse_ui_messages(data if isinstance(data, list) else [], path.parent.name, source, now)
                    self._cache[path] = (mtime, summary)
            except (OSError, ValueError):
                continue
            if summary.task_id in own or summary.first_prompt_is_probe:
                continue  # our own availability checks are not your sessions
            tasks.append(summary)
        self._cache = {p: v for p, v in self._cache.items() if p in live}
        return summarize(tasks, self._cli_open(), now, [r for r, _ in self.roots])

    def _cli_open(self) -> bool:
        return any(is_interactive_vero(c, self.ignore_processes) for c in self.list_processes())


def summarize(tasks: List[TaskSummary], cli_open: bool, now: float, roots: List[str]) -> Dict[str, Any]:
    recent = sorted(tasks, key=lambda t: t.last_activity, reverse=True)
    active = [t for t in recent if now - t.last_activity < OPEN_WINDOW_S or t.waiting_since]
    current = active[0] if active else None  # an idle open CLI shows Vero's configured model instead
    reqs = sorted(((r, t) for t in tasks for r in t.requests), key=lambda x: x[0].start)

    def window(seconds: float) -> Dict[str, Any]:
        vals = [r.seconds for r, _ in reqs if now - r.start <= seconds and not r.failed]
        return {"n": len(vals), "p50": percentile(vals, 50), "p95": percentile(vals, 95)}

    return {
        "open": bool(active) or cli_open,
        "cli_process": cli_open,
        "current": None
        if current is None
        else {
            "source": current.source,
            "model": current.model,
            "provider": current.provider,
            "last_activity": current.last_activity,
            "waiting_since": current.waiting_since,
        },
        "latency": {"hour": window(3600), "day": window(86400)},
        "recent": [
            {
                "t": r.start,
                "s": r.seconds,
                "failed": r.failed,
                "source": t.source,
                "model": t.model,
                "tokens_in": r.tokens_in,
                "tokens_out": r.tokens_out,
            }
            for r, t in reqs[-40:]
        ],
        "tasks_seen": len(tasks),
        "searched": roots,
    }
