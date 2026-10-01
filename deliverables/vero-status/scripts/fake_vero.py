#!/usr/bin/env python3
"""Stand-in for the Vero CLI (demo and tests): `version`, `config`, `task --json ...` like Vero CLI 2.3.x.

FAKE_VERO_MODE: ok (default) | down | auth | hang | nocompletion | refuse
FAKE_VERO_DELAY: seconds before answering (default 2)
"""

import json
import os
import sys
import time


def emit(obj):
    print(json.dumps(obj), flush=True)


def main(argv):
    cmd = argv[0] if argv else "version"
    if cmd in ("version", "--version"):
        print("vero 2.3.3 (fake0000)")
        return 0
    if cmd == "config":
        print("actModeApiProvider : bedrock")
        print("actModeApiModelId  : us.anthropic.claude-opus-5")
        print("awsRegion          : us-west-2")
        return 0
    if cmd not in ("task", "t"):
        print(f"unknown command {cmd}", file=sys.stderr)
        return 2
    args = argv[1:]
    model = args[args.index("-m") + 1] if "-m" in args else "us.anthropic.claude-opus-5"
    info = {"providerId": "bedrock", "modelId": model, "mode": "act"}
    mode = os.environ.get("FAKE_VERO_MODE", "ok")
    delay = float(os.environ.get("FAKE_VERO_DELAY", "2"))
    emit({"type": "task_started", "taskId": str(int(time.time() * 1000))})
    emit({"type": "say", "say": "task", "text": args[-1], "modelInfo": info})
    emit({"type": "say", "say": "api_req_started", "text": "SYSTEM PROMPT FAKE-SECRET-PROMPT", "modelInfo": info})
    if mode == "hang":
        time.sleep(3600)
    if mode == "auth":
        print("error: Unauthorized token=abc123secret", file=sys.stderr)
        return 1
    if mode == "down":
        print("error: provider unavailable (connect ETIMEDOUT)", file=sys.stderr)
        return 1
    time.sleep(delay)
    answer = "I cannot do that." if mode == "refuse" else "OK"
    emit({"type": "say", "say": "text", "text": answer[:1], "partial": True, "modelInfo": info})
    if mode != "nocompletion":
        emit({"type": "say", "say": "completion_result", "text": answer, "modelInfo": info})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
