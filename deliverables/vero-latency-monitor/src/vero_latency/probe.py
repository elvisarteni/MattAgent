"""Run the cheapest prompt through the Vero CLI and time it.

One *run* = one probe per configured model. Each run gets a run_id
(<YYYYMMDD-HHMM>-vero-latency, SCMP naming) and a JSON run manifest.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import os
import platform
import shutil
import subprocess
import threading
import time
from pathlib import Path

from . import COMPONENT, __version__
from .store import Store

log = logging.getLogger("vero_latency")

IS_WINDOWS = os.name == "nt"
NO_WINDOW = 0x08000000 if IS_WINDOWS else 0  # CREATE_NO_WINDOW: no console flash from Task Scheduler
ERROR_MAX = 300


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso(t: dt.datetime) -> str:
    return t.isoformat(timespec="seconds").replace("+00:00", "Z")


def build_command(template: list[str], prompt: str, model_id: str, prompt_via: str) -> list[str]:
    """Fill {prompt}/{model}. An empty model drops the {model} arg and the flag before it."""
    args: list[str] = []
    for a in template:
        if "{model}" in a and not model_id:
            if a == "{model}" and args and args[-1].startswith("-"):
                args.pop()
            continue
        if "{prompt}" in a and prompt_via == "stdin":
            continue
        args.append(a.replace("{prompt}", prompt).replace("{model}", model_id))
    exe = shutil.which(args[0])  # resolves vero.cmd / vero.exe on Windows
    if exe:
        args[0] = exe
    return args


def _kill_tree(proc: subprocess.Popen) -> None:
    try:
        if IS_WINDOWS:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                           capture_output=True, creationflags=NO_WINDOW)
        else:
            proc.kill()
    except OSError:
        pass


def time_command(args: list[str], stdin_text: str | None, timeout_s: float,
                 env_extra: dict | None = None) -> dict:
    """Run one command. Returns total_ms, first_byte_ms, exit_code, stdout, stderr, timed_out."""
    env = dict(os.environ, **{k: str(v) for k, v in (env_extra or {}).items()})
    t0 = time.perf_counter()
    try:
        proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=env, creationflags=NO_WINDOW,
        )
    except OSError as e:
        return {"total_ms": None, "first_byte_ms": None, "exit_code": None,
                "stdout": "", "stderr": f"cannot start {args[0]!r}: {e}", "timed_out": False}

    first = {}
    out_chunks: list[bytes] = []
    err_chunks: list[bytes] = []

    def read_out():
        while True:
            chunk = proc.stdout.read1(4096)
            if not chunk:
                break
            if "t" not in first and chunk.strip():
                first["t"] = time.perf_counter()
            out_chunks.append(chunk)

    def read_err():
        err_chunks.append(proc.stderr.read())

    threads = [threading.Thread(target=read_out, daemon=True),
               threading.Thread(target=read_err, daemon=True)]
    for th in threads:
        th.start()
    if stdin_text is not None:
        try:
            proc.stdin.write(stdin_text.encode("utf-8"))
            proc.stdin.close()
        except OSError:
            pass
    timed_out = False
    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_tree(proc)
        proc.wait()
    t1 = time.perf_counter()
    for th in threads:
        th.join(timeout=5)
    return {
        "total_ms": (t1 - t0) * 1000,
        "first_byte_ms": (first["t"] - t0) * 1000 if "t" in first else None,
        "exit_code": proc.returncode,
        "stdout": b"".join(out_chunks).decode("utf-8", "replace"),
        "stderr": b"".join(err_chunks).decode("utf-8", "replace"),
        "timed_out": timed_out,
    }


def classify(res: dict, expect: str) -> tuple[str, str | None]:
    if res["timed_out"]:
        return "timeout", "no answer within timeout"
    if res["total_ms"] is None:
        return "error", res["stderr"][:ERROR_MAX]
    if res["exit_code"] != 0:
        msg = (res["stderr"].strip() or res["stdout"].strip())[:ERROR_MAX]
        return "error", f"exit {res['exit_code']}: {msg}"
    if expect and expect.lower() not in res["stdout"].lower():
        return "unexpected", f"answer did not contain {expect!r} ({len(res['stdout'])} chars)"
    return "ok", None


def cli_version(cfg: dict) -> str:
    cmd = cfg["cli"].get("version_command") or []
    if not cmd:
        return "n/a"
    res = time_command(build_command(cmd, "", "", "arg"), None, 15, cfg["cli"].get("env"))
    text = (res["stdout"] or res["stderr"]).strip().splitlines()
    return text[0][:80] if res["exit_code"] == 0 and text else "unknown"


def new_run_id(store: Store, now: dt.datetime) -> str:
    base = f"{now:%Y%m%d-%H%M}-{COMPONENT}"
    run_id, n = base, 2
    while store.run_exists(run_id):
        run_id, n = f"{base}-{n}", n + 1
    return run_id


class RunLock:
    """File lock so a Task Scheduler run and a dashboard run never overlap."""

    def __init__(self, data_dir: str, stale_s: float):
        self.path = Path(data_dir) / "probe.lock"
        self.stale_s = stale_s
        self.held = False

    def __enter__(self):
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                self.held = True
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > self.stale_s:
                        self.path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                return self
        return self

    def __exit__(self, *exc):
        if self.held:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


def run_cycle(cfg: dict, store: Store, trigger: str = "manual") -> dict | None:
    """Probe every model once. Returns the run manifest, or None if another run holds the lock."""
    cli = cfg["cli"]
    stale = cli["timeout_s"] * len(cfg["models"]) + 120
    with RunLock(cfg["data_dir"], stale) as lock:
        if not lock.held:
            log.info("another run is in progress; skipped")
            return None
        started = utc_now()
        run = {
            "run_id": new_run_id(store, started),
            "started_at": iso(started),
            "trigger": trigger,
            "host": platform.node(),
            "tool_version": __version__,
            "cli_version": cli_version(cfg),
            "prompt_sha256": hashlib.sha256(cfg["prompt"].encode("utf-8")).hexdigest(),
        }
        store.start_run(run)
        results = []
        for m in cfg["models"]:
            args = build_command(cli["command"], cfg["prompt"], m["id"], cli["prompt_via"])
            stdin = cfg["prompt"] if cli["prompt_via"] == "stdin" else None
            when = utc_now()
            res = time_command(args, stdin, cli["timeout_s"], cli.get("env"))
            status, error = classify(res, cfg.get("expect", ""))
            probe = {
                "run_id": run["run_id"],
                "ts": iso(when),
                "epoch": when.timestamp(),
                "model": m["label"],
                "model_id": m["id"],
                "status": status,
                "total_ms": round(res["total_ms"], 1) if res["total_ms"] is not None else None,
                "first_byte_ms": round(res["first_byte_ms"], 1) if res["first_byte_ms"] is not None else None,
                "exit_code": res["exit_code"],
                "out_chars": len(res["stdout"]),
                "error": error,
            }
            probe["id"] = store.add_probe(probe)
            results.append(probe)
            log.info("%s %-12s %-10s %s ms", run["run_id"], m["label"], status, probe["total_ms"])
        finished = utc_now()
        store.finish_run(run["run_id"], iso(finished))
        store.prune(int(cfg["retention_days"]))
        manifest = write_manifest(cfg, run, iso(finished), results)
        return manifest


def write_manifest(cfg: dict, run: dict, finished_at: str, results: list[dict]) -> dict:
    ok = sum(1 for r in results if r["status"] == "ok")
    manifest = {
        "run_id": run["run_id"],
        "component": COMPONENT,
        "tool_version": run["tool_version"],
        "trigger": run["trigger"],
        "host": run["host"],
        "started_at": run["started_at"],
        "finished_at": finished_at,
        "cli": {"name": "vero", "version": run["cli_version"]},
        "prompt_sha256": run["prompt_sha256"],
        "models": [{"label": m["label"], "id": m["id"]} for m in cfg["models"]],
        "results": [{k: r[k] for k in ("model", "status", "total_ms", "first_byte_ms", "exit_code", "error")}
                    for r in results],
        "totals": {"probes": len(results), "ok": ok, "failed": len(results) - ok},
        "availability_percent": round(ok / len(results) * 100, 2) if results else None,
    }
    d = Path(cfg["data_dir"]) / "runs" / run["started_at"][:7]
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{run['run_id']}.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
