#!/usr/bin/env python3
"""Stand-in for the Vero CLI (demo and tests). Answers 'OK' after a realistic delay.

Env: FAKE_VERO_FAIL=1 always fails, =0 never fails, FAKE_VERO_DELAY=<seconds> fixed delay."""
import argparse
import os
import random
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("-p", "--prompt")
p.add_argument("--model", default="fake-mini")
p.add_argument("--version", action="store_true")
a = p.parse_args()
if a.version:
    print("vero-fake 0.0.1")
    sys.exit(0)
prompt = a.prompt if a.prompt is not None else sys.stdin.read()
if os.environ.get("FAKE_VERO_DELAY"):
    delay = float(os.environ["FAKE_VERO_DELAY"])
else:
    base = 1.2 if a.model == "fake-mini" else 2.4
    delay = random.lognormvariate(0, 0.35) * base
    if random.random() < 0.04:
        delay *= 4  # occasional slow answer
time.sleep(delay)
fail = os.environ.get("FAKE_VERO_FAIL")
if fail == "1" or (fail is None and random.random() < 0.03):
    print("error: upstream model unavailable (fake)", file=sys.stderr)
    sys.exit(3)
print("OK")
