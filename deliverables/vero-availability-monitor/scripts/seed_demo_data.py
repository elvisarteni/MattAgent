#!/usr/bin/env python3
"""Fill data-demo/ with 7 days of synthetic checks (with a few incidents) so the status page
can be shown before Vero is connected. Refuses any data folder other than data-demo."""

import datetime as dt
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vero_monitor import config  # noqa: E402
from vero_monitor.domain import Check, CheckResult, RunResult, Status, overall_status  # noqa: E402
from vero_monitor.runner import iso  # noqa: E402
from vero_monitor.store import Store  # noqa: E402

cfg = config.load()
if not cfg.data_dir.name.startswith("data-demo"):
    sys.exit(f"refusing to seed demo data into {cfg.data_dir}: run  vam init --demo  first")
store = Store(cfg.data_dir)
rnd = random.Random(1578)
now = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0)
t = now - dt.timedelta(days=7)
outages = [
    (now - dt.timedelta(days=5, hours=3), 70),
    (now - dt.timedelta(days=2, hours=9), 35),
    (now - dt.timedelta(hours=20), 25),
]
n = 0
while t < now:
    down = any(s <= t < s + dt.timedelta(minutes=m) for s, m in outages)
    task_s = rnd.lognormvariate(0, 0.12) * 52
    checks = [CheckResult(Check.CLI, Status.UP, rnd.uniform(800, 1500), version="vero 2.3.3 (demo)")]
    if down:
        checks.append(
            CheckResult(
                Check.TASK, Status.DOWN, 210000.0, "no completion within 210 s", provider_id="bedrock", model_id=cfg.vero.model
            )
        )
    elif rnd.random() < 0.04:
        checks.append(
            CheckResult(
                Check.TASK,
                Status.DEGRADED,
                task_s * 2000,
                f"slow: {task_s * 2:.0f} s > 90 s",
                provider_id="bedrock",
                model_id=cfg.vero.model,
            )
        )
    else:
        checks.append(CheckResult(Check.TASK, Status.UP, task_s * 1000, provider_id="bedrock", model_id=cfg.vero.model))
    run_id = f"{t:%Y%m%d-%H%M}-vero-availability-demo"
    if not store.run_exists(run_id):
        store.save(RunResult(run_id, iso(t), t.timestamp(), "demo", tuple(checks), overall_status(checks)), "demo", "demo")
        n += 1
    t += dt.timedelta(minutes=15)
print(f"seeded {n} demo runs into {store.path}")
