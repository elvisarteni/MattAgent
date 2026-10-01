"""Application service: one monitoring run = lock -> checks -> overall status -> store -> manifest."""

from __future__ import annotations

import contextlib
import datetime as dt
import json
import logging
import os
import platform
import time
from pathlib import Path
from typing import Callable, List, Optional

from . import COMPONENT, __version__
from .checks import run_all
from .checks.vero_cli import hard_limit_s
from .config import Config
from .domain import CheckResult, RunResult, overall_status
from .store import Store, reason_of

log = logging.getLogger("vero_monitor")


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def new_run_id(store: Store, when: dt.datetime) -> str:
    """SCMP naming <YYYYMMDD-HHMM>-<component>, suffix -2, -3 within the same minute."""
    base = f"{when.astimezone(dt.timezone.utc):%Y%m%d-%H%M}-{COMPONENT}"
    run_id, n = base, 2
    while store.run_exists(run_id):
        run_id, n = f"{base}-{n}", n + 1
    return run_id


def stale_after_s(cfg: Config) -> float:
    """A lock older than the longest possible run is left over from a crash."""
    return hard_limit_s(cfg) + cfg.chat.timeout_s + 30 + 120


class RunLock:
    """Cross-process lock file. A Task Scheduler run and a dashboard run never overlap."""

    def __init__(self, data_dir: Path, stale_s: float):
        self.path = Path(data_dir) / "run.lock"
        self.stale_s = stale_s
        self.held = False

    def __enter__(self) -> RunLock:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > self.stale_s:
                        self.path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                return self
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            self.held = True
            return self
        return self

    def __exit__(self, *exc: object) -> None:
        if self.held:
            with contextlib.suppress(FileNotFoundError):
                self.path.unlink()


def in_progress(cfg: Config) -> bool:
    try:
        return time.time() - (cfg.data_dir / "run.lock").stat().st_mtime < stale_after_s(cfg)
    except FileNotFoundError:
        return False


Checker = Callable[[Config], List[CheckResult]]


def run_once(cfg: Config, store: Store, trigger: str, checker: Checker = run_all) -> Optional[RunResult]:
    """Run every enabled check once. None if another run holds the lock."""
    with RunLock(cfg.data_dir, stale_after_s(cfg)) as lock:
        if not lock.held:
            log.info("another run is in progress; skipped")
            return None
        now = dt.datetime.now(dt.timezone.utc)
        run_id = new_run_id(store, now)
        results = checker(cfg)
        run = RunResult(
            run_id=run_id,
            started_at=iso(now),
            epoch=now.timestamp(),
            trigger=trigger,
            checks=tuple(results),
            overall=overall_status(results),
        )
        store.save(run, platform.node(), __version__)
        store.prune(cfg.retention_days)
        write_manifest(cfg, run)
        log.info("%s %s %s", run_id, run.overall.value.upper(), " ".join(f"{r.check.value}={r.status.value}" for r in results))
        return run


def write_manifest(cfg: Config, run: RunResult) -> Path:
    """SCMP run manifest: what was checked, with which CLI/model, and the outcome."""
    task = next((c for c in run.checks if c.check.value == "task"), None)
    manifest = {
        "run_id": run.run_id,
        "component": COMPONENT,
        "tool_version": __version__,
        "trigger": run.trigger,
        "host": platform.node(),
        "started_at": run.started_at,
        "overall": run.overall.value,
        "reason": reason_of(run),
        "model": {
            "provider": task.provider_id if task else None,
            "id": task.model_id if task else None,
            "configured_id": cfg.vero.model,
        },
        "checks": [
            {
                "check": c.check.value,
                "status": c.status.value,
                "duration_ms": None if c.duration_ms is None else round(c.duration_ms, 1),
                "detail": c.detail,
                "version": c.version,
            }
            for c in run.checks
        ],
    }
    d = cfg.data_dir / "runs" / run.started_at[:7]
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{run.run_id}.json"
    p.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return p
