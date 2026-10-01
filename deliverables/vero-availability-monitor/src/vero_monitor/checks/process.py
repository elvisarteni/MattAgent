"""Run one external process with a hard timeout. Kills the whole process tree on timeout
(vero.cmd -> node -> ...), never opens a console window on Windows."""

from __future__ import annotations

import contextlib
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from typing import List, Mapping, Optional, Sequence

IS_WINDOWS = os.name == "nt"
NO_WINDOW = 0x08000000 if IS_WINDOWS else 0  # CREATE_NO_WINDOW


@dataclass(frozen=True)
class ProcessResult:
    started: bool
    exit_code: Optional[int]
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool


def resolve(program: str) -> Optional[str]:
    """Full path of the program, or None. Finds vero.cmd / vero.exe for 'vero' on Windows."""
    return shutil.which(program)


def kill_tree(proc: subprocess.Popen[bytes]) -> None:
    """Kill the process and everything it started (vero.cmd -> node -> ...)."""
    with contextlib.suppress(OSError):
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, creationflags=NO_WINDOW, check=False
            )
        else:
            os.killpg(proc.pid, signal.SIGKILL)  # own process group: start_new_session=True
    with contextlib.suppress(OSError):
        proc.kill()


def run(
    args: Sequence[str], timeout_s: float, env: Optional[Mapping[str, str]] = None, cwd: Optional[str] = None
) -> ProcessResult:
    full_env = dict(os.environ)
    full_env.update(env or {})
    t0 = time.perf_counter()
    try:
        proc = subprocess.Popen(
            list(args),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=full_env,
            cwd=cwd,
            creationflags=NO_WINDOW,
            start_new_session=not IS_WINDOWS,
        )
    except OSError as e:
        return ProcessResult(False, None, "", f"cannot start {args[0]!r}: {e}", 0.0, False)

    out: List[bytes] = []
    err: List[bytes] = []
    stdout, stderr = proc.stdout, proc.stderr
    if stdout is None or stderr is None:  # cannot happen with PIPE; keeps the types honest
        kill_tree(proc)
        return ProcessResult(False, None, "", "no output pipes", 0.0, False)
    readers = [
        threading.Thread(target=lambda: out.append(stdout.read()), daemon=True),
        threading.Thread(target=lambda: err.append(stderr.read()), daemon=True),
    ]
    for r in readers:
        r.start()
    timed_out = False
    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_tree(proc)
        proc.wait()
    duration = (time.perf_counter() - t0) * 1000
    for r in readers:
        r.join(timeout=5)
    stdout.close()  # release OS handles (long-running dashboard on Windows)
    stderr.close()
    return ProcessResult(
        started=True,
        exit_code=proc.returncode,
        stdout=b"".join(out).decode("utf-8", "replace"),
        stderr=b"".join(err).decode("utf-8", "replace"),
        duration_ms=duration,
        timed_out=timed_out,
    )
