"""Program start: one instance, dashboard in the browser, no console window."""

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import logging.handlers
import os
import secrets
import signal
import socket
import sys
import threading
import urllib.request
import webbrowser
from pathlib import Path
from typing import Mapping

from . import APP_ID
from .monitor import Monitor
from .server import create

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
log = logging.getLogger("vero_status")


def message(text: str) -> None:
    """Tell the user something without a console (pythonw): a Windows message box."""
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.user32.MessageBoxW(None, text, "Vero Status", 0x40)
    else:
        print(text)


def can_open_browser(platform: str = sys.platform, env: Mapping[str, str] | None = None) -> bool:
    """False on a headless Linux VM (no desktop): there the URL is printed and logged instead, and you
    open it through VS Code port forwarding or an SSH tunnel."""
    env = os.environ if env is None else env
    if platform in ("win32", "darwin"):
        return True
    return bool(env.get("DISPLAY") or env.get("WAYLAND_DISPLAY"))


def private(path: Path) -> None:
    """Owner-only access on Linux/macOS: a shared VM has other users (no effect on Windows)."""
    if os.name != "nt":
        try:
            path.chmod(0o700 if path.is_dir() else 0o600)
        except OSError:
            log.warning("cannot restrict access to %s", path)


def stop_on_sigterm() -> None:
    """systemd and `kill` send SIGTERM: stop like Ctrl+C so the shutdown is logged and clean."""

    def handler(signum: int, frame: object) -> None:
        raise KeyboardInterrupt

    with contextlib.suppress(ValueError):  # only possible in the main thread
        signal.signal(signal.SIGTERM, handler)


def already_running(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=2) as r:
            return bool(json.load(r).get("app") == APP_ID)
    except Exception:
        return False


def setup_logging() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    private(DATA)  # history, settings, log and the admin key stay readable by you only
    handler = logging.handlers.RotatingFileHandler(DATA / "vero-status.log", maxBytes=500_000, backupCount=2, encoding="utf-8")
    logging.basicConfig(level=logging.INFO, handlers=[handler], format="%(asctime)s %(levelname)s %(message)s", force=True)


def main() -> int:
    setup_logging()
    monitor = Monitor(DATA)
    port = monitor.settings.port
    url = f"http://127.0.0.1:{port}/"
    if already_running(port):
        if can_open_browser():
            webbrowser.open(url)  # second double-click: just show the dashboard
        else:
            print(f"Vero Status is already running: {url}")
        return 0
    try:
        srv = create(monitor, port)
    except OSError as e:
        log.error("cannot use port %s: %s", port, e)
        message(
            f"Vero Status cannot start: port {port} is used by another program.\n\n"
            f'Change "port" in {DATA / "settings.json"} and start it again.'
        )
        return 1
    monitor.start(check_at_start=True)
    log.info("dashboard %s", url)
    if can_open_browser():
        threading.Timer(0.3, webbrowser.open, args=(url,)).start()
    else:  # headless VM: never start a text-mode browser in the background
        print(f"Vero Status runs at {url} (forward port {port} to open it on your laptop)")
    stop_on_sigterm()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()
        srv.server_close()
        log.info("stopped")
    return 0


def admin_key(data: Path) -> str:
    """The server's admin key: created once, kept in data/admin_key.txt (keep this file private)."""
    path = data / "admin_key.txt"
    try:
        key = path.read_text(encoding="utf-8").strip()
        if len(key) >= 16:
            return key
    except OSError:
        pass
    data.mkdir(parents=True, exist_ok=True)
    key = secrets.token_urlsafe(24)
    path.write_text(key + "\n", encoding="utf-8")
    private(path)
    return key


def serve_team(argv: list[str] | None = None) -> int:
    """Server mode: one shared status page for everyone on the network, no login."""
    ap = argparse.ArgumentParser(description="Vero Status team server")
    ap.add_argument("--port", type=int, help="default: port in data/settings.json (8767)")
    ap.add_argument("--host", default="0.0.0.0", help="address to listen on (default: all)")  # noqa: S104
    a = ap.parse_args(argv)
    setup_logging()
    # a terminal shows the links; under systemd or cron (no terminal) they go to data/vero-status.log only,
    # so the admin key does not end up in the system journal, which admins can read
    console = logging.StreamHandler(sys.stdout) if sys.stdout and sys.stdout.isatty() else None
    if console:
        logging.getLogger().addHandler(console)
    monitor = Monitor(DATA, server_mode=True)
    port = a.port or monitor.settings.port
    key = admin_key(DATA)
    try:
        srv = create(monitor, port, server_mode=True, admin_key=key, host=a.host)
    except OSError as e:
        log.error("cannot listen on %s:%s: %s", a.host, port, e)
        return 1
    fqdn = socket.getfqdn() or socket.gethostname()
    loopback = a.host in ("127.0.0.1", "localhost", "::1")
    name = "127.0.0.1" if loopback else fqdn
    log.info("Vero Status team server %s on %s port %s", fqdn, a.host, port)
    if loopback:  # e.g. a cloud VM where only SSH is open
        log.info("Only this machine can connect. From your laptop:  ssh -N -L %s:127.0.0.1:%s <user>@%s", port, port, fqdn)
    log.info("Share with the team:  http://%s:%s/", name, port)
    log.info("Admin link (keep private, it allows changing settings):  http://%s:%s/?admin=%s", name, port, key)
    monitor.start(check_at_start=True)
    stop_on_sigterm()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()
        srv.server_close()
        log.info("stopped")
    return 0


def run() -> None:
    try:
        sys.exit(main())
    except Exception as e:  # last resort: never die silently
        logging.getLogger("vero_status").exception("crash")
        message(f"Vero Status stopped because of an error:\n{e}\n\nDetails: {DATA / 'vero-status.log'}")
        sys.exit(1)
