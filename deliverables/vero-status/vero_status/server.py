"""Local web server for the dashboard. Binds to 127.0.0.1 only.
Host and Origin are checked so other web pages cannot use it."""

from __future__ import annotations

import json
import logging
import threading
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


def make_handler(monitor: Monitor, port: int, on_quit: Callable[[], None]) -> Type[BaseHTTPRequestHandler]:
    hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}

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
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj: Any, code: int = 200) -> None:
            self._send(code, json.dumps(obj).encode(), "application/json")

        def _allowed(self, post: bool) -> bool:
            host = (self.headers.get("Host") or "").lower()
            if host not in hosts:
                return False
            origin = self.headers.get("Origin")
            return not post or origin is None or urlparse(origin).netloc.lower() == host

        def do_GET(self) -> None:
            if not self._allowed(post=False):
                return self._json({"error": "forbidden"}, 403)
            path = urlparse(self.path).path
            if path in ("/", "/index.html"):
                self._send(200, INDEX.read_bytes(), "text/html; charset=utf-8")
            elif path == "/api/state":
                self._json({"version": __version__, **monitor.state()})
            elif path == "/api/health":
                self._json({"app": APP_ID, "version": __version__})
            else:
                self._json({"error": "not found"}, 404)

        def do_POST(self) -> None:
            if not self._allowed(post=True):
                return self._json({"error": "forbidden"}, 403)
            path = urlparse(self.path).path
            if path == "/api/check":
                started = monitor.check_now("manual")
                return self._json({"started": started}, 202 if started else 409)
            if path == "/api/settings":
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
            if path == "/api/quit":
                self._json({"stopping": True})
                threading.Thread(target=on_quit, daemon=True).start()
                return None
            return self._json({"error": "not found"}, 404)

    return Handler


def create(monitor: Monitor, port: int, on_quit: Optional[Callable[[], None]] = None) -> ThreadingHTTPServer:
    holder: Dict[str, ThreadingHTTPServer] = {}

    def quit_() -> None:
        monitor.stop()
        holder["srv"].shutdown()
        if on_quit:
            on_quit()

    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(monitor, port, quit_))
    srv.daemon_threads = True
    holder["srv"] = srv
    return srv
