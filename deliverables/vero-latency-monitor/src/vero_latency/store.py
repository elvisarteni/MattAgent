"""SQLite storage for probe results. One file: <data_dir>/latency.db."""
from __future__ import annotations

import contextlib
import csv
import io
import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id        TEXT PRIMARY KEY,
    started_at    TEXT NOT NULL,
    finished_at   TEXT,
    trigger       TEXT NOT NULL,
    host          TEXT,
    tool_version  TEXT,
    cli_version   TEXT,
    prompt_sha256 TEXT
);
CREATE TABLE IF NOT EXISTS probes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        TEXT NOT NULL REFERENCES runs(run_id),
    ts            TEXT NOT NULL,
    epoch         REAL NOT NULL,
    model         TEXT NOT NULL,
    model_id      TEXT,
    status        TEXT NOT NULL,
    total_ms      REAL,
    first_byte_ms REAL,
    exit_code     INTEGER,
    out_chars     INTEGER,
    error         TEXT
);
CREATE INDEX IF NOT EXISTS ix_probes_epoch ON probes(epoch);
CREATE INDEX IF NOT EXISTS ix_probes_model ON probes(model, epoch);
"""

PROBE_COLS = ["id", "run_id", "ts", "epoch", "model", "model_id", "status",
              "total_ms", "first_byte_ms", "exit_code", "out_chars", "error"]


class Store:
    def __init__(self, data_dir: str | Path):
        self.path = Path(data_dir) / "latency.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.execute("PRAGMA journal_mode=WAL")
            c.executescript(SCHEMA)

    @contextlib.contextmanager
    def _conn(self):
        """Commit on success, roll back on error, always close (no leaked file handles on Windows)."""
        c = sqlite3.connect(self.path, timeout=30)
        c.row_factory = sqlite3.Row
        try:
            with c:
                yield c
        finally:
            c.close()

    # writes -------------------------------------------------------------
    def run_exists(self, run_id: str) -> bool:
        with self._conn() as c:
            return c.execute("SELECT 1 FROM runs WHERE run_id=?", (run_id,)).fetchone() is not None

    def start_run(self, run: dict) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO runs(run_id, started_at, trigger, host, tool_version, cli_version, prompt_sha256)"
                " VALUES(:run_id, :started_at, :trigger, :host, :tool_version, :cli_version, :prompt_sha256)",
                run,
            )

    def finish_run(self, run_id: str, finished_at: str) -> None:
        with self._conn() as c:
            c.execute("UPDATE runs SET finished_at=? WHERE run_id=?", (finished_at, run_id))

    def add_probe(self, p: dict) -> int:
        cols = [k for k in PROBE_COLS if k != "id"]
        with self._conn() as c:
            cur = c.execute(
                f"INSERT INTO probes({', '.join(cols)}) VALUES({', '.join(':' + k for k in cols)})",
                {k: p.get(k) for k in cols},
            )
            return cur.lastrowid

    def prune(self, retention_days: int) -> int:
        cutoff = time.time() - retention_days * 86400
        with self._conn() as c:
            n = c.execute("DELETE FROM probes WHERE epoch < ?", (cutoff,)).rowcount
            c.execute("DELETE FROM runs WHERE finished_at IS NOT NULL"
                      " AND run_id NOT IN (SELECT DISTINCT run_id FROM probes)")
            return n

    # reads --------------------------------------------------------------
    def probes(self, since_epoch: float = 0, model: str | None = None,
               after_id: int = 0, limit: int | None = None, newest_first: bool = False) -> list[dict]:
        q = "SELECT * FROM probes WHERE epoch >= ? AND id > ?"
        args: list = [since_epoch, after_id]
        if model:
            q += " AND model = ?"
            args.append(model)
        q += " ORDER BY epoch DESC, id DESC" if newest_first else " ORDER BY epoch, id"
        if limit:
            q += " LIMIT ?"
            args.append(limit)
        with self._conn() as c:
            return [dict(r) for r in c.execute(q, args)]

    def last_run(self) -> dict | None:
        with self._conn() as c:
            r = c.execute("SELECT * FROM runs ORDER BY started_at DESC LIMIT 1").fetchone()
            return dict(r) if r else None

    def max_probe_id(self) -> int:
        with self._conn() as c:
            return c.execute("SELECT COALESCE(MAX(id), 0) FROM probes").fetchone()[0]

    def to_csv(self, since_epoch: float = 0, model: str | None = None) -> str:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(PROBE_COLS)
        for r in self.probes(since_epoch, model):
            w.writerow([r[k] for k in PROBE_COLS])
        return buf.getvalue()
