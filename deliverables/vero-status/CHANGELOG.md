# Changelog

## 4.3.0 (Linux VM)
- `scripts/install_vm.sh`: runs Vero Status in the background on a Linux VM and starts it with the machine
  (systemd user service, else crontab @reboot); `personal` (default) or `team`, plus `status` and `uninstall`. No sudo.
  Copies PATH and proxy settings for the service into `data/service.env` (owner-only), never AWS keys.
- Vero CLI found without PATH: nvm (newest node first), `~/.npm-global/bin`, `~/.local/bin`, `/usr/local/bin`.
  The program's folder is put first on the child PATH so `#!/usr/bin/env node` finds nvm's node.
- Headless: no browser is started without a desktop; the URL is printed and logged instead.
- Port forwarding works: local mode accepts 127.0.0.1 / localhost on any port (VS Code may forward 8767 as 8768).
  Before, a different forwarded port got 403.
- Shared VM: `data/` is owner-only (0700, admin key 0600); only your own processes count as an open Vero CLI;
  under systemd/cron the admin link goes to the private log only, not the system journal.
- VS Code Remote-SSH session logs (`~/.vscode-server/data/User/globalStorage`) are read.
- SIGTERM (systemd stop, kill) stops cleanly. The page footer shows the machine the checks run on.

## 4.2.0
- **Team server**: `python vero_status_server.py` serves one shared page on the network. No login or registration:
  anyone with the link sees availability, models, 24 h availability and the new **Recent activity** table.
- Viewers can trigger **Check now** at most once every 5 minutes; settings need the admin link
  (`?admin=<key>`, key in `data/admin_key.txt`, compared in constant time, removed from the address bar).
- On the server there is no Quit, the personal panels are off, and the Vero path is hidden from viewers.
  Cross-site POSTs are still rejected.
- New **Recent activity** panel (also locally): last 10 checks with result, model, answer time and trigger.

## 4.1.0
- New panel **Vero open now**: when a Vero CLI is running, or a Vero CLI / VS Code session was active in the last
  10 minutes, it shows the model in use right now (idle CLI: Vero's configured model). "Waiting for the model for N s"
  while a request runs.
- New panel **Your Vero sessions: response time**: for every model request in your own sessions (CLI and VS Code),
  the time until the model started answering, read from Vero's own task logs (`ui_messages.json`). Median and p95 for
  the last hour, median for 24 h, and the last 40 requests as bars with details on hover.
- Privacy: only timestamps, event kinds, model names and token counts are read; prompts and answers never. Files are
  only read. The dashboard's own test questions are excluded (by task id and prompt). Setting to switch it off.
- Process detection is structural (vero / vero.cmd / node running a `vero` package), so Vero Status itself, admin
  commands (`vero version`, `config`, …) and its own checks are never mistaken for an open session.

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
