"""Builds the status-page payload (JSON) from stored runs, using the pure domain rules."""

from __future__ import annotations

import datetime as dt
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

from . import __version__
from .config import Config
from .domain import Check, Status, availability_percent, current_since, incidents, timeline
from .store import Store

RANGES = {1: 60, 6: 72, 24: 96, 168: 168, 720: 120}  # hours -> timeline bars
WEB = Path(__file__).parent / "web"


def parse_hours(value: Optional[str], default: int = 24) -> int:
    try:
        h = int(float(value)) if value is not None else default
    except ValueError:
        return default
    return h if h in RANGES else default


def payload(
    cfg: Config,
    store: Store,
    hours: int,
    *,
    running: bool = False,
    scheduler: str = "external",
    next_run: Optional[float] = None,
    now: Optional[float] = None,
) -> Dict[str, Any]:
    now = time.time() if now is None else now
    start = now - hours * 3600
    month = store.points(now - 30 * 86400)
    in_range = [p for p in month if p.epoch >= start] if hours <= 720 else store.points(start)
    status, since = current_since(month)

    def window(h: int) -> Optional[float]:
        return availability_percent([p.status for p in month if p.epoch >= now - h * 3600])

    components = {}
    for chk, on in ((Check.CLI, cfg.check_cli), (Check.TASK, cfg.check_task), (Check.CHAT, cfg.check_chat)):
        last = store.latest_check(chk.value) if on else None
        components[chk.value] = {
            "enabled": on,
            **(
                {k: last[k] for k in ("status", "epoch", "duration_ms", "detail", "version", "provider_id", "model_id")}
                if last
                else {}
            ),
        }

    incs = sorted(incidents(in_range), key=lambda i: -i.start)[:20]
    return {
        "generated_at": dt.datetime.fromtimestamp(now, dt.timezone.utc).isoformat(timespec="seconds"),
        "now": now,
        "tool_version": __version__,
        "range_hours": hours,
        "config": cfg.public(),
        "state": {"running": running, "scheduler": scheduler, "next_run_epoch": next_run},
        "current": {"status": status.value, "since": since},
        "availability": {"24h": window(24), "7d": window(168), "30d": window(720)},
        "counts": {s.value: sum(1 for p in in_range if p.status is s) for s in (Status.UP, Status.DEGRADED, Status.DOWN)},
        "timeline": [{"t": t, "status": s.value, "n": n} for t, s, n in timeline(in_range, start, now, RANGES[hours])],
        "incidents": [
            {
                "start": i.start,
                "end": i.end,
                "worst": i.worst.value,
                "runs": i.runs,
                "duration_s": round(i.duration_s(now)),
                "reason": i.reason,
            }
            for i in incs
        ],
        "components": components,
        "recent": store.runs(start, limit=20),
    }


def static_html(cfg: Config, store: Store, hours: int) -> str:
    """Self-contained HTML snapshot (e-mailable). Every '<' in the data is escaped."""
    blob = json.dumps(payload(cfg, store, hours)).replace("<", "\\u003c")
    html = (WEB / "dashboard.html").read_text(encoding="utf-8")
    return html.replace("<!--STATIC_DATA-->", f"<script>window.STATIC_DATA={blob};</script>", 1)
