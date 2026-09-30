"""Command line: vlm <command>. Run `vlm -h` for help."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import shutil
import sys
import time
import webbrowser
from pathlib import Path

from . import __version__, config, scheduler
from .config import ROOT, ConfigError
from .probe import build_command, classify, cli_version, run_cycle, time_command
from .server import WEB, dashboard_payload, serve
from .store import Store


def _setup_logging(data_dir: str, verbose: bool) -> None:
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [logging.FileHandler(Path(data_dir) / "monitor.log", encoding="utf-8")]
    if sys.stdout is not None:  # None under pythonw (Task Scheduler)
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, handlers=handlers,
                        format="%(asctime)s %(levelname)s %(message)s")


def cmd_init(a) -> int:
    target = config.CONFIG_FILE
    if target.exists() and not a.force:
        print(f"{target} already exists (use --force to overwrite)")
        return 0
    cfg = json.loads(config.EXAMPLE_FILE.read_text(encoding="utf-8"))
    if a.demo:
        cfg["cli"]["command"] = [sys.executable, str(ROOT / "scripts" / "fake_vero.py"),
                                 "-p", "{prompt}", "--model", "{model}"]
        cfg["cli"]["version_command"] = [sys.executable, str(ROOT / "scripts" / "fake_vero.py"), "--version"]
        cfg["models"] = [{"id": "fake-mini", "label": "fake-mini"}, {"id": "fake-std", "label": "fake-std"}]
        cfg["schedule"]["interval_minutes"] = 1
    target.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {target}" + ("  (demo mode: fake Vero CLI)" if a.demo else ""))
    print("next: edit it, then run  vlm doctor")
    return 0


def cmd_doctor(a, cfg) -> int:
    cli = cfg["cli"]
    ok = True
    print(f"config         {cfg['_path']}")
    exe = cli["command"][0]
    found = shutil.which(exe)
    print(f"executable     {exe} -> {found or 'NOT FOUND on PATH'}")
    ok &= bool(found)
    print(f"cli version    {cli_version(cfg)}")
    for m in cfg["models"]:
        args = build_command(cli["command"], cfg["prompt"], m["id"], cli["prompt_via"])
        stdin = cfg["prompt"] if cli["prompt_via"] == "stdin" else None
        res = time_command(args, stdin, cli["timeout_s"], cli.get("env"))
        status, err = classify(res, cfg.get("expect", ""))
        ms = f"{res['total_ms']:.0f} ms" if res["total_ms"] is not None else "-"
        print(f"probe {m['label']:<12} {status:<11}{ms:>9}   {err or res['stdout'].strip()[:60]!r}")
        print(f"               command: {' '.join(args)}")
        ok &= status == "ok"
    print("RESULT         " + ("ready" if ok else "fix the items above (see the guide, Troubleshooting)"))
    return 0 if ok else 1


def cmd_probe(a, cfg) -> int:
    store = Store(cfg["data_dir"])
    m = run_cycle(cfg, store, a.trigger)
    if m is None:
        return 0
    if not a.quiet:
        print(json.dumps(m, indent=2))
    return 0 if m["totals"]["failed"] == 0 else 2


def cmd_serve(a, cfg) -> int:
    host = a.host or cfg["server"]["host"]
    port = a.port or cfg["server"]["port"]
    with_sched = cfg["schedule"]["run_in_dashboard"] and not a.no_scheduler
    if a.open:
        webbrowser.open(f"http://{host}:{port}/")
    serve(cfg, Store(cfg["data_dir"]), host, port, with_sched)
    return 0


def cmd_schedule(a, cfg) -> int:
    try:
        if a.action == "install":
            print(scheduler.install(int(a.every or cfg["schedule"]["interval_minutes"])))
            if cfg["schedule"]["run_in_dashboard"]:
                print("tip: set schedule.run_in_dashboard=false so the dashboard does not probe twice")
        elif a.action == "remove":
            print(scheduler.remove())
        else:
            print(scheduler.status())
    except (RuntimeError, OSError) as e:
        print(f"error: {e}")
        return 1
    return 0


def cmd_export(a, cfg) -> int:
    data = Store(cfg["data_dir"]).to_csv(time.time() - a.hours * 3600 if a.hours else 0, a.model)
    out = Path(a.out or f"vero_latency_{dt.date.today():%Y%m%d}.csv")
    out.write_text(data, encoding="utf-8")
    print(f"wrote {out} ({data.count(chr(10)) - 1} rows)")
    return 0


def cmd_report(a, cfg) -> int:
    payload = dashboard_payload(cfg, Store(cfg["data_dir"]), a.hours, a.model)
    html = (WEB / "dashboard.html").read_text(encoding="utf-8")
    blob = json.dumps(payload).replace("</", "<\\/")
    html = html.replace("<!--STATIC_DATA-->", f"<script>window.STATIC_DATA={blob};</script>")
    out = Path(a.out or f"vero_latency_report_{dt.date.today():%Y%m%d}.html")
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} (last {a.hours:g} h, self-contained, can be emailed)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vlm", description="Vero CLI latency monitor (ASPF-1578)")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--config", help="path to monitor.json (default config/monitor.json)")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create config/monitor.json from the example")
    s.add_argument("--demo", action="store_true", help="use the bundled fake Vero CLI")
    s.add_argument("--force", action="store_true")

    sub.add_parser("doctor", help="check the Vero CLI connection with one test probe (nothing stored)")

    s = sub.add_parser("probe", help="run one probe cycle now and store it")
    s.add_argument("--trigger", default="manual", choices=["manual", "task", "schedule", "dashboard"])
    s.add_argument("-q", "--quiet", action="store_true")

    s = sub.add_parser("serve", help="start the dashboard (and the built-in scheduler)")
    s.add_argument("--host")
    s.add_argument("--port", type=int)
    s.add_argument("--no-scheduler", action="store_true")
    s.add_argument("--open", action="store_true", help="open the browser")

    s = sub.add_parser("schedule", help="Windows Task Scheduler / cron trigger")
    s.add_argument("action", choices=["install", "remove", "status"])
    s.add_argument("--every", type=int, help="minutes (default: schedule.interval_minutes)")

    for name, helptext in (("export", "write probes to CSV"), ("report", "write a self-contained HTML report")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("--hours", type=float, default=0 if name == "export" else 168)
        s.add_argument("--model")
        s.add_argument("--out")
    return p


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    if a.cmd == "init":
        return cmd_init(a)
    try:
        cfg = config.load(a.config)
    except ConfigError as e:
        print(f"config error: {e}")
        return 1
    _setup_logging(cfg["data_dir"], a.verbose)
    handler = {"doctor": cmd_doctor, "probe": cmd_probe, "serve": cmd_serve,
               "schedule": cmd_schedule, "export": cmd_export, "report": cmd_report}[a.cmd]
    return handler(a, cfg)
