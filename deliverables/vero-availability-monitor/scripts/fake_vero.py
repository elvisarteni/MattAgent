#!/usr/bin/env python3
"""Stand-in for the Vero CLI (demo and tests). Emulates `vero version` and
`vero task --json -m <model> -t <s> -c <dir> <prompt>` with the event stream of Vero CLI 2.3.x.

FAKE_VERO_MODE: ok | slow | down | auth | nocompletion | refuse | hang | random (default)
FAKE_VERO_DELAY: seconds before the answer (default: about 1-3 s)
"""

import json
import os
import random
import sys
import time

MODEL = {"providerId": "bedrock", "modelId": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "mode": "act"}


def emit(obj):
    print(json.dumps(obj), flush=True)


def main(argv):
    if not argv or argv[0] in ("version", "--version", "-V"):
        print("vero 2.3.3 (fake0000)")
        return 0
    if argv[0] not in ("task", "t"):
        print(f"unknown command {argv[0]}", file=sys.stderr)
        return 2
    args = argv[1:]
    model = MODEL["modelId"]
    if "-m" in args:
        model = args[args.index("-m") + 1]
    prompt = args[-1] if args else ""
    mode = os.environ.get("FAKE_VERO_MODE", "random")
    if mode == "random":
        r = random.random()
        mode = "down" if r < 0.03 else "nocompletion" if r < 0.05 else "slow" if r < 0.09 else "ok"
    delay = float(os.environ.get("FAKE_VERO_DELAY", random.uniform(1.0, 3.0)))
    info = dict(MODEL, modelId=model)
    ts = int(time.time() * 1000)
    if "--json" in args:
        emit({"type": "task_started", "taskId": str(ts)})
        emit({"ts": ts, "type": "say", "say": "task", "text": prompt, "modelInfo": info})
        # the real CLI puts the full upstream prompt here; the monitor must never keep it
        emit(
            {
                "ts": ts,
                "type": "say",
                "say": "api_req_started",
                "text": json.dumps({"request": "SYSTEM PROMPT ... FAKE-SECRET-api_req_started ..."}),
                "modelInfo": info,
            }
        )
    if mode == "hang":
        time.sleep(3600)
    if mode == "auth":
        print("error: Unauthorized (token=abc123secret) - run vero auth", file=sys.stderr)
        return 1
    if mode == "down":
        time.sleep(min(delay, 1))
        print("error: provider unavailable: connect ETIMEDOUT bedrock-runtime.us-west-2", file=sys.stderr)
        return 1
    time.sleep(delay * (6 if mode == "slow" else 1))
    answer = "I cannot help with that." if mode == "refuse" else "OK"
    if "--json" in args:
        emit({"ts": ts, "type": "say", "say": "text", "text": answer[:1], "partial": True, "modelInfo": info})
        emit({"ts": ts, "type": "say", "say": "text", "text": answer, "partial": False, "modelInfo": info})
        if mode != "nocompletion":
            emit({"ts": ts, "type": "say", "say": "completion_result", "text": answer, "modelInfo": info})
    else:
        print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
