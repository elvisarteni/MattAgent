"""Command line: python vam.py <command>. Run with -h for help."""

from __future__ import annotations

import argparse
import csv
import logging
import logging.handlers
import os
import shutil
import sys
import time
import webbrowser
from pathlib import Path
from typing import Callable, Dict, List, Optional

from . import __version__, config, scheduler
from .checks import run_all
from .checks.vero_cli import task_command
from .config import ROOT, Config, ConfigError
from .domain import Status, overall_status
from .report import static_html
from .runner import in_progress, run_once
from .server import already_running, serve
from .store import CSV_HEADER, Store

log = logging.getLogger("vero_monitor")
FAKE = ROOT / "scripts" / "fake_vero.py"
ICON = {"up": "UP  ", "degraded": "WARN", "down": "DOWN", "unknown": "  ? "}


def setup_logging(data_dir: Path, verbose: bool) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    handlers: List[logging.Handler] = [
        logging.handlers.RotatingFileHandler(data_dir / "monitor.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    ]
    if sys.stdout is not None:  # None under pythonw (Task Scheduler)
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        handlers=handlers,
        format="%(asctime)s %(levelname)s %(message)s",
        force=True,
    )


def ask(question: str, default: str) -> str:
    try:
        answer = input(f"{question} [{default}]: ").strip()
    except EOFError:
        answer = ""
    return answer or default


def yes(question: str, default: bool) -> bool:
    return ask(question + " (y/n)", "y" if default else "n").lower().startswith("y")


# commands without a loaded config -------------------------------------------------


def cmd_init(a: argparse.Namespace) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    if target.exists() and not a.force:
        print(f"{target} already exists (--force to overwrite, or: vam configure)")
        return 0
    raw = config.read_json(config.EXAMPLE_FILE)
    if a.demo:
        # the fake CLI is a Python script: run it with this Python, script path as first argument
        raw["vero"]["command"] = sys.executable
        raw["vero"]["version_args"] = [str(FAKE)] + raw["vero"]["version_args"]
        raw["vero"]["task_args"] = [str(FAKE)] + raw["vero"]["task_args"]
        raw["schedule"]["interval_minutes"] = 2
        raw["vero"]["task_timeout_s"] = 30
        raw["thresholds_s"]["task_slow"] = 8
        raw["data_dir"] = "data-demo"  # never mixed with real measurements
    config.write_json(target, raw)
    print(f"wrote {target}" + ("  (demo: fake Vero CLI, data in data-demo/)" if a.demo else ""))
    return 0


def cmd_configure(a: argparse.Namespace) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    raw = config.read_json(config.EXAMPLE_FILE)
    if target.exists():
        try:
            cur = config.read_json(target)
            if not str(cur.get("data_dir", "")).startswith("data-demo"):
                raw = config.merge(raw, cur)
        except ConfigError as e:
            print(f"current config is broken, starting from the defaults ({e})")
    raw = config.merge(config.DEFAULTS, raw)
    v = raw["vero"]
    print("\nVero availability monitor: configuration. Enter keeps the value in [brackets].\n")
    while True:
        v["command"] = ask("1. Vero CLI program (name or full path; `where vero` shows it)", v["command"]).strip('"')
        found = shutil.which(v["command"])
        if found:
            print(f"   found: {found}")
            break
        print(f"   '{v['command']}' was not found on PATH.")
        if yes("   Keep it anyway", False):
            break
    v["model"] = ask("2. Model id to pin (-m), cheapest first", v["model"])
    raw["checks"]["task"] = yes("3. End-to-end task check (~1 min, 2 small model calls per run)", raw["checks"]["task"])
    raw["checks"]["chat"] = yes("4. Also check Vero Chat (MCP handshake, free; needs a token variable)", raw["checks"]["chat"])
    if raw["checks"]["chat"]:
        raw["chat"]["token_env"] = ask(
            "   Name of the environment variable holding the Vero Chat token", raw["chat"]["token_env"]
        )
        if not os.environ.get(raw["chat"]["token_env"]):
            print(f"   note: {raw['chat']['token_env']} is not set in this session (see guide, Vero Chat token)")
    try:
        raw["schedule"]["interval_minutes"] = int(ask("5. Check every N minutes", str(raw["schedule"]["interval_minutes"])))
        v["task_timeout_s"] = float(ask("6. Task timeout, seconds", f"{float(v['task_timeout_s']):g}"))
        raw["thresholds_s"]["task_slow"] = float(
            ask("7. Task counts as slow (degraded) above, seconds", f"{float(raw['thresholds_s']['task_slow']):g}")
        )
        config.build(raw, target)
    except (ConfigError, ValueError) as e:
        print(f"\nnot saved: {e}")
        return 1
    config.write_json(target, raw)
    print(f"\nsaved {target}")
    return 0


# commands with a config ----------------------------------------------------------


def cmd_doctor(a: argparse.Namespace, cfg: Config) -> int:
    print(f"config    {cfg.path}\ndata      {cfg.data_dir}")
    print(f"program   {cfg.vero.command} -> {shutil.which(cfg.vero.command) or 'NOT FOUND'}")
    if cfg.check_task:
        exe = shutil.which(cfg.vero.command) or cfg.vero.command
        cmd = task_command(cfg, exe, cfg.data_dir / "sandbox")
        print("task cmd  " + " ".join(f'"{a}"' if " " in a else a for a in cmd))
    print("running the enabled checks once (nothing is stored)...")
    results = run_all(cfg)
    for r in results:
        ms = f"{r.duration_ms / 1000:6.1f} s" if r.duration_ms is not None else "      - "
        extra = " ".join(x for x in (r.version or "", r.model_id or "", r.detail) if x)
        print(f"  {ICON[r.status.value]}  {r.check.value:<5} {ms}  {extra}")
    overall = overall_status(results)
    print(
        f"RESULT    {overall.value.upper()}"
        + ("  -> ready" if overall is not Status.DOWN else "  -> fix the items above (guide: Troubleshooting)")
    )
    return 0 if overall is not Status.DOWN else 1


def cmd_check(a: argparse.Namespace, cfg: Config) -> int:
    run = run_once(cfg, Store(cfg.data_dir), a.trigger)
    if run is None:
        print("another run is in progress; skipped")
        return 0
    if not a.quiet:
        for r in run.checks:
            print(f"  {ICON[r.status.value]}  {r.check.value:<5} {r.detail}")
        print(f"{run.run_id}: {run.overall.value.upper()}")
    if a.trigger == "task":
        return 0  # a DOWN result is data, not a task failure (Task Scheduler 'Last Result' stays 0)
    return 0 if run.overall is not Status.DOWN else 2


def cmd_serve(a: argparse.Namespace, cfg: Config) -> int:
    if a.port:
        cfg = config.build({**config.read_json(cfg.path), "server": {"host": cfg.host, "port": a.port}}, cfg.path)
    return serve(cfg, Store(cfg.data_dir), cfg.run_in_dashboard and not a.no_scheduler, a.open)


def _set_run_in_dashboard(cfg: Config, value: bool) -> None:
    raw = config.read_json(cfg.path)
    raw.setdefault("schedule", {})["run_in_dashboard"] = value
    config.write_json(cfg.path, raw)


def cmd_install(a: argparse.Namespace, cfg: Config) -> int:
    every = int(a.every or cfg.interval_minutes)
    if not 1 <= every <= 1440:
        print("--every must be between 1 and 1440")
        return 1
    url = f"http://127.0.0.1:{cfg.port}/"
    for line in scheduler.install(every, url, dashboard=not a.no_dashboard):
        print(line)
    _set_run_in_dashboard(cfg, False)
    print(f"config: schedule.run_in_dashboard = false\nopen the dashboard: {url}")
    return 0


def cmd_uninstall(a: argparse.Namespace, cfg: Config) -> int:
    for line in scheduler.remove():
        print(line)
    _set_run_in_dashboard(cfg, True)
    print(f"config: schedule.run_in_dashboard = true. Data kept in {cfg.data_dir}")
    return 0


def cmd_status(a: argparse.Namespace, cfg: Config) -> int:
    store = Store(cfg.data_dir)
    last = store.runs(limit=1)
    print(f"version   {__version__}\nconfig    {cfg.path}\ndata      {cfg.data_dir} ({store.count()} runs)")
    if last:
        r = last[0]
        print(f"last run  {r['run_id']}  {r['overall'].upper()}  {r['reason'] or ''}")
    else:
        print("last run  none yet")
    print(f"running   {'yes' if in_progress(cfg) else 'no'}")
    up = already_running(cfg.port)
    print(f"dashboard {f'up at http://127.0.0.1:{cfg.port}/' if up else 'not running'}\n")
    print(scheduler.status())
    return 0


def cmd_open(a: argparse.Namespace, cfg: Config) -> int:
    url = f"http://127.0.0.1:{cfg.port}/"
    deadline = time.time() + a.wait
    while not already_running(cfg.port):
        if time.time() > deadline:
            print(f"dashboard not running at {url}: use start_dashboard.bat, see data/monitor.log")
            return 1
        time.sleep(1)
    webbrowser.open(url)
    print(f"opened {url}")
    return 0


def cmd_export(a: argparse.Namespace, cfg: Config) -> int:
    out = Path(a.out or "vero_availability.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = Store(cfg.data_dir).csv_rows(time.time() - a.hours * 3600 if a.hours else 0)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CSV_HEADER)
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)")
    return 0


def cmd_report(a: argparse.Namespace, cfg: Config) -> int:
    out = Path(a.out or "vero_status_report.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(static_html(cfg, Store(cfg.data_dir), a.hours), encoding="utf-8")
    print(f"wrote {out} (last {a.hours} h, self-contained)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vam", description="Vero availability monitor (ASPF-1578)")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--config", help="config file (default config/monitor.json, or env VAM_CONFIG)")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", metavar="command")
    sub.required = True
    s = sub.add_parser("init", help="create config/monitor.json from the example")
    s.add_argument("--demo", action="store_true", help="bundled fake Vero CLI, data in data-demo/")
    s.add_argument("--force", action="store_true")
    sub.add_parser("configure", help="guided configuration")
    sub.add_parser("doctor", help="run the checks once without storing, and explain the result")
    s = sub.add_parser("check", help="run the checks now and store the result")
    s.add_argument("--trigger", default="manual", choices=["manual", "task", "schedule", "dashboard"])
    s.add_argument("-q", "--quiet", action="store_true")
    s = sub.add_parser("serve", help="status dashboard (with the built-in timer unless installed)")
    s.add_argument("--port", type=int)
    s.add_argument("--no-scheduler", action="store_true")
    s.add_argument("--open", action="store_true")
    s = sub.add_parser("install", help="scheduled check + dashboard at logon + desktop shortcut")
    s.add_argument("--every", type=int)
    s.add_argument("--no-dashboard", action="store_true")
    sub.add_parser("uninstall", help="remove the tasks and the shortcut (data is kept)")
    sub.add_parser("status", help="configuration, last run, dashboard and task state")
    s = sub.add_parser("open", help="open the running dashboard")
    s.add_argument("--wait", type=float, default=20)
    s = sub.add_parser("export", help="CSV of runs and checks")
    s.add_argument("--hours", type=float, default=0)
    s.add_argument("--out")
    s = sub.add_parser("report", help="self-contained HTML snapshot")
    s.add_argument("--hours", type=int, default=168, choices=[1, 6, 24, 168, 720])
    s.add_argument("--out")
    return p


HANDLERS: Dict[str, Callable[[argparse.Namespace, Config], int]] = {
    "doctor": cmd_doctor,
    "check": cmd_check,
    "serve": cmd_serve,
    "install": cmd_install,
    "uninstall": cmd_uninstall,
    "status": cmd_status,
    "open": cmd_open,
    "export": cmd_export,
    "report": cmd_report,
}


def main(argv: Optional[List[str]] = None) -> int:
    a = build_parser().parse_args(argv)
    try:
        if a.cmd == "init":
            return cmd_init(a)
        if a.cmd == "configure":
            return cmd_configure(a)
        cfg = config.load(a.config)
    except ConfigError as e:
        print(f"config error: {e}")
        return 1
    setup_logging(cfg.data_dir, a.verbose)
    try:
        return HANDLERS[a.cmd](a, cfg)
    except KeyboardInterrupt:
        return 130
    except (RuntimeError, OSError) as e:
        log.error("%s failed: %s", a.cmd, e)
        return 1
    except Exception:
        log.exception("%s crashed", a.cmd)  # visible in data/monitor.log even under pythonw
        return 1
