# Changelog

## 4.0.0
Rewritten as a simple program with a dashboard (feedback on 3.0: too many command windows and steps).
- Double-click `Vero Status.pyw`: no console, no setup, no Task Scheduler. A second double-click just opens the dashboard.
- The dashboard shows whether Vero is available and **which model Vero uses**: the configured model (`vero config`)
  and the model asked in the last check (`modelInfo`). Also the Vero version, response time, 24 h availability and the last checks.
- Check now, Settings (interval: off / 5 / 15 / 30 / 60 min, check model, timeout, Vero location) and Quit on the page.
- Keeps the safe parts of 3.0: `--json` stream with `completion_result` only, no `--yolo`, empty working folder,
  the whole process tree killed on timeout, Host and Origin checks, nothing secret stored. Errors at start show a Windows message box.
- 30 tests (fake Vero), ruff, mypy strict for Linux and Windows, checked in a real browser.

## 3.0.0 and older
Vero Availability Monitor (3.0) and Vero Latency Monitor (0.x): command-line tools with installer scripts. Superseded.
