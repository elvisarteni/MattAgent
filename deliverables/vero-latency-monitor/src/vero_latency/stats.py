"""Latency statistics and time buckets for the dashboard."""
from __future__ import annotations

import math

BUCKET_STEPS = [60, 300, 900, 1800, 3600, 7200, 21600, 43200, 86400]


def percentile(values: list[float], pct: float) -> float | None:
    """Linear interpolation between closest ranks (same as numpy default)."""
    if not values:
        return None
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * pct / 100.0
    lo, hi = math.floor(k), math.ceil(k)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def _r(x):
    return None if x is None else round(x, 1)


def summarize(probes: list[dict], warn_ms: float, crit_ms: float) -> dict:
    """Availability counts every probe; latency figures use successful probes only."""
    total = len(probes)
    ok = [p for p in probes if p["status"] == "ok"]
    lat = [p["total_ms"] for p in ok]
    fb = [p["first_byte_ms"] for p in ok if p.get("first_byte_ms") is not None]
    last = probes[-1] if probes else None
    return {
        "probes": total,
        "ok": len(ok),
        "failed": total - len(ok),
        "availability_percent": round(len(ok) / total * 100, 2) if total else None,
        "avg_ms": _r(sum(lat) / len(lat)) if lat else None,
        "min_ms": _r(min(lat)) if lat else None,
        "p50_ms": _r(percentile(lat, 50)),
        "p95_ms": _r(percentile(lat, 95)),
        "p99_ms": _r(percentile(lat, 99)),
        "max_ms": _r(max(lat)) if lat else None,
        "first_byte_p50_ms": _r(percentile(fb, 50)),
        "warn_breaches": sum(1 for x in lat if warn_ms <= x < crit_ms),
        "crit_breaches": sum(1 for x in lat if x >= crit_ms),
        "last": {k: last[k] for k in ("ts", "status", "total_ms", "model")} if last else None,
    }


def bucket_seconds(range_hours: float, target_points: int = 200) -> int:
    raw = range_hours * 3600 / target_points
    for step in BUCKET_STEPS:
        if step >= raw:
            return step
    return BUCKET_STEPS[-1]


def series(probes: list[dict], bucket_s: int) -> dict:
    """Per model: list of buckets {t, n, fail, p50, p95, avg} ordered by time."""
    grouped: dict[str, dict[int, list[dict]]] = {}
    for p in probes:
        b = int(p["epoch"] // bucket_s * bucket_s)
        grouped.setdefault(p["model"], {}).setdefault(b, []).append(p)
    out = {}
    for model, buckets in grouped.items():
        rows = []
        for t in sorted(buckets):
            items = buckets[t]
            lat = [p["total_ms"] for p in items if p["status"] == "ok"]
            rows.append({
                "t": t,
                "n": len(items),
                "fail": sum(1 for p in items if p["status"] != "ok"),
                "p50": _r(percentile(lat, 50)),
                "p95": _r(percentile(lat, 95)),
                "avg": _r(sum(lat) / len(lat)) if lat else None,
            })
        out[model] = rows
    return out
