"""The monitor: runs a check on a timer or on demand, keeps the latest result and a short history."""

from __future__ import annotations

import json
import logging
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from . import sessions, vero
from .settings import Settings, load, save

log = logging.getLogger("vero_status")
HISTORY_MAX = 500
Runner = Callable[[List[str], float, Optional[str]], vero.Proc]


def perform_check(settings: Settings, workdir: Path, run: Runner = vero.run, now: Optional[float] = None) -> Dict[str, Any]:
    """One availability check. Returns a JSON-ready record; never raises for Vero problems."""
    rec: Dict[str, Any] = {
        "time": time.time() if now is None else now,
        "available": False,
        "reason": "",
        "seconds": None,
        "asked_model": None,
        "provider": None,
        "vero_version": None,
        "configured": {},
    }
    exe = vero.find_vero(settings.vero_path)
    if not exe:
        rec["reason"] = "Vero CLI not found on this computer (set its path in Settings)"
        return rec
    ver = run([exe, "version"], 30, None)
    if not ver.started or ver.timed_out or ver.code != 0:
        rec["reason"] = "Vero CLI does not start: " + vero.clean(ver.err or ver.out or "no output")
        return rec
    rec["vero_version"] = vero.parse_version(ver.out)
    cfg = run([exe, "config"], 30, None)
    if cfg.started and cfg.code == 0:
        rec["configured"] = vero.parse_config(cfg.out)
    workdir.mkdir(parents=True, exist_ok=True)  # empty folder: the agent has nothing to read or change
    limit = settings.timeout_seconds
    task = run(vero.task_args(exe, settings.check_model, limit, workdir), limit + 30, str(workdir))
    stream = vero.parse_task_stream(task.out.splitlines())
    rec["asked_model"], rec["provider"] = stream.model, stream.provider  # model Vero used for the check
    rec["task_id"] = stream.task_id  # lets the session tracker ignore our own test tasks
    if task.timed_out:
        rec["reason"] = f"no answer within {limit + 30} s"
    elif stream.answer is not None:
        rec["available"] = True
        rec["seconds"] = round(task.seconds, 1)  # only a real answer has a response time
        if "ok" not in stream.answer.lower():
            rec["reason"] = "answered, but not with OK (a guardrail or the model replied differently)"
    elif stream.error:
        rec["reason"] = stream.error
    elif task.code:
        msg = vero.clean(task.err or task.out or "no output")
        msg = msg[6:].lstrip() if msg.lower().startswith("error:") else msg
        rec["reason"] = f"Vero reported an error (exit code {task.code}): {msg}"
    elif stream.events == 0:
        rec["reason"] = "Vero returned no JSON events (is this Vero CLI 2.3 or newer?)"
    else:
        rec["reason"] = "Vero finished without an answer"
    return rec


class Monitor:
    def __init__(self, data_dir: Path, run: Runner = vero.run, scanner: Optional[sessions.Scanner] = None):
        self.data_dir = data_dir
        self.run = run
        self.settings_path = data_dir / "settings.json"
        self.history_path = data_dir / "history.json"
        self.settings = load(self.settings_path)
        self.history: List[Dict[str, Any]] = self._load_history()
        self.checking = False
        self.next_check: Optional[float] = None
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self.scanner = scanner or sessions.Scanner(ignore_processes=[str(data_dir / "sandbox"), "vero_status", "vero-status"])

    # history ---------------------------------------------------------------
    def _load_history(self) -> List[Dict[str, Any]]:
        try:
            data = json.loads(self.history_path.read_text(encoding="utf-8"))
            return [r for r in data if isinstance(r, dict) and "time" in r][-HISTORY_MAX:]
        except (OSError, ValueError):
            return []

    def _save_history(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        tmp = self.history_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.history[-HISTORY_MAX:]), encoding="utf-8")
        tmp.replace(self.history_path)

    # checks ----------------------------------------------------------------
    def check_now(self, trigger: str = "manual") -> bool:
        """Start a check in the background. False if one is already running."""
        with self._lock:
            if self.checking:
                return False
            self.checking = True
        threading.Thread(target=self._check, args=(trigger,), daemon=True).start()
        return True

    def _check(self, trigger: str) -> None:
        try:
            rec = perform_check(self.settings, self.data_dir / "sandbox", self.run)
        except Exception as e:  # a bug must never kill the program
            log.exception("check failed")
            rec = {
                "time": time.time(),
                "available": False,
                "reason": f"monitor error: {type(e).__name__}",
                "seconds": None,
                "asked_model": None,
                "provider": None,
                "vero_version": None,
                "configured": {},
            }
        rec["trigger"] = trigger
        with self._lock:
            self.history.append(rec)
            self.history = self.history[-HISTORY_MAX:]
            self._save_history()
            self.checking = False
        log.info("check: %s %s", "AVAILABLE" if rec["available"] else "NOT AVAILABLE", rec["reason"])
        self._plan_next()

    def _plan_next(self) -> None:
        m = self.settings.interval_minutes
        self.next_check = time.time() + m * 60 if m else None
        self._wake.set()

    def start(self, check_at_start: bool = True) -> None:
        def loop() -> None:
            while not self._stop.is_set():
                self._wake.clear()
                due = self.next_check
                wait = None if due is None else max(0.0, due - time.time())
                if self._wake.wait(wait) or self._stop.is_set():
                    continue  # plan changed: re-evaluate
                if due is not None and time.time() >= due:
                    self.next_check = None
                    if not self.check_now("auto"):
                        self._plan_next()

        threading.Thread(target=loop, daemon=True).start()
        threading.Thread(target=self._scan_loop, daemon=True).start()
        if check_at_start:
            self.check_now("start")
        else:
            self._plan_next()

    def own_task_ids(self) -> List[str]:
        with self._lock:
            return [str(r["task_id"]) for r in self.history if r.get("task_id")]

    def scan_sessions(self) -> Dict[str, Any]:
        """Your own Vero sessions; never raises (a bad file must not break the dashboard)."""
        try:
            return self.scanner.state(self.own_task_ids(), force=True)
        except Exception:
            log.exception("session scan failed")
            return {}

    def _scan_loop(self) -> None:
        while not self._stop.is_set():
            if self.settings.track_sessions:
                self.scan_sessions()
            self._stop.wait(sessions.SCAN_EVERY_S)

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()

    # settings ----------------------------------------------------------------
    def update_settings(self, changes: Dict[str, Any]) -> Settings:
        new = self.settings.merged(changes)
        save(self.settings_path, new)
        self.settings = new
        if not self.checking:
            self._plan_next()
        return new

    # view ----------------------------------------------------------------------
    def state(self) -> Dict[str, Any]:
        with self._lock:
            hist = list(self.history)
        day = [r for r in hist if r["time"] >= time.time() - 86400]
        last = hist[-1] if hist else None
        last_ok = next((r for r in reversed(hist) if r.get("available")), None)
        since = None
        if last:
            since = last["time"]
            for r in reversed(hist):
                if bool(r.get("available")) != bool(last.get("available")):
                    break
                since = r["time"]
        return {
            "checking": self.checking,
            "next_check": self.next_check,
            "last": last,
            "since": since,
            "configured": (last or {}).get("configured") or (last_ok or {}).get("configured") or {},
            "availability_24h": round(sum(1 for r in day if r.get("available")) / len(day) * 100, 1) if day else None,
            "checks_24h": len(day),
            "history": hist[-48:],
            "settings": {
                "vero_path": self.settings.vero_path,
                "vero_found": vero.find_vero(self.settings.vero_path),
                "check_model": self.settings.check_model,
                "interval_minutes": self.settings.interval_minutes,
                "timeout_seconds": self.settings.timeout_seconds,
                "track_sessions": self.settings.track_sessions,
            },
            "sessions": self.scanner.result if self.settings.track_sessions else None,
        }
