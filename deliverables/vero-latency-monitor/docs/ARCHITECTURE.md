# Architecture: vero-latency-monitor

## Context
Runs on one Windows laptop (or any machine with Python 3.8+). Calls the Vero CLI installed on that machine. Fits the platform's Report stage: it produces run manifests in the same shape as automation-code.

## Components
| Module | Job |
|--------|-----|
| `config.py` | loads `config/monitor.json` (non-secret) |
| `probe.py` | builds the command, times one call (total and first byte), classifies status, writes the run manifest |
| `store.py` | SQLite `data/latency.db`: tables `runs`, `probes` |
| `stats.py` | percentiles, availability, time buckets |
| `scheduler.py` | in-process loop; Windows Task Scheduler / cron install |
| `server.py` | local HTTP server: dashboard, JSON API, SSE live stream |
| `web/dashboard.html` | single-file dashboard, no external libraries |

## Data flow
Trigger (task / loop / button) -> `run_cycle` -> Vero CLI per model -> `probes` rows + `data/runs/<YYYY-MM>/<run_id>.json` -> `/api/dashboard` and `/api/stream` -> dashboard.

## Interfaces
- CLI: `python vlm.py init|doctor|probe|serve|schedule|export|report`
- HTTP (127.0.0.1:8765): `GET /`, `GET /api/dashboard?hours=&model=`, `GET /api/stream` (SSE), `POST /api/probe`, `GET /api/export.csv`, `GET /api/health`
- Run manifest: run_id, component, tool_version, trigger, host, started/finished, cli version, prompt_sha256, models, results, totals, availability_percent

## Dependencies
Python 3.8+ standard library. Vero CLI (version recorded per run). Model id per probe recorded.
