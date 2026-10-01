"""SQLite persistence: <data_dir>/availability.db. One row per run, one row per check."""

from __future__ import annotations

import contextlib
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .domain import Point, RunResult, Status

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id       TEXT PRIMARY KEY,
    started_at   TEXT NOT NULL,
    epoch        REAL NOT NULL,
    trigger      TEXT NOT NULL,
    overall      TEXT NOT NULL,
    reason       TEXT,
    host         TEXT,
    tool_version TEXT
);
CREATE TABLE IF NOT EXISTS checks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id       TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    epoch        REAL NOT NULL,
    check_name   TEXT NOT NULL,
    status       TEXT NOT NULL,
    duration_ms  REAL,
    detail       TEXT,
    version      TEXT,
    provider_id  TEXT,
    model_id     TEXT
);
CREATE INDEX IF NOT EXISTS ix_runs_epoch ON runs(epoch);
CREATE INDEX IF NOT EXISTS ix_checks_run ON checks(run_id);
"""


def reason_of(run: RunResult) -> str:
    """The detail of the worst check: what the dashboard shows as the reason."""
    bad = [c for c in run.checks if c.status in (Status.DOWN, Status.DEGRADED)]
    bad.sort(key=lambda c: -c.status.rank)
    return f"{bad[0].check.value}: {bad[0].detail}" if bad else ""


class Store:
    def __init__(self, data_dir: Path):
        self.path = Path(data_dir) / "availability.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.execute("PRAGMA journal_mode=WAL")
            c.executescript(SCHEMA)

    @contextlib.contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        c = sqlite3.connect(str(self.path), timeout=30)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON")
        try:
            with c:
                yield c
        finally:
            c.close()

    def save(self, run: RunResult, host: str, tool_version: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO runs VALUES (?,?,?,?,?,?,?,?)",
                (run.run_id, run.started_at, run.epoch, run.trigger, run.overall.value, reason_of(run), host, tool_version),
            )
            c.executemany(
                "INSERT INTO checks(run_id, epoch, check_name, status, duration_ms, detail, version, provider_id, model_id)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                [
                    (
                        run.run_id,
                        run.epoch,
                        r.check.value,
                        r.status.value,
                        r.duration_ms,
                        r.detail,
                        r.version,
                        r.provider_id,
                        r.model_id,
                    )
                    for r in run.checks
                ],
            )

    def run_exists(self, run_id: str) -> bool:
        with self._conn() as c:
            return c.execute("SELECT 1 FROM runs WHERE run_id=?", (run_id,)).fetchone() is not None

    def prune(self, retention_days: int, now: Optional[float] = None) -> int:
        cutoff = (now or time.time()) - retention_days * 86400
        with self._conn() as c:
            return c.execute("DELETE FROM runs WHERE epoch < ?", (cutoff,)).rowcount

    def points(self, since: float) -> List[Point]:
        with self._conn() as c:
            rows = c.execute("SELECT epoch, overall, reason FROM runs WHERE epoch >= ? ORDER BY epoch", (since,))
            return [Point(r["epoch"], Status(r["overall"]), r["reason"] or "") for r in rows]

    def runs(
        self, since: float = 0, limit: Optional[int] = None, newest_first: bool = True, after_epoch: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        q = "SELECT * FROM runs WHERE epoch >= ?"
        args: List[Any] = [since]
        if after_epoch is not None:
            q += " AND epoch > ?"
            args.append(after_epoch)
        q += " ORDER BY epoch DESC" if newest_first else " ORDER BY epoch"
        if limit:
            q += " LIMIT ?"
            args.append(limit)
        with self._conn() as c:
            runs = [dict(r) for r in c.execute(q, args)]
            for r in runs:
                r["checks"] = [
                    dict(x)
                    for x in c.execute(
                        "SELECT check_name, status, duration_ms, detail, version, provider_id, model_id"
                        " FROM checks WHERE run_id=? ORDER BY id",
                        (r["run_id"],),
                    )
                ]
        return runs

    def latest_check(self, name: str) -> Optional[Dict[str, Any]]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM checks WHERE check_name=? ORDER BY epoch DESC, id DESC LIMIT 1", (name,)).fetchone()
            return dict(r) if r else None

    def last_epoch(self) -> float:
        with self._conn() as c:
            return float(c.execute("SELECT COALESCE(MAX(epoch), 0) FROM runs").fetchone()[0])

    def count(self) -> int:
        with self._conn() as c:
            return int(c.execute("SELECT COUNT(*) FROM runs").fetchone()[0])

    def csv_rows(self, since: float = 0) -> List[List[Any]]:
        with self._conn() as c:
            q = (
                "SELECT r.run_id, r.started_at, r.trigger, r.overall, k.check_name, k.status, k.duration_ms,"
                " k.detail, k.version, k.provider_id, k.model_id FROM runs r JOIN checks k USING(run_id)"
                " WHERE r.epoch >= ? ORDER BY r.epoch, k.id"
            )
            return [list(r) for r in c.execute(q, (since,))]


CSV_HEADER = [
    "run_id",
    "started_at",
    "trigger",
    "overall",
    "check",
    "status",
    "duration_ms",
    "detail",
    "version",
    "provider_id",
    "model_id",
]
