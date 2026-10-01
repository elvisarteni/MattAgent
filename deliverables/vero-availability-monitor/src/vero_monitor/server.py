"""Local status page: dashboard HTML, JSON API and a Server-Sent Events stream.
Binds to 127.0.0.1. Host and Origin are checked (no DNS rebinding, no cross-site 'check now')."""

from __future__ import annotations

import contextlib
import csv
import io
import json
import logging
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Optional, Type
from urllib.parse import parse_qs, urlparse

from . import __version__
from .config import Config
from .report import WEB, parse_hours, payload
from .runner import in_progress
from .scheduler import Loop
from .store import CSV_HEADER, Store

log = logging.getLogger("vero_monitor")
APP_ID = "vero-availability"


def make_handler(cfg: Config, store: Store, loop: Optional[Loop]) -> Type[BaseHTTPRequestHandler]:
    allowed_hosts = {f"127.0.0.1:{cfg.port}", f"localhost:{cfg.port}", f"{cfg.host}:{cfg.port}"}

    def running() -> bool:
        return bool(loop and loop.running) or in_progress(cfg)

    def state() -> Dict[str, Any]:
        return {
            "running": running(),
            "scheduler": "dashboard" if loop and loop.active else "external",
            "next_run": loop.expected_next() if loop else None,
        }

    class Handler(BaseHTTPRequestHandler):
        server_version = f"{APP_ID}/{__version__}"

        def log_message(self, format: str, *args: Any) -> None:
            log.debug("%s " + format, self.address_string(), *args)

        def _send(self, code: int, body: bytes, ctype: str, extra: Optional[Dict[str, str]] = None) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj: Any, code: int = 200) -> None:
            self._send(code, json.dumps(obj).encode(), "application/json")

        def _host_ok(self) -> bool:
            return cfg.host == "0.0.0.0" or (self.headers.get("Host") or "").lower() in allowed_hosts

        def _same_origin(self) -> bool:
            origin = self.headers.get("Origin")
            return origin is None or urlparse(origin).netloc.lower() == (self.headers.get("Host") or "").lower()

        def do_GET(self) -> None:
            try:
                if not self._host_ok():
                    return self._json({"error": "forbidden host"}, 403)
                u = urlparse(self.path)
                q = {k: v[0] for k, v in parse_qs(u.query).items()}
                hours = parse_hours(q.get("hours"))
                if u.path in ("/", "/index.html"):
                    self._send(200, (WEB / "dashboard.html").read_bytes(), "text/html; charset=utf-8")
                elif u.path == "/api/status":
                    s = state()
                    self._json(payload(cfg, store, hours, running=s["running"], scheduler=s["scheduler"], next_run=s["next_run"]))
                elif u.path == "/api/health":
                    self._json({"status": "up", "app": APP_ID, "version": __version__})
                elif u.path == "/api/export.csv":
                    buf = io.StringIO()
                    w = csv.writer(buf, lineterminator="\n")
                    w.writerow(CSV_HEADER)
                    w.writerows(store.csv_rows(time.time() - hours * 3600))
                    self._send(
                        200,
                        buf.getvalue().encode(),
                        "text/csv",
                        {"Content-Disposition": 'attachment; filename="vero_availability.csv"'},
                    )
                elif u.path == "/api/stream":
                    self._stream()
                else:
                    self._json({"error": "not found"}, 404)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass
            except Exception:
                log.exception("request failed: %s", self.path)
                with contextlib.suppress(OSError):
                    self._json({"error": "internal error, see data/monitor.log"}, 500)

        def do_POST(self) -> None:
            if not self._host_ok() or not self._same_origin():
                return self._json({"error": "forbidden"}, 403)
            if urlparse(self.path).path != "/api/check":
                return self._json({"error": "not found"}, 404)
            if loop is None:
                return self._json({"error": "unavailable"}, 503)
            if running():
                return self._json({"started": False, "running": True}, 409)
            started = loop.trigger("dashboard")
            self._json({"started": started, "running": True}, 202 if started else 409)

        def _stream(self) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            last = store.last_epoch()
            was: Optional[Dict[str, Any]] = None
            beat = time.time()
            while True:
                s = state()
                if s != was:
                    self._event("state", s)
                    was = s
                for r in store.runs(after_epoch=last, newest_first=False):
                    self._event("run", r)
                    last = max(last, r["epoch"])
                if time.time() - beat > 15:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    beat = time.time()
                time.sleep(1.5)

        def _event(self, name: str, data: Any) -> None:
            self.wfile.write(f"event: {name}\ndata: {json.dumps(data)}\n\n".encode())
            self.wfile.flush()

    return Handler


def already_running(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=2) as r:
            return bool(json.load(r).get("app") == APP_ID)
    except Exception:
        return False


def serve(cfg: Config, store: Store, with_scheduler: bool, open_browser: bool) -> int:
    url = f"http://127.0.0.1:{cfg.port}/"
    if already_running(cfg.port):
        print(f"Dashboard already running: {url}")
        if open_browser:
            webbrowser.open(url)
        return 0
    loop = Loop(cfg, store)
    try:
        httpd = ThreadingHTTPServer((cfg.host, cfg.port), make_handler(cfg, store, loop))
    except OSError as e:
        msg = f"cannot listen on {cfg.host}:{cfg.port} ({e}); set server.port in config/monitor.json"
        log.error(msg)
        print(msg)
        return 1
    httpd.daemon_threads = True
    if with_scheduler:
        loop.start()
    log.info("dashboard %s (scheduler: %s)", url, "dashboard" if with_scheduler else "external")
    print(f"Dashboard: {url}   (Ctrl+C to stop)")
    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()  # after the socket is bound
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        httpd.server_close()
    return 0
