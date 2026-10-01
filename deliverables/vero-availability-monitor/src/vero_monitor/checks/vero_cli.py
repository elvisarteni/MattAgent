"""Vero CLI checks.

cli  : `vero version`          -> installed and starts. Free, a few seconds.
task : `vero task --json ...`  -> end-to-end: the agent reaches the model and completes.

Contract of the --json stream (Vero CLI 2.3.x, see the integration guide section 3.3):
one JSON object per line; the answer is ONLY the `say == "completion_result"` event; `partial: true`
fragments are ignored; `modelInfo` gives the real provider/model; `task_started` gives the taskId.
`api_req_started.text` holds the full upstream prompt and is never kept or logged.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from ..config import Config
from ..domain import Check, CheckResult, Status
from . import process

DETAIL_MAX = 200
_SECRETISH = re.compile(r"(?i)(bearer\s+\S+|token[=:]\s*\S+|aws_secret\S*|password[=:]\s*\S+)")


def clean(text: str) -> str:
    """One short line, with anything that looks like a credential masked."""
    line = " ".join(text.split())
    return _SECRETISH.sub("[masked]", line)[:DETAIL_MAX]


@dataclass(frozen=True)
class TaskStream:
    task_id: Optional[str]
    completion: Optional[str]
    provider_id: Optional[str]
    model_id: Optional[str]
    error: Optional[str]
    events: int


def parse_stream(lines: Iterable[str]) -> TaskStream:
    task_id = completion = provider = model = error = None
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
        say = ev.get("say")
        if say == "completion_result":
            completion = str(ev.get("text") or "")
        elif say in ("error", "api_req_failed") or ev.get("type") == "error":
            error = clean(str(ev.get("text") or ev.get("message") or say))
    return TaskStream(task_id, completion, provider, model, error, events)


def _program(cfg: Config) -> Optional[str]:
    return process.resolve(cfg.vero.command)


def check_cli(cfg: Config) -> CheckResult:
    exe = _program(cfg)
    if not exe:
        return CheckResult(Check.CLI, Status.DOWN, None, f"'{cfg.vero.command}' not found on PATH")
    r = process.run([exe, *cfg.vero.version_args], 30, dict(cfg.vero.env))
    if r.timed_out:
        return CheckResult(Check.CLI, Status.DOWN, r.duration_ms, "version command timed out")
    if r.exit_code != 0:
        return CheckResult(Check.CLI, Status.DOWN, r.duration_ms, f"exit {r.exit_code}: {clean(r.stderr or r.stdout)}")
    first = (r.stdout.strip().splitlines() or [""])[0]
    return CheckResult(Check.CLI, Status.UP, r.duration_ms, "", version=clean(first)[:80])


def task_command(cfg: Config, exe: str, workdir: Path) -> list[str]:
    fill = {
        "{model}": cfg.vero.model,
        "{timeout}": str(int(cfg.vero.task_timeout_s)),
        "{workdir}": str(workdir),
        "{prompt}": cfg.vero.prompt,
    }
    args = [exe]
    for a in cfg.vero.task_args:
        for k, v in fill.items():
            a = a.replace(k, v)
        args.append(a)
    return args


def hard_limit_s(cfg: Config) -> float:
    """Our own kill deadline: Vero's -t plus a grace period (min(30 s, -t)) in case the CLI ignores -t."""
    return cfg.vero.task_timeout_s + min(30.0, cfg.vero.task_timeout_s)


def check_task(cfg: Config) -> CheckResult:
    exe = _program(cfg)
    if not exe:
        return CheckResult(Check.TASK, Status.DOWN, None, f"'{cfg.vero.command}' not found on PATH")
    workdir = cfg.data_dir / "sandbox"  # empty folder: the agent has nothing to read or change
    workdir.mkdir(parents=True, exist_ok=True)
    limit = hard_limit_s(cfg)
    r = process.run(task_command(cfg, exe, workdir), limit, dict(cfg.vero.env), str(workdir))
    if not r.started:
        return CheckResult(Check.TASK, Status.DOWN, None, clean(r.stderr))
    s = parse_stream(r.stdout.splitlines())

    def result(status: Status, detail: str) -> CheckResult:
        return CheckResult(Check.TASK, status, r.duration_ms, clean(detail), provider_id=s.provider_id, model_id=s.model_id)

    if r.timed_out:
        return result(Status.DOWN, f"no completion within {limit:g} s")
    if s.completion is None:
        why = s.error or (f"exit {r.exit_code}: {r.stderr}" if r.exit_code else "")
        why = why or ("no JSON events: is --json in vero.task_args?" if s.events == 0 else "no completion_result")
        return result(Status.DOWN, why)
    notes = []
    if cfg.vero.expect and cfg.vero.expect.lower() not in s.completion.lower():
        notes.append(f"answered, but not with {cfg.vero.expect!r} ({len(s.completion)} chars)")
    if r.duration_ms > cfg.task_slow_s * 1000:
        notes.append(f"slow: {r.duration_ms / 1000:.0f} s > {cfg.task_slow_s:g} s")
    return result(Status.DEGRADED if notes else Status.UP, "; ".join(notes))
