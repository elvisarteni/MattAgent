# Agents: vero-availability-monitor

## Role
Monitors whether Vero is available. It is not an AI agent itself: it starts the Vero CLI with one fixed, harmless prompt and checks that an answer comes back.

## Rules
- Never pass `--yolo`; the task runs in an empty sandbox folder (`-c data/sandbox`). See ADR-003.
- Only `completion_result` counts as an answer. Never store or log the event stream; `api_req_started` contains the full upstream prompt.
- Never store model answers, tokens or `vero.env` values. Error details are one line, max 200 chars, with credential-like text masked.
- The Vero Chat token is read from an environment variable at run time only (ADR-004).
- Every run has a run_id `<YYYYMMDD-HHMM>-vero-availability` and a JSON manifest that records the model reported by Vero (`modelInfo`), not the configured one.

## Tools allowed
Python 3.8+ standard library (ADR-001). Vero CLI and Vero Chat as configured.

## For coding agents
- Layers: `domain.py` (pure) <- `checks/` (adapters) <- `runner.py`, `report.py` (application) <- `cli.py`, `server.py`, `scheduler.py` (interfaces). Do not import upwards.
- Before every commit: `uvx ruff check .`, `uvx ruff format --check .`, `uvx mypy`, `uvx mypy --platform win32`, `python -m unittest discover -s tests -t .`
- Tests use `scripts/fake_vero.py` and a local fake MCP server, never the real Vero.
- Commit and PR title: `ASPF-1578: <imperative summary>`.
