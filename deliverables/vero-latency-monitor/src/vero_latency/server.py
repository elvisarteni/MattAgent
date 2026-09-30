"""Local web server: dashboard page, JSON API and a live Server-Sent Events stream."""
from __future__ import annotations

import datetime as dt
import json
import logging
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import __version__, stats
from .config import public_view
from .probe import run_in_progress
from .scheduler import Loop
from .store import Store

log = logging.getLogger("vero_latency")
WEB = Path(__file__).parent / "web"
RANGES = (1, 6, 24, 168, 720)


def parse_hours(value: str | None, default: float = 24) -> float:
    try:
        h = float(value) if value is not None else default
    except ValueError:
        return default
    return h if h in RANGES else default


def dashboard_payload(cfg: dict, store: Store, hours: float, model: str | None,
                      loop: Loop | None = None) -> dict:
    since = time.time() - hours * 3600
    rows = store.probes(since, model)
    warn, crit = cfg["thresholds_ms"]["warn"], cfg["thresholds_ms"]["crit"]
    labels = [m["label"] for m in cfg["models"]]
    seen = sorted({r["model"] for r in rows} - set(labels))
    per_model = []
    for label in labels + seen:
        if model and label != model:
            continue
        s = stats.summarize([r for r in rows if r["model"] == label], warn, crit)
        s["model"] = label
        per_model.append(s)
    bucket = stats.bucket_seconds(hours)
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "tool_version": __version__,
        "range_hours": hours,
        "model": model,
        "config": public_view(cfg),
        "state": {
            "running": bool(loop and loop.running) or run_in_progress(cfg),
            "scheduler": "dashboard" if loop and loop.active else "external",
            "next_run_epoch": loop.expected_next() if loop else None,
            "last_run": store.last_run(),
        },
        "overall": stats.summarize(rows, warn, crit),
        "per_model": per_model,
        "series": {"bucket_s": bucket, "models": stats.series(rows, bucket)},
        "failures": [{k: r[k] for k in ("ts", "epoch", "model", "status", "error")}
                     for r in rows if r["status"] != "ok"][-50:],
        "recent": store.probes(since, model, limit=15, newest_first=True),
    }


def static_report(cfg: dict, store: Store, hours: float, model: str | None) -> str:
    payload = dashboard_payload(cfg, store, hours, model)
    html = (WEB / "dashboard.html").read_text(encoding="utf-8")
    blob = json.dumps(payload).replace("<", "\\u003c")  # nothing in the data can open or close a tag
    return html.replace("<!--STATIC_DATA-->", f"<script>window.STATIC_DATA={blob};</script>", 1)


def make_handler(cfg: dict, store: Store, loop: Loop | None):
    port = cfg["server"]["port"]
    bind = cfg["server"]["host"]
    allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}", f"{bind}:{port}"}

    class Handler(BaseHTTPRequestHandler):
        server_version = f"vero-latency/{__version__}"

        def log_message(self, fmt, *args):
            log.debug("%s " + fmt, self.address_string(), *args)

        def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj, code: int = 200):
            self._send(code, json.dumps(obj).encode(), "application/json")

        def _host_ok(self) -> bool:
            # blocks DNS rebinding: only requests addressed to this local server
            if bind == "0.0.0.0":
                return True
            return (self.headers.get("Host") or "").lower() in allowed_hosts

        def _same_origin(self) -> bool:
            # blocks other web pages from POSTing (a probe costs tokens)
            origin = self.headers.get("Origin")
            if origin is None:
                return True
            return urlparse(origin).netloc.lower() == (self.headers.get("Host") or "").lower()

        def do_GET(self):
            try:
                if not self._host_ok():
                    return self._json({"error": "forbidden host"}, 403)
                u = urlparse(self.path)
                q = {k: v[0] for k, v in parse_qs(u.query).items()}
                hours = parse_hours(q.get("hours"))
                model = q.get("model") or None
                if u.path in ("/", "/index.html"):
                    self._send(200, (WEB / "dashboard.html").read_bytes(), "text/html; charset=utf-8")
                elif u.path == "/api/dashboard":
                    self._json(dashboard_payload(cfg, store, hours, model, loop))
                elif u.path == "/api/health":
                    self._json({"status": "up", "app": "vero-latency", "version": __version__})
                elif u.path == "/api/export.csv":
                    name = f"vero_latency_{dt.date.today():%Y%m%d}.csv"
                    self._send(200, store.to_csv(time.time() - hours * 3600, model).encode(), "text/csv",
                               {"Content-Disposition": f'attachment; filename="{name}"'})
                elif u.path == "/api/stream":
                    self._stream()
                else:
                    self._json({"error": "not found"}, 404)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass
            except Exception:
                log.exception("request failed: %s", self.path)
                try:
                    self._json({"error": "internal error, see data/monitor.log"}, 500)
                except OSError:
                    pass

        def do_POST(self):
            if not self._host_ok() or not self._same_origin():
                return self._json({"error": "forbidden"}, 403)
            if urlparse(self.path).path != "/api/probe":
                return self._json({"error": "not found"}, 404)
            if loop is None:
                return self._json({"error": "scheduler unavailable"}, 503)
            if run_in_progress(cfg):
                return self._json({"started": False, "running": True}, 409)
            started = loop.trigger("dashboard")
            self._json({"started": started, "running": True}, 202 if started else 409)

        def _stream(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            last_id = store.max_probe_id()
            was = None
            beat = time.time()
            while True:
                running = bool(loop and loop.running) or run_in_progress(cfg)
                nxt = loop.expected_next() if loop else None
                if (running, nxt) != was:
                    self._event("state", {"running": running, "next_run_epoch": nxt})
                    was = (running, nxt)
                for p in store.probes(after_id=last_id):
                    self._event("probe", p)
                    last_id = max(last_id, p["id"])
                if time.time() - beat > 15:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    beat = time.time()
                time.sleep(1.5)

        def _event(self, name: str, data: dict):
            self.wfile.write(f"event: {name}\ndata: {json.dumps(data)}\n\n".encode())
            self.wfile.flush()

    return Handler


def already_running(host: str, port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://{host}:{port}/api/health", timeout=2) as r:
            return json.load(r).get("app") == "vero-latency"
    except Exception:
        return False


def serve(cfg: dict, store: Store, host: str, port: int, with_scheduler: bool, open_browser: bool) -> int:
    local = "127.0.0.1" if host == "0.0.0.0" else host
    url = f"http://{local}:{port}/"
    if already_running(local, port):
        print(f"Dashboard already running: {url}")
        if open_browser:
            webbrowser.open(url)
        return 0
    loop = Loop(cfg, store)
    try:
        httpd = ThreadingHTTPServer((host, port), make_handler(cfg, store, loop))
    except OSError as e:
        msg = f"cannot listen on {host}:{port} ({e}). Another program uses the port: change server.port in config/monitor.json"
        log.error(msg)
        print(msg)
        return 1
    httpd.daemon_threads = True
    if with_scheduler:
        loop.start()
    log.info("dashboard %s (scheduler: %s)", url, "dashboard" if with_scheduler else "external")
    print(f"Dashboard: {url}   (Ctrl+C to stop)")
    print("Scheduler: " + (f"every {cfg['schedule']['interval_minutes']} min (in this window)"
                           if with_scheduler else "external (Task Scheduler / cron)"))
    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()  # only after the socket is bound
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        httpd.server_close()
    return 0
