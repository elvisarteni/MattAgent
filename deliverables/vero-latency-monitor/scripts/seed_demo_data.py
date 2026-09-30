#!/usr/bin/env python3
"""Fill data/latency.db with 7 days of synthetic probes so the dashboard can be shown
before a real Vero CLI is connected. Demo only: never run this against real data.

usage: python scripts/seed_demo_data.py [--days 7] [--interval 15]"""
import argparse
import datetime as dt
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vero_latency import config  # noqa: E402
from vero_latency.probe import iso  # noqa: E402
from vero_latency.store import Store  # noqa: E402

a = argparse.ArgumentParser()
a.add_argument("--days", type=int, default=7)
a.add_argument("--interval", type=int, default=15)
args = a.parse_args()

cfg = config.load()
store = Store(cfg["data_dir"])
now = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0)
t = now - dt.timedelta(days=args.days)
n = 0
while t < now:
    run_id = f"{t:%Y%m%d-%H%M}-vero-latency-demo"
    if not store.run_exists(run_id):
        store.start_run({"run_id": run_id, "started_at": iso(t), "trigger": "demo", "host": "demo",
                         "tool_version": "demo", "cli_version": "vero-fake 0.0.1", "prompt_sha256": ""})
        busy = 1.0 + 0.6 * (8 <= t.hour <= 16)  # office hours are slower
        for i, m in enumerate(cfg["models"]):
            base = (1100 + 1300 * i) * busy
            ms = random.lognormvariate(0, 0.3) * base * (4 if random.random() < 0.02 else 1)
            status = "ok"
            err = None
            r = random.random()
            if r < 0.015:
                status, err, ms = "error", "exit 3: error: upstream model unavailable (demo)", ms * 0.3
            elif r < 0.02:
                status, err, ms = "timeout", "no answer within timeout", cfg["cli"]["timeout_s"] * 1000
            store.add_probe({"run_id": run_id, "ts": iso(t), "epoch": t.timestamp(), "model": m["label"],
                             "model_id": m["id"], "status": status, "total_ms": round(ms, 1),
                             "first_byte_ms": round(ms * 0.85, 1) if status == "ok" else None,
                             "exit_code": 0 if status == "ok" else (3 if status == "error" else None),
                             "out_chars": 3 if status == "ok" else 0, "error": err})
            n += 1
        store.finish_run(run_id, iso(t))
    t += dt.timedelta(minutes=args.interval)
print(f"seeded {n} demo probes into {store.path}")
