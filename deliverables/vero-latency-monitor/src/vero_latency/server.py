"""Local web server: dashboard page, JSON API and a live Server-Sent Events stream."""
from __future__ import annotations

import datetime as dt
import json
import logging
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import __version__, stats
from .config import public_view
from .scheduler import Loop
from .store import Store

log = logging.getLogger("vero_latency")
WEB = Path(__file__).parent / "web"
RANGES = {1, 6, 24, 168, 720}


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
            "running": bool(loop and loop.running),
            "next_run_epoch": loop.next_run if loop else None,
            "last_run": store.last_run(),
        },
        "overall": stats.summarize(rows, warn, crit),
        "per_model": per_model,
        "series": {"bucket_s": bucket, "models": stats.series(rows, bucket)},
        "failures": [{k: r[k] for k in ("ts", "epoch", "model", "status", "error")}
                     for r in rows if r["status"] != "ok"][-50:],
        "recent": store.probes(since, model, limit=15, newest_first=True),
    }


def make_handler(cfg: dict, store: Store, loop: Loop | None):
    class Handler(BaseHTTPRequestHandler):
        server_version = f"vero-latency/{__version__}"

        def log_message(self, fmt, *args):
            log.debug("%s " + fmt, self.address_string(), *args)

        def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj, code: int = 200):
            self._send(code, json.dumps(obj).encode(), "application/json")

        def do_GET(self):
            u = urlparse(self.path)
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            hours = float(q.get("hours", 24))
            if hours not in RANGES:
                hours = 24
            model = q.get("model") or None
            if u.path in ("/", "/index.html"):
                self._send(200, (WEB / "dashboard.html").read_bytes(), "text/html; charset=utf-8")
            elif u.path == "/api/dashboard":
                self._json(dashboard_payload(cfg, store, hours, model, loop))
            elif u.path == "/api/health":
                self._json({"status": "up", "version": __version__})
            elif u.path == "/api/export.csv":
                name = f"vero_latency_{dt.date.today():%Y%m%d}.csv"
                self._send(200, store.to_csv(time.time() - hours * 3600, model).encode(), "text/csv",
                           {"Content-Disposition": f'attachment; filename="{name}"'})
            elif u.path == "/api/stream":
                self._stream()
            else:
                self._json({"error": "not found"}, 404)

        def do_POST(self):
            if urlparse(self.path).path != "/api/probe":
                return self._json({"error": "not found"}, 404)
            if loop is None:
                return self._json({"error": "scheduler unavailable"}, 503)
            started = loop.trigger("dashboard")
            self._json({"started": started, "running": True}, 202 if started else 409)

        def _stream(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            last_id = store.max_probe_id()
            was_running = None
            beat = time.time()
            try:
                while True:
                    running = bool(loop and loop.running)
                    if running != was_running:
                        self._event("state", {"running": running,
                                              "next_run_epoch": loop.next_run if loop else None})
                        was_running = running
                    for p in store.probes(after_id=last_id):
                        self._event("probe", p)
                        last_id = max(last_id, p["id"])
                    if time.time() - beat > 15:
                        self.wfile.write(b": ping\n\n")
                        self.wfile.flush()
                        beat = time.time()
                    time.sleep(1.5)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass

        def _event(self, name: str, data: dict):
            self.wfile.write(f"event: {name}\ndata: {json.dumps(data)}\n\n".encode())
            self.wfile.flush()

    return Handler


def serve(cfg: dict, store: Store, host: str, port: int, with_scheduler: bool) -> None:
    loop = Loop(cfg, store)
    if with_scheduler:
        loop.start()
    httpd = ThreadingHTTPServer((host, port), make_handler(cfg, store, loop))
    httpd.daemon_threads = True
    print(f"Dashboard: http://{host}:{port}/   (Ctrl+C to stop)")
    print("Scheduler: " + (f"every {cfg['schedule']['interval_minutes']} min (in this window)"
                           if with_scheduler else "off here (use Task Scheduler / cron)"))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        httpd.server_close()
