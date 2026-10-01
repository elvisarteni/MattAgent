# Changelog

## Unreleased

## 3.0.0
Rebuilt from scratch as an **availability** monitor (scope change from the 0.x latency monitor; ADR-002).
- Checks: `cli` (vero version), `task` (`vero task --json`, end-to-end, `completion_result` only), optional `chat`
  (Vero Chat MCP initialize handshake, no model call). Overall status per run: available / degraded / unavailable.
- Status page: current status and since when, components, availability 24 h / 7 d / 30 d, status timeline,
  incidents (outages, or degradation lasting 2+ checks), recent checks; live (SSE); CSV; self-contained snapshot.
- Uses the measured Vero CLI 2.3.x contract: `--json` event stream, pinned `-m`, `-t` timeout, `modelInfo` recorded.
  No `--yolo`; runs in an empty sandbox folder (ADR-003). Vero Chat token from an environment variable (ADR-004).
- Structure: pure domain layer, adapters, application services, interfaces; strict typing (mypy strict, Linux and
  Windows), ruff lint + format, 64 unit and integration tests on Python 3.8 to 3.13.
- Kept from 0.2: guided setup, Task Scheduler XML (laptop-safe), dashboard at logon, Host/Origin checks, lock file,
  stale-lock recovery, rotating log, run manifests, rebuild document for channels without archives.
- Coexists with the 0.x latency monitor: different port (8766), task names and data.
- Distribution as documents only: `..._Source.pdf` (numbered rows, visible space mark, SHA-256 verify script;
  rebuild verified byte-identical with pypdf and pdfplumber extraction) and the guide as PDF.
