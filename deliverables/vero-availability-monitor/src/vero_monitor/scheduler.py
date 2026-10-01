"""Time triggers.

- Loop: in-process scheduler used while the dashboard runs in "dashboard" mode.
- install()/remove()/status(): the OS scheduler for unattended use.
  Windows: two Task Scheduler tasks, registered from XML so laptop-safe settings apply
  (runs on battery, catches up after sleep, never two at once):
    VeroAvailabilityCheck     every N minutes: pythonw vam.py check --trigger task
    VeroAvailabilityDashboard at logon:        pythonw vam.py serve --no-scheduler (hidden, background)
  Linux/macOS: two crontab lines (check every N minutes, dashboard @reboot).
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from xml.sax.saxutils import escape

from .checks.process import NO_WINDOW
from .config import ROOT, Config
from .runner import run_once
from .store import Store

log = logging.getLogger("vero_monitor")

PROBE_TASK = "VeroAvailabilityCheck"
DASH_TASK = "VeroAvailabilityDashboard"
CRON_MARK = "# vero-availability-monitor"
SHORTCUT = "Vero Status.url"


def next_aligned(interval_s: int, now: float | None = None) -> float:
    """Next wall-clock boundary (:00, :15, ...). Task Scheduler and the Loop use the same grid."""
    now = time.time() if now is None else now
    return (now // interval_s + 1) * interval_s


class Loop:
    """Runs the checks every interval while the dashboard is open."""

    def __init__(self, cfg: Config, store: Store):
        self.cfg, self.store = cfg, store
        self.interval = cfg.interval_minutes * 60
        self.active = False
        self.next_run: float | None = None
        self.running = False
        self._stop = threading.Event()
        self._busy = threading.Lock()

    def expected_next(self) -> float:
        """Next run time; in external mode the OS scheduler uses the same aligned grid."""
        return self.next_run if self.active and self.next_run else next_aligned(self.interval)

    def trigger(self, source: str) -> bool:
        """Start a cycle in the background. False if one is already running here."""
        if not self._busy.acquire(blocking=False):
            return False

        def work() -> None:
            self.running = True
            try:
                run_once(self.cfg, self.store, source)
            except Exception:
                log.exception("run failed")
            finally:
                self.running = False
                self._busy.release()

        threading.Thread(target=work, daemon=True).start()
        return True

    def start(self) -> None:
        self.active = True

        def loop() -> None:
            self.next_run = next_aligned(self.interval)
            while not self._stop.wait(max(0.0, self.next_run - time.time())):
                self.trigger("schedule")
                self.next_run = next_aligned(self.interval)

        threading.Thread(target=loop, daemon=True).start()

    def stop(self) -> None:
        self._stop.set()


# commands the OS scheduler runs ------------------------------------------------


def _python(background: bool) -> str:
    exe = Path(sys.executable)
    if os.name == "nt" and background:
        w = exe.with_name("pythonw.exe")  # no console window
        if w.exists():
            return str(w)
    return str(exe)


def probe_command() -> list[str]:
    return [_python(True), str(ROOT / "vam.py"), "check", "--trigger", "task", "--quiet"]


def dashboard_command() -> list[str]:
    return [_python(True), str(ROOT / "vam.py"), "serve", "--no-scheduler"]


# Windows ------------------------------------------------------------------------


def _win_user() -> str:
    user = os.environ.get("USERNAME", "")
    dom = os.environ.get("USERDOMAIN", "")
    return f"{dom}\\{user}" if dom and user else user


def _args(cmd: list[str]) -> str:
    return " ".join(f'"{a}"' if (" " in a or a.endswith(".py")) else a for a in cmd)


def _task_xml(description: str, trigger_xml: str, cmd: list[str], time_limit: str) -> str:
    user = escape(_win_user())
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>{escape(description)}</Description></RegistrationInfo>
  <Triggers>{trigger_xml}</Triggers>
  <Principals><Principal id="Author"><UserId>{user}</UserId><LogonType>InteractiveToken</LogonType>
    <RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <ExecutionTimeLimit>{time_limit}</ExecutionTimeLimit>
    <RestartOnFailure><Interval>PT1M</Interval><Count>3</Count></RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{escape(cmd[0])}</Command>
      <Arguments>{escape(_args(cmd[1:]))}</Arguments>
      <WorkingDirectory>{escape(str(ROOT))}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def probe_task_xml(interval_minutes: int) -> str:
    start = dt.datetime.fromtimestamp(next_aligned(interval_minutes * 60)).strftime("%Y-%m-%dT%H:%M:%S")
    trig = (
        f"<TimeTrigger><Repetition><Interval>PT{interval_minutes}M</Interval>"
        f"<StopAtDurationEnd>false</StopAtDurationEnd></Repetition>"
        f"<StartBoundary>{start}</StartBoundary><Enabled>true</Enabled></TimeTrigger>"
    )
    return _task_xml("Vero availability check (ASPF-1578)", trig, probe_command(), "PT1H")


def dashboard_task_xml() -> str:
    trig = f"<LogonTrigger><Enabled>true</Enabled><UserId>{escape(_win_user())}</UserId></LogonTrigger>"
    return _task_xml("Vero status dashboard, http://127.0.0.1 (ASPF-1578)", trig, dashboard_command(), "PT0S")


def _schtasks(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    r = subprocess.run(["schtasks", *args], capture_output=True, text=True, creationflags=NO_WINDOW)
    if check and r.returncode != 0:
        raise RuntimeError(f"schtasks {args[0]} failed: {(r.stderr or r.stdout).strip()}")
    return r


def _register(name: str, xml: str) -> None:
    fd, path = tempfile.mkstemp(suffix=".xml")
    os.close(fd)
    try:
        Path(path).write_text(xml, encoding="utf-16")
        _schtasks("/Create", "/F", "/TN", name, "/XML", path)
    finally:
        os.unlink(path)


def _desktop() -> Path:
    """The real Desktop folder (it may be redirected to OneDrive on Windows)."""
    if sys.platform == "win32":
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            ) as key:
                value = winreg.QueryValueEx(key, "Desktop")[0]
            return Path(os.path.expandvars(str(value)))
        except OSError:
            pass
    return Path.home() / "Desktop"


def _shortcut(url: str) -> Path | None:
    d = _desktop()
    if not d.is_dir():
        return None
    p = d / SHORTCUT
    p.write_text(f"[InternetShortcut]\nURL={url}\n", encoding="utf-8")
    return p


# public -----------------------------------------------------------------------


def install(interval_minutes: int, url: str, dashboard: bool = True) -> list[str]:
    out = []
    if os.name == "nt":
        _register(PROBE_TASK, probe_task_xml(interval_minutes))
        out.append(f"task '{PROBE_TASK}': check every {interval_minutes} min (also on battery, catches up after sleep)")
        if dashboard:
            _register(DASH_TASK, dashboard_task_xml())
            _schtasks("/Run", "/TN", DASH_TASK, check=False)
            out.append(f"task '{DASH_TASK}': dashboard starts hidden at every logon (started now)")
    else:
        lines = [ln for ln in _crontab_lines() if CRON_MARK not in ln]
        lines.append(f"{_cron_expr(interval_minutes)} {' '.join(_sh(c) for c in probe_command())} {CRON_MARK}")
        if dashboard:
            lines.append(f"@reboot {' '.join(_sh(c) for c in dashboard_command())} >/dev/null 2>&1 {CRON_MARK}")
            subprocess.Popen(dashboard_command(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        _write_crontab(lines)
        out.append(f"cron: check every {interval_minutes} min" + (", dashboard @reboot (started now)" if dashboard else ""))
    if dashboard:
        sc = _shortcut(url)
        out.append(f"desktop shortcut: {sc}" if sc else "no desktop folder found; open " + url)
    return out


def remove() -> list[str]:
    out = []
    if os.name == "nt":
        _schtasks("/End", "/TN", DASH_TASK, check=False)
        for name in (PROBE_TASK, DASH_TASK):
            r = _schtasks("/Delete", "/F", "/TN", name, check=False)
            out.append(f"task '{name}': " + ("removed" if r.returncode == 0 else "not installed"))
    else:
        _write_crontab([ln for ln in _crontab_lines() if CRON_MARK not in ln])
        out.append("cron entries removed (a running dashboard stops at the next reboot or with Ctrl+C)")
    sc = _desktop() / SHORTCUT
    if sc.exists():
        sc.unlink()
        out.append("desktop shortcut removed")
    return out


def status() -> str:
    if os.name == "nt":
        parts = []
        for name in (PROBE_TASK, DASH_TASK):
            r = _schtasks("/Query", "/TN", name, "/FO", "LIST", check=False)
            parts.append(r.stdout.strip() if r.returncode == 0 else f"{name}: not installed")
        return "\n\n".join(parts)
    try:
        mine = [ln for ln in _crontab_lines() if CRON_MARK in ln]
    except RuntimeError as e:
        return f"OS scheduler: {e}"
    return "\n".join(mine) if mine else "cron entries not installed"


def _cron_expr(minutes: int) -> str:
    if minutes < 60:
        return f"*/{minutes} * * * *"
    if minutes % 60 == 0 and minutes < 1440:
        return f"0 */{minutes // 60} * * *"
    return "0 0 * * *"


def _sh(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'" if any(c in s for c in " '\"$") else s


def _crontab_lines() -> list[str]:
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    except FileNotFoundError:
        raise RuntimeError("crontab is not installed on this machine") from None
    return r.stdout.splitlines() if r.returncode == 0 else []


def _write_crontab(lines: list[str]) -> None:
    r = subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
