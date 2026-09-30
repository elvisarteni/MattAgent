# Changelog

## Unreleased

## 0.2.0
Review fixes (details: guide, section 16 Review log):
- Config: accept Notepad "UTF-8 with BOM"; full validation with clear errors; env vars in data_dir.
- Scheduler: Task Scheduler tasks registered from XML (run on battery, catch up after sleep, no overlap,
  no /TR length limit); dashboard task at logon; desktop shortcut; `install`, `uninstall`, `status`, `open`.
- Probe: timeout kills the whole process tree; stale-lock aware "running" state; exit code 0 for scheduled runs.
- Server: Host and Origin checks; safe query parsing; errors logged; browser opened only after bind;
  detects an already running dashboard.
- Dashboard: data loads before the live stream; chart clamped to the plot; report times relative to generation.
- Setup: guided `configure`, `setup.bat` end to end, `setup_demo.bat` with separate `data-demo/`.
- Ops: rotating log, crash logging under pythonw, SQLite connections closed, stable zip folder name.

## 0.1.0
- First version (ASPF-1578): cheapest-prompt probe of the Vero CLI, SQLite store, run manifests,
  live dashboard (SSE), built-in scheduler, Windows Task Scheduler / cron trigger, CSV export,
  static HTML report, HTML guide.
