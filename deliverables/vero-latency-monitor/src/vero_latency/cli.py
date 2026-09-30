"""Command line: python vlm.py <command>. Run with -h for help."""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import logging.handlers
import os
import shlex
import shutil
import sys
import time
from pathlib import Path

from . import __version__, config, scheduler
from .config import ROOT, ConfigError
from .probe import build_command, classify, cli_version, run_cycle, run_in_progress, time_command
from .server import already_running, serve, static_report
from .store import Store

log = logging.getLogger("vero_latency")
FAKE = ROOT / "scripts" / "fake_vero.py"


def _setup_logging(data_dir: str, verbose: bool) -> None:
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [logging.handlers.RotatingFileHandler(
        Path(data_dir) / "monitor.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")]
    if sys.stdout is not None:  # None under pythonw (Task Scheduler)
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, handlers=handlers,
                        format="%(asctime)s %(levelname)s %(message)s", force=True)


def _ask(question: str, default: str) -> str:
    try:
        answer = input(f"{question} [{default}]: ").strip()
    except EOFError:
        answer = ""
    return answer or default


def _split(line: str) -> list[str]:
    parts = shlex.split(line, posix=os.name != "nt")
    return [p[1:-1] if len(p) >= 2 and p[0] == p[-1] == '"' else p for p in parts]


def _join(args: list[str]) -> str:
    return " ".join(f'"{a}"' if " " in a else a for a in args)


# commands ---------------------------------------------------------------------

def cmd_init(a) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    if target.exists() and not a.force:
        print(f"{target} already exists (use --force to overwrite, or run: vlm configure)")
        return 0
    cfg = config.read_json(config.EXAMPLE_FILE)
    if a.demo:
        cfg["cli"]["command"] = [sys.executable, str(FAKE), "-p", "{prompt}", "--model", "{model}"]
        cfg["cli"]["version_command"] = [sys.executable, str(FAKE), "--version"]
        cfg["models"] = [{"id": "fake-mini", "label": "fake-mini"}, {"id": "fake-std", "label": "fake-std"}]
        cfg["schedule"]["interval_minutes"] = 1
        cfg["data_dir"] = "data-demo"  # never mixed with real measurements
    config.write_json(target, cfg)
    print(f"wrote {target}" + ("  (demo: fake Vero CLI, data in data-demo/)" if a.demo else ""))
    return 0


def cmd_configure(a) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    cur = config.read_json(config.EXAMPLE_FILE)
    if target.exists():
        try:
            cur = config.read_json(target)
        except ConfigError as e:
            print(f"current config is broken, starting from the defaults ({e})")
    if str(cur.get("data_dir", "")).startswith("data-demo"):
        cur = config.read_json(config.EXAMPLE_FILE)  # leaving demo mode
    cur = config._merge(config.DEFAULTS, cur)
    print("\nVero latency monitor: configuration. Press Enter to keep the value in [brackets].\n")
    print("1. How to run the Vero CLI once, non-interactively. Check with: vero --help")
    print("   Placeholders: {prompt} = the probe prompt, {model} = model id. Without {prompt} the prompt goes to stdin.")
    while True:
        cmd = _split(_ask("   Command", _join(cur["cli"]["command"])))
        found = shutil.which(cmd[0]) if cmd else None
        if cmd and found:
            print(f"   found: {found}")
            break
        print(f"   '{cmd[0] if cmd else ''}' was not found. Give the full path (run: where vero), or type it again to keep it.")
        if cmd and _ask("   Keep it anyway? (y/n)", "n").lower().startswith("y"):
            break
    cur["cli"]["command"] = cmd
    cur["cli"]["prompt_via"] = "arg" if any("{prompt}" in c for c in cmd) else "stdin"
    ver = cur["cli"].get("version_command") or []
    if ver and ver[0] in ("vero", "vero.exe", "vero.cmd"):
        cur["cli"]["version_command"] = [cmd[0]] + ver[1:]

    print("\n2. Model ids to probe, comma separated. Put the cheapest first. Empty = the CLI default model.")
    ids = [m["id"] for m in cur["models"] if "<<" not in m["id"]]
    raw = _ask("   Models", ",".join(ids) or "")
    ids = [x.strip() for x in raw.split(",")] if raw.strip() else [""]
    cur["models"] = [{"id": i, "label": i or "default"} for i in ids]

    print("\n3. Timing")
    try:
        cur["schedule"]["interval_minutes"] = int(_ask("   Probe every N minutes", str(cur["schedule"]["interval_minutes"])))
        cur["cli"]["timeout_s"] = float(_ask("   Timeout per call, seconds", f"{float(cur['cli']['timeout_s']):g}"))
        cur["thresholds_ms"]["warn"] = float(_ask("   Warn from, seconds", f"{cur['thresholds_ms']['warn'] / 1000:g}")) * 1000
        cur["thresholds_ms"]["crit"] = float(_ask("   Critical from, seconds", f"{cur['thresholds_ms']['crit'] / 1000:g}")) * 1000
        config.validate(config._merge(config.DEFAULTS, cur))
    except (ConfigError, KeyError, TypeError, ValueError) as e:
        print(f"\nnot saved: {e}")
        return 1
    config.write_json(target, cur)
    print(f"\nsaved {target}")
    return 0


def cmd_doctor(a, cfg) -> int:
    cli = cfg["cli"]
    ok = True
    print(f"config         {cfg['_path']}")
    print(f"data           {cfg['data_dir']}")
    exe = cli["command"][0]
    found = shutil.which(exe)
    print(f"executable     {exe} -> {found or 'NOT FOUND (use the full path, see: where vero)'}")
    ok &= bool(found)
    print(f"cli version    {cli_version(cfg)}")
    for m in cfg["models"]:
        args = build_command(cli["command"], cfg["prompt"], m["id"], cli["prompt_via"])
        stdin = cfg["prompt"] if cli["prompt_via"] == "stdin" else None
        res = time_command(args, stdin, cli["timeout_s"], cli.get("env"))
        status, err = classify(res, cfg.get("expect", ""))
        ms = f"{res['total_ms']:.0f} ms" if res["total_ms"] is not None else "-"
        print(f"probe {m['label']:<12} {status:<11}{ms:>9}   {err or res['stdout'].strip()[:60]!r}")
        print(f"               command: {_join(args)}")
        ok &= status == "ok"
    print("RESULT         " + ("ready" if ok else "NOT READY: fix the items above (guide, section Troubleshooting)"))
    return 0 if ok else 1


def cmd_probe(a, cfg) -> int:
    m = run_cycle(cfg, Store(cfg["data_dir"]), a.trigger)
    if m is None:
        print("another run is in progress; skipped")
        return 0
    if not a.quiet:
        import json
        print(json.dumps(m, indent=2))
    if a.trigger == "task":
        return 0  # failed probes are data, not a task failure (keeps Task Scheduler "Last Result" = 0)
    return 0 if m["totals"]["failed"] == 0 else 2


def cmd_serve(a, cfg) -> int:
    host = a.host or cfg["server"]["host"]
    port = a.port or cfg["server"]["port"]
    cfg["server"]["host"], cfg["server"]["port"] = host, port
    with_sched = bool(cfg["schedule"]["run_in_dashboard"]) and not a.no_scheduler
    return serve(cfg, Store(cfg["data_dir"]), host, port, with_sched, a.open)


def _set_run_in_dashboard(cfg: dict, value: bool) -> None:
    raw = config.read_json(Path(cfg["_path"]))
    raw.setdefault("schedule", {})["run_in_dashboard"] = value
    config.write_json(Path(cfg["_path"]), raw)


def cmd_install(a, cfg) -> int:
    every = int(a.every or cfg["schedule"]["interval_minutes"])
    if not 1 <= every <= 1440:
        print("--every must be between 1 and 1440 minutes")
        return 1
    url = f"http://127.0.0.1:{cfg['server']['port']}/"
    for line in scheduler.install(every, url, dashboard=not a.no_dashboard):
        print(line)
    _set_run_in_dashboard(cfg, False)
    print("config: schedule.run_in_dashboard = false (the OS scheduler runs the probes now)")
    print(f"open the dashboard: {url}")
    return 0


def cmd_uninstall(a, cfg) -> int:
    for line in scheduler.remove():
        print(line)
    _set_run_in_dashboard(cfg, True)
    print("config: schedule.run_in_dashboard = true. Data is kept in " + cfg["data_dir"])
    return 0


def cmd_open(a, cfg) -> int:
    """Wait for the background dashboard to answer, then open it in the browser."""
    import webbrowser
    port = cfg["server"]["port"]
    url = f"http://127.0.0.1:{port}/"
    deadline = time.time() + a.wait
    while not already_running("127.0.0.1", port):
        if time.time() > deadline:
            print(f"dashboard is not running at {url}: use start_dashboard.bat, or see data/monitor.log")
            return 1
        time.sleep(1)
    webbrowser.open(url)
    print(f"opened {url}")
    return 0


def cmd_status(a, cfg) -> int:
    store = Store(cfg["data_dir"])
    last = store.last_run()
    port = cfg["server"]["port"]
    print(f"version        {__version__}")
    print(f"config         {cfg['_path']}")
    print(f"data           {cfg['data_dir']}  ({store.max_probe_id()} probes recorded)")
    print(f"last run       {last['run_id'] + ' at ' + last['started_at'] if last else 'none yet'}")
    print(f"run now        {'yes' if run_in_progress(cfg) else 'no'}")
    print(f"dashboard      {'running at http://127.0.0.1:%d/' % port if already_running('127.0.0.1', port) else 'not running'}")
    print(f"scheduler      {'dashboard window' if cfg['schedule']['run_in_dashboard'] else 'OS (Task Scheduler / cron)'}"
          f", every {cfg['schedule']['interval_minutes']} min\n")
    print(scheduler.status())
    return 0


def cmd_export(a, cfg) -> int:
    data = Store(cfg["data_dir"]).to_csv(time.time() - a.hours * 3600 if a.hours else 0, a.model)
    out = Path(a.out or f"vero_latency_{dt.date.today():%Y%m%d}.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(data, encoding="utf-8")
    print(f"wrote {out} ({data.count(chr(10)) - 1} rows)")
    return 0


def cmd_report(a, cfg) -> int:
    out = Path(a.out or f"vero_latency_report_{dt.date.today():%Y%m%d}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(static_report(cfg, Store(cfg["data_dir"]), a.hours, a.model), encoding="utf-8")
    print(f"wrote {out} (last {a.hours:g} h, self-contained, can be emailed)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vlm", description="Vero CLI latency monitor (ASPF-1578)")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--config", help="path to monitor.json (default config/monitor.json, or env VLM_CONFIG)")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", metavar="command")
    sub.required = True

    s = sub.add_parser("init", help="create config/monitor.json from the example")
    s.add_argument("--demo", action="store_true", help="use the bundled fake Vero CLI (data in data-demo/)")
    s.add_argument("--force", action="store_true")
    sub.add_parser("configure", help="guided set-up of the Vero command, models and thresholds")
    sub.add_parser("doctor", help="check the Vero CLI connection with one test call per model (nothing stored)")

    s = sub.add_parser("probe", help="run one probe cycle now and store it")
    s.add_argument("--trigger", default="manual", choices=["manual", "task", "schedule", "dashboard"])
    s.add_argument("-q", "--quiet", action="store_true")

    s = sub.add_parser("serve", help="start the dashboard (with the built-in scheduler unless installed)")
    s.add_argument("--host")
    s.add_argument("--port", type=int)
    s.add_argument("--no-scheduler", action="store_true")
    s.add_argument("--open", action="store_true", help="open the browser")

    s = sub.add_parser("install", help="unattended mode: OS scheduler task + dashboard at logon + desktop shortcut")
    s.add_argument("--every", type=int, help="minutes (default: schedule.interval_minutes)")
    s.add_argument("--no-dashboard", action="store_true", help="only the probe task")
    sub.add_parser("uninstall", help="remove the tasks and the shortcut (data is kept)")
    sub.add_parser("status", help="show configuration, last run, dashboard and task state")
    s = sub.add_parser("open", help="open the running dashboard in the browser")
    s.add_argument("--wait", type=float, default=20, help="seconds to wait for it to start")

    for name, helptext in (("export", "write probes to CSV"), ("report", "write a self-contained HTML report")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("--hours", type=float, default=0 if name == "export" else 168)
        s.add_argument("--model")
        s.add_argument("--out")
    return p


HANDLERS = {"doctor": cmd_doctor, "probe": cmd_probe, "serve": cmd_serve, "install": cmd_install,
            "uninstall": cmd_uninstall, "status": cmd_status, "open": cmd_open, "export": cmd_export, "report": cmd_report}


def main(argv: list[str] | None = None) -> int:
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
    _setup_logging(cfg["data_dir"], a.verbose)
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
