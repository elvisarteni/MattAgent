"""Domain model and pure rules. No I/O here: everything is unit-testable.

Vocabulary
- check:    one probe of one component (cli, task, chat) -> CheckResult
- run:      all enabled checks at one moment            -> RunResult with an overall Status
- incident: consecutive runs whose overall status is not UP
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence


class Status(str, Enum):
    UP = "up"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"  # no data

    @property
    def rank(self) -> int:
        return {"unknown": 0, "up": 1, "degraded": 2, "down": 3}[self.value]


def worst(statuses: Iterable[Status]) -> Status:
    result = Status.UNKNOWN
    for s in statuses:
        if s.rank > result.rank:
            result = s
    return result


class Check(str, Enum):
    CLI = "cli"  # `vero version`: installed and starts (free, seconds)
    TASK = "task"  # `vero task --json`: end-to-end answer through the model (2 API calls, ~1 min)
    CHAT = "chat"  # Vero Chat MCP `initialize` handshake (free, no model call)


@dataclass(frozen=True)
class CheckResult:
    check: Check
    status: Status
    duration_ms: float | None
    detail: str = ""
    version: str | None = None  # cli version or chat server version
    provider_id: str | None = None  # from task modelInfo (never assumed from config)
    model_id: str | None = None


@dataclass(frozen=True)
class RunResult:
    run_id: str
    started_at: str
    epoch: float
    trigger: str
    checks: tuple[CheckResult, ...]
    overall: Status = field(default=Status.UNKNOWN)


def overall_status(results: Sequence[CheckResult]) -> Status:
    """DOWN if the primary check is down (task when enabled, else cli).
    DEGRADED if any other check is down or any check is degraded. UP otherwise."""
    if not results:
        return Status.UNKNOWN
    by = {r.check: r for r in results}
    primary = by.get(Check.TASK) or by.get(Check.CLI) or results[0]
    if primary.status is Status.DOWN:
        return Status.DOWN
    if any(r.status in (Status.DOWN, Status.DEGRADED) for r in results):
        return Status.DEGRADED
    return Status.UP


def availability_percent(statuses: Sequence[Status]) -> float | None:
    """Share of runs where Vero answered (UP or DEGRADED)."""
    known = [s for s in statuses if s is not Status.UNKNOWN]
    if not known:
        return None
    return round(sum(1 for s in known if s is not Status.DOWN) / len(known) * 100, 2)


@dataclass(frozen=True)
class Point:
    """One run on the time axis (what the incident and timeline rules need)."""

    epoch: float
    status: Status
    reason: str = ""


@dataclass(frozen=True)
class Incident:
    start: float
    end: float | None  # None = ongoing
    worst: Status
    runs: int
    reason: str

    def duration_s(self, now: float) -> float:
        return (self.end if self.end is not None else now) - self.start


def incidents(points: Sequence[Point], min_degraded_runs: int = 2) -> list[Incident]:
    """Group consecutive non-UP runs; the incident ends at the first UP run after it.
    Any outage (DOWN) is an incident; a degradation only when it lasts min_degraded_runs runs,
    so one slow answer does not flood the list (it still shows on the timeline)."""
    out: list[Incident] = []
    cur: list[Point] = []
    for p in sorted(points, key=lambda x: x.epoch):
        if p.status in (Status.DOWN, Status.DEGRADED):
            cur.append(p)
            continue
        if cur and p.status is Status.UP:
            out.append(_incident(cur, end=p.epoch))
            cur = []
    if cur:
        out.append(_incident(cur, end=None))
    return [i for i in out if i.worst is Status.DOWN or i.runs >= min_degraded_runs]


def _incident(group: list[Point], end: float | None) -> Incident:
    w = worst(p.status for p in group)
    reason = next((p.reason for p in group if p.status is w and p.reason), "")
    return Incident(start=group[0].epoch, end=end, worst=w, runs=len(group), reason=reason)


def timeline(points: Sequence[Point], start: float, end: float, bins: int) -> list[tuple[float, Status, int]]:
    """Split [start, end) into equal bins; each bin shows the worst status in it (UNKNOWN if empty)."""
    if bins <= 0 or end <= start:
        return []
    width = (end - start) / bins
    acc: list[list[Status]] = [[] for _ in range(bins)]
    for p in points:
        if start <= p.epoch < end:
            acc[min(int((p.epoch - start) / width), bins - 1)].append(p.status)
    return [(start + i * width, worst(a), len(a)) for i, a in enumerate(acc)]


def current_since(points: Sequence[Point]) -> tuple[Status, float | None]:
    """Current overall status and since when it has been continuously so."""
    pts = sorted(points, key=lambda x: x.epoch)
    if not pts:
        return Status.UNKNOWN, None
    status = pts[-1].status
    since = pts[-1].epoch
    for p in reversed(pts):
        if p.status is not status:
            break
        since = p.epoch
    return status, since
