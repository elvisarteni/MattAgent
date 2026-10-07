"""Web server for the dashboard.

Local mode (default): binds to 127.0.0.1; Host and Origin are checked so other web pages cannot use it.
Server mode (team server): binds to all interfaces, no login. Everyone can read the status; "Check now"
is limited to once per COOLDOWN_S for viewers. Settings and stopping need the admin key, sent in the
X-Admin-Key header (the page takes it once from an admin link). Quit does not exist in server mode.
"""

from __future__ import annotations

import hmac
import json
import logging
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type
from urllib.parse import urlparse

from . import APP_ID, __version__
from .monitor import Monitor
from .settings import SettingsError

log = logging.getLogger("vero_status")
INDEX = Path(__file__).parent / "web" / "index.html"
MAX_BODY = 10_000
COOLDOWN_S = 5 * 60  # server mode: viewers may start a check at most this often


def make_handler(
    monitor: Monitor, port: int, on_quit: Callable[[], None], server_mode: bool = False, admin_key: Optional[str] = None
) -> Type[BaseHTTPRequestHandler]:
    local_names = {"127.0.0.1", "localhost", "[::1]"}  # any port: VS Code or `ssh -L` may forward from another one

    class Handler(BaseHTTPRequestHandler):
        server_version = f"{APP_ID}/{__version__}"

        def log_message(self, format: str, *args: Any) -> None:
            log.debug("%s " + format, self.address_string(), *args)

        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")  # the admin link never leaks via Referer
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj: Any, code: int = 200) -> None:
            self._send(code, json.dumps(obj).encode(), "application/json")

        def _is_admin(self) -> bool:
            if not server_mode:
                return True  # local mode: the only user is the person at this computer
            given = self.headers.get("X-Admin-Key") or ""
            return bool(admin_key) and hmac.compare_digest(given.encode(), str(admin_key).encode())

        def _allowed(self, post: bool) -> bool:
            host = (self.headers.get("Host") or "").lower()
            if not server_mode and re.sub(r":\d+$", "", host) not in local_names:
                return False  # blocks DNS rebinding: only loopback names, whatever the forwarded port
            origin = self.headers.get("Origin")
            return not post or origin is None or urlparse(origin).netloc.lower() == host

        def do_GET(self) -> None:
            if not self._allowed(post=False):
                return self._json({"error": "forbidden"}, 403)
            path = urlparse(self.path).path
            if path in ("/", "/index.html"):
                self._send(200, INDEX.read_bytes(), "text/html; charset=utf-8")
            elif path == "/api/state":
                admin = self._is_admin()
                cooldown = max(0.0, monitor.last_manual + COOLDOWN_S - time.time()) if server_mode and not admin else 0.0
                self._json({"version": __version__, "admin": admin, "check_wait_s": round(cooldown), **monitor.state(admin)})
            elif path == "/api/health":
                self._json({"app": APP_ID, "version": __version__})
            else:
                self._json({"error": "not found"}, 404)

        def do_POST(self) -> None:
            if not self._allowed(post=True):
                return self._json({"error": "forbidden"}, 403)
            path = urlparse(self.path).path
            admin = self._is_admin()
            if path == "/api/check":
                wait = monitor.last_manual + COOLDOWN_S - time.time()
                if server_mode and not admin and wait > 0:
                    return self._json({"error": f"checked recently; try again in {int(wait // 60) + 1} min"}, 429)
                started = monitor.check_now("manual")
                if started:
                    monitor.last_manual = time.time()
                return self._json({"started": started}, 202 if started else 409)
            if path == "/api/settings":
                if not admin:
                    return self._json({"error": "settings can only be changed with the admin link"}, 403)
                try:
                    length = int(self.headers.get("Content-Length") or 0)
                    if not 0 < length <= MAX_BODY:
                        raise SettingsError("empty or too large request")
                    changes = json.loads(self.rfile.read(length))
                    if not isinstance(changes, dict):
                        raise SettingsError("expected a JSON object")
                    monitor.update_settings(changes)
                except (SettingsError, ValueError, TypeError) as e:
                    return self._json({"error": str(e)}, 400)
                return self._json({"saved": True})
            if path == "/api/quit" and not server_mode:
                self._json({"stopping": True})
                threading.Thread(target=on_quit, daemon=True).start()
                return None
            return self._json({"error": "not found"}, 404)

    return Handler


def create(
    monitor: Monitor,
    port: int,
    on_quit: Optional[Callable[[], None]] = None,
    server_mode: bool = False,
    admin_key: Optional[str] = None,
    host: Optional[str] = None,
) -> ThreadingHTTPServer:
    holder: Dict[str, ThreadingHTTPServer] = {}

    def quit_() -> None:
        monitor.stop()
        holder["srv"].shutdown()
        if on_quit:
            on_quit()

    bind = host or ("0.0.0.0" if server_mode else "127.0.0.1")  # noqa: S104 (server mode serves the team)
    srv = ThreadingHTTPServer((bind, port), make_handler(monitor, port, quit_, server_mode, admin_key))
    srv.daemon_threads = True
    holder["srv"] = srv
    return srv
