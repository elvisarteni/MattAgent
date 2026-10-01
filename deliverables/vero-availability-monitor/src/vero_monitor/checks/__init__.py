"""Check registry: which checks run, in which order. Cheap checks first."""

from __future__ import annotations

import logging
import time
from typing import Callable, List, Tuple

from ..config import Config
from ..domain import Check, CheckResult, Status
from .vero_chat import check_chat
from .vero_cli import check_cli, check_task

log = logging.getLogger("vero_monitor")

CheckFn = Callable[[Config], CheckResult]


def enabled(cfg: Config) -> List[Tuple[Check, CheckFn]]:
    plan: List[Tuple[Check, CheckFn]] = []
    if cfg.check_cli:
        plan.append((Check.CLI, check_cli))
    if cfg.check_chat:
        plan.append((Check.CHAT, check_chat))
    if cfg.check_task:
        plan.append((Check.TASK, check_task))
    return plan


def run_all(cfg: Config) -> List[CheckResult]:
    results: List[CheckResult] = []
    cli_down = False
    for name, fn in enabled(cfg):
        if name is Check.TASK and cli_down:
            # no point spending a minute on a task when the CLI cannot even start
            results.append(CheckResult(Check.TASK, Status.DOWN, None, "skipped: Vero CLI not available"))
            continue
        t0 = time.perf_counter()
        try:
            res = fn(cfg)
        except Exception as e:  # a bug in one check must not hide the others
            log.exception("check %s crashed", name.value)
            res = CheckResult(name, Status.DOWN, (time.perf_counter() - t0) * 1000, f"monitor error: {type(e).__name__}")
        results.append(res)
        cli_down = cli_down or (name is Check.CLI and res.status is Status.DOWN)
    return results
