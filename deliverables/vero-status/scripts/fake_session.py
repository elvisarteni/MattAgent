#!/usr/bin/env python3
"""Simulate a user's Vero session for demos and tests: appends events to <tasks-dir>/<id>/ui_messages.json
in the same shape Vero writes them (Cline-style events with ts, say, modelInfo).

usage: python scripts/fake_session.py <tasks-dir> [--requests 6] [--model us.anthropic.claude-opus-5]
Never point it at your real ~/.vero folder.
"""

import argparse
import json
import random
import time
from pathlib import Path

a = argparse.ArgumentParser()
a.add_argument("tasks_dir")
a.add_argument("--requests", type=int, default=6)
a.add_argument("--model", default="us.anthropic.claude-opus-5")
a.add_argument("--pause", type=float, default=1.5, help="seconds between requests")
args = a.parse_args()

info = {"providerId": "bedrock", "modelId": args.model, "mode": "act"}
task = Path(args.tasks_dir) / f"demo-{int(time.time() * 1000)}"
task.mkdir(parents=True, exist_ok=True)
events = []


def add(ev):
    events.append({"ts": int(time.time() * 1000), **ev, "modelInfo": info})
    (task / "ui_messages.json").write_text(json.dumps(events), encoding="utf-8")


add({"type": "say", "say": "task", "text": "demo task"})
for _ in range(args.requests):
    add({"type": "say", "say": "api_req_started", "text": json.dumps({"tokensIn": random.randint(800, 9000), "tokensOut": 0})})
    time.sleep(random.uniform(1.5, 6.0))
    add({"type": "say", "say": "text", "text": "...", "partial": True})
    time.sleep(args.pause)
add({"type": "say", "say": "completion_result", "text": "done"})
print(f"wrote {task}")
