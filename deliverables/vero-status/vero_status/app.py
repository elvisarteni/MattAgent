"""Program start: one instance, dashboard in the browser, no console window."""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import secrets
import socket
import sys
import threading
import urllib.request
import webbrowser
from pathlib import Path

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


def already_running(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=2) as r:
            return bool(json.load(r).get("app") == APP_ID)
    except Exception:
        return False


def setup_logging() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(DATA / "vero-status.log", maxBytes=500_000, backupCount=2, encoding="utf-8")
    logging.basicConfig(level=logging.INFO, handlers=[handler], format="%(asctime)s %(levelname)s %(message)s", force=True)


def main() -> int:
    setup_logging()
    monitor = Monitor(DATA)
    port = monitor.settings.port
    url = f"http://127.0.0.1:{port}/"
    if already_running(port):
        webbrowser.open(url)  # second double-click: just show the dashboard
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
    threading.Timer(0.3, webbrowser.open, args=(url,)).start()
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
    return key


def serve_team(argv: list[str] | None = None) -> int:
    """Server mode: one shared status page for everyone on the network, no login."""
    ap = argparse.ArgumentParser(description="Vero Status team server")
    ap.add_argument("--port", type=int, help="default: port in data/settings.json (8767)")
    ap.add_argument("--host", default="0.0.0.0", help="address to listen on (default: all)")  # noqa: S104
    a = ap.parse_args(argv)
    setup_logging()
    console = logging.StreamHandler(sys.stdout) if sys.stdout else None
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
    name = socket.getfqdn() or socket.gethostname()
    log.info("Vero Status team server %s on port %s", name, port)
    log.info("Share with the team:  http://%s:%s/", name, port)
    log.info("Admin link (keep private, it allows changing settings):  http://%s:%s/?admin=%s", name, port, key)
    monitor.start(check_at_start=True)
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
