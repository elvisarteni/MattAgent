# Architecture: vero-availability-monitor

## Context
Runs on one Windows laptop (or Linux/macOS). Talks only to the local Vero CLI and, optionally, to Vero Chat
(`https://verostudio.sw.nxp.com/mcp`). Status page on `http://127.0.0.1:8766`.

## Components (dependencies point down only)
```
interfaces   cli.py (commands)   server.py (HTTP, SSE)   scheduler.py (timer, Task Scheduler, cron)
                 |                     |                        |
application  runner.py (lock, run, store, manifest)      report.py (status payload)
                 |                                              |
adapters     checks/process.py  checks/vero_cli.py  checks/vero_chat.py  store.py (SQLite)
                 |
domain       domain.py: Status, Check, CheckResult, RunResult, overall_status, availability_percent,
             incidents, timeline, current_since  (pure, no I/O)
config       config.py: typed, validated, frozen dataclasses
```

## Data flow
trigger -> `runner.run_once` -> lock `data/run.lock` -> `checks.run_all` (cli -> chat -> task; task skipped if cli down)
-> `domain.overall_status` -> `store.save` (runs + checks) -> prune -> manifest `data/runs/<YYYY-MM>/<run_id>.json`
-> `/api/status` + `/api/stream` -> status page.

## Status rules (domain.py)
- check: up / degraded / down. Task degraded = slower than `thresholds_s.task_slow` or answer without `expect`.
- run: DOWN if the primary check is down (task if enabled, else cli); DEGRADED if any other check is down or any is degraded; else UP.
- availability = runs not DOWN / runs. Incident = consecutive non-UP runs (outage, or degradation of 2+ runs).

## Interfaces
- CLI: `vam configure|init|doctor|check|serve|install|uninstall|status|open|export|report`
- HTTP: `GET /`, `GET /api/status?hours=1|6|24|168|720`, `GET /api/stream` (SSE: run, state), `POST /api/check`,
  `GET /api/export.csv`, `GET /api/health`. Host and Origin checked.
- Vero CLI: `vero version`; `vero task --json -m {model} -t {timeout} -c {workdir} {prompt}` (configurable).
- Vero Chat: JSON-RPC `initialize`, `Authorization: Bearer $VERO_CHAT_TOKEN`.

## Dependencies
Python 3.8+ stdlib. Vero CLI 2.3.x (version recorded per run). Model from `modelInfo` recorded per run.
