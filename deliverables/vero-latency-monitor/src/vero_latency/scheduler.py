"""Time triggers: an in-process loop (dashboard mode) and the OS scheduler
(Windows Task Scheduler or cron) for fully unattended runs."""
from __future__ import annotations

import logging
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from .config import ROOT
from .probe import NO_WINDOW, run_cycle
from .store import Store

log = logging.getLogger("vero_latency")

TASK_NAME = "VeroLatencyMonitor"
CRON_MARK = "# vero-latency-monitor"


class Loop:
    """Runs a probe cycle every interval, aligned to wall-clock boundaries."""

    def __init__(self, cfg: dict, store: Store):
        self.cfg, self.store = cfg, store
        self.interval = int(cfg["schedule"]["interval_minutes"]) * 60
        self.next_run: float | None = None
        self.running = False
        self._stop = threading.Event()
        self._busy = threading.Lock()

    def _align(self, now: float) -> float:
        return (now // self.interval + 1) * self.interval

    def trigger(self, source: str) -> bool:
        """Start a cycle in the background. False if one is already running."""
        if not self._busy.acquire(blocking=False):
            return False

        def work():
            self.running = True
            try:
                run_cycle(self.cfg, self.store, source)
            except Exception:
                log.exception("probe cycle failed")
            finally:
                self.running = False
                self._busy.release()

        threading.Thread(target=work, daemon=True).start()
        return True

    def start(self) -> None:
        def loop():
            self.next_run = self._align(time.time())
            while not self._stop.wait(max(0.0, self.next_run - time.time())):
                self.trigger("schedule")
                self.next_run = self._align(time.time())

        threading.Thread(target=loop, daemon=True).start()

    def stop(self) -> None:
        self._stop.set()


# OS scheduler -----------------------------------------------------------------

def _python_for_task() -> str:
    exe = Path(sys.executable)
    if os.name == "nt":
        w = exe.with_name("pythonw.exe")  # no console window every run
        if w.exists():
            return str(w)
    return str(exe)


def task_command() -> list[str]:
    return [_python_for_task(), str(ROOT / "vlm.py"), "probe", "--trigger", "task"]


def install(interval_minutes: int) -> str:
    cmd = task_command()
    if os.name == "nt":
        tr = f'"{cmd[0]}" "{cmd[1]}" ' + " ".join(cmd[2:])
        if interval_minutes % 60 == 0:
            sc = ["/SC", "HOURLY", "/MO", str(interval_minutes // 60)]
        else:
            sc = ["/SC", "MINUTE", "/MO", str(interval_minutes)]
        args = ["schtasks", "/Create", "/F", "/TN", TASK_NAME, "/TR", tr] + sc
        r = subprocess.run(args, capture_output=True, text=True, creationflags=NO_WINDOW)
        if r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).strip())
        return f"Windows task '{TASK_NAME}' created: every {interval_minutes} min\n  {tr}"
    line = f"{_cron_expr(interval_minutes)} {' '.join(_sh(c) for c in cmd)} {CRON_MARK}"
    lines = [l for l in _crontab_lines() if CRON_MARK not in l] + [line]
    _write_crontab(lines)
    return f"cron entry installed:\n  {line}"


def remove() -> str:
    if os.name == "nt":
        r = subprocess.run(["schtasks", "/Delete", "/F", "/TN", TASK_NAME],
                           capture_output=True, text=True, creationflags=NO_WINDOW)
        if r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).strip())
        return f"Windows task '{TASK_NAME}' removed"
    _write_crontab([l for l in _crontab_lines() if CRON_MARK not in l])
    return "cron entry removed"


def status() -> str:
    if os.name == "nt":
        r = subprocess.run(["schtasks", "/Query", "/TN", TASK_NAME, "/V", "/FO", "LIST"],
                           capture_output=True, text=True, creationflags=NO_WINDOW)
        if r.returncode != 0:
            return f"Windows task '{TASK_NAME}' not installed"
        keep = ("TaskName", "Next Run Time", "Status", "Last Run Time", "Last Result", "Task To Run", "Repeat: Every")
        return "\n".join(l for l in r.stdout.splitlines() if l.strip().startswith(keep))
    mine = [l for l in _crontab_lines() if CRON_MARK in l]
    return mine[0] if mine else "cron entry not installed"


def _cron_expr(minutes: int) -> str:
    if minutes < 60:
        return f"*/{minutes} * * * *"
    if minutes % 60 == 0 and minutes < 1440:
        return f"0 */{minutes // 60} * * *"
    return "0 0 * * *"


def _sh(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'" if any(c in s for c in " '\"$") else s


def _crontab_lines() -> list[str]:
    r = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else []


def _write_crontab(lines: list[str]) -> None:
    r = subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
