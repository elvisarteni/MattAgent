# Agents: vero-latency-monitor

## Role
Measures Vero CLI response latency. It is not an AI agent itself: it calls the Vero CLI with one fixed prompt and times the call.

## Rules
- The probe prompt stays minimal and neutral ("Reply with OK") so it is the cheapest call and within Vero guardrails.
- Never store the model answer. Store only status, timings, exit code, answer length and a truncated error.
- No secrets in `config/monitor.json` or in Git. Credentials stay in the Vero CLI's own login or in environment variables.
- Every probe belongs to a run with a run_id `<YYYYMMDD-HHMM>-vero-latency` and a JSON run manifest.
- Run outputs (`data/`, `reports/`) are never committed.

## Tools allowed
Python 3.8+ standard library only (ADR-001). The Vero CLI as configured.

## For coding agents
- Code lives in `src/vero_latency/`; the dashboard is one file, `src/vero_latency/web/dashboard.html`.
- Run `python -m unittest discover -s tests -t .` before every commit. Tests use `scripts/fake_vero.py`, never the real CLI.
- Commit and PR title: `ASPF-1578: <imperative summary>`.
