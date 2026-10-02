# VERO_CONTEXT: Vero Status 4.2.0

> **For the AI reading this:** this file describes the whole program. Read a file before changing it, and keep the rules at the end.

## What it is

A small program for one laptop. When you double-click `Vero Status.pyw`, it opens a dashboard in the browser at `http://127.0.0.1:8767`. The dashboard shows:

- whether **Vero is available** (Vero CLI 2.3.x);
- **which model Vero uses**: the configured model from `vero config`, and the model the last check used (`modelInfo` in the `--json` stream);
- the Vero version, the response time, availability over 24 h, and the last 48 checks;
- **Vero open now**: the model in use in your own open Vero CLI or VS Code session;
- **Your Vero sessions: response time**: median and p95 per hour, the 24 h median, and the last 40 requests;
- **Recent activity**: the last 10 checks (time, result, model, answer time, trigger);
- buttons for Check now, Settings and Quit.

**Team server** (4.2): `python vero_status_server.py [--port N] [--host H]` serves the same page on the network for
everyone, with no login. Viewers see status, models, history and Recent activity; their Check now is limited to once per
5 minutes (`server.COOLDOWN_S`). Settings need the admin key (`?admin=<key>` in the URL, sent as the `X-Admin-Key` header,
stored in `data/admin_key.txt`, compared with `hmac.compare_digest`). No Quit endpoint, no personal session panels,
and the Vero path is hidden from viewers.

It uses only the Python 3.8+ standard library. It opens no console window (`pythonw`), and every child process starts with `CREATE_NO_WINDOW`.

The Jira story is ASPF-1578, for the Quality AI Automation team at NXP. Version 4.0.0 replaces the 3.0 "Vero Availability Monitor", which was command-line based.

## Files

```
Vero Status.pyw          double-click entry: adds the folder to sys.path, calls vero_status.app.run()
vero_status_server.py    team server entry: calls vero_status.app.serve_team() (admin key, binds 0.0.0.0)
vero_status/
  __init__.py            __version__ = "4.2.0", APP_ID = "vero-status"
  app.py                 single instance (GET /api/health), logging to data/vero-status.log, opens the browser,
                         shows a Windows message box on errors (no console)
  vero.py                find_vero, run (no window, kills the process tree on timeout), and pure parsers:
                         parse_version, parse_config, parse_task_stream, task_args, clean (masks credentials)
  sessions.py            your own Vero sessions: parse_ui_messages (pure: request latency = first event after
                         api_req_started; model from modelInfo), Scanner (finds tasks/*/ui_messages.json for CLI
                         and VS Code, cached by mtime, every 15 s), is_interactive_vero / process_command_lines
                         (a vero / vero.cmd / node-with-vero-package process = an open CLI), summarize
  monitor.py             perform_check(settings, workdir, run) -> record; Monitor: timer thread, check_now,
                         history (data/history.json, last 500), update_settings, state() for the page
  settings.py            Settings (frozen dataclass), validation, load/save of data/settings.json
  server.py              GET / , /api/state, /api/health; POST /api/check, /api/settings, /api/quit (local only).
                         Local: 127.0.0.1, Host and Origin checked. Server mode: any Host, POST Origin checked,
                         settings need the admin key, viewer Check now cooldown (429).
  web/index.html         the dashboard (one file, vanilla JS, light and dark, polls /api/state)
scripts/fake_vero.py     stand-in Vero: version, config, task --json (FAKE_VERO_MODE ok|down|auth|hang|nocompletion|refuse)
scripts/fake_session.py  writes a realistic session log into a folder (demo and tests; never your real ~/.vero)
scripts/vero, vero.cmd   launch the fake Vero (point "Vero CLI location" at one of these for a demo)
scripts/build_source_pdf.py   writes the source as a PDF for rebuilding (developer tool, needs reportlab)
tests/                   unittest; never calls the real Vero
```

## One check (`monitor.perform_check`)

1. `find_vero(settings.vero_path)` looks for the Vero CLI in this order: the configured path, `vero` on the PATH (`vero.cmd` on Windows), then `%APPDATA%\npm\vero.cmd`. If nothing is found, the result is "not available" with the reason "not found".
2. `vero version`: if this fails, the result is "not available".
3. `vero config` reads the settings `actModeApiModelId`, `actModeApiProvider` and `awsRegion`, given either as `key : value` lines or as JSON. If this step fails, the configured model is simply unknown; it does not affect the status.
4. `vero task --json -t <timeout> -c data/sandbox [-m <check_model>] "Reply with exactly: OK"`, killed at timeout + 30 s.
   - **Available** if and only if a `completion_result` event arrives. A different answer still counts as available, with a note.
   - `partial` events are ignored. `api_req_started`, which holds the full prompt, is never kept.
   - The record holds `time`, `available`, `reason`, `seconds` (only when there is an answer), `asked_model`, `provider`, `vero_version`, `configured` {`model`, `provider`, `region`} and `trigger` (start, auto or manual).

## Settings

Stored in `data/settings.json` and editable on the page:

| Setting | Default | Allowed values |
|---|---|---|
| `vero_path` | `""` (find it automatically) | any path |
| `check_model` | Haiku 4.5 | a model id, or `""` to use Vero's own model |
| `interval_minutes` | 15 | 0 (off), 5, 15, 30, 60 |
| `timeout_seconds` | 120 | 30–600 |
| `port` | 8767 | 1024–65535; change it in the file only |
| `track_sessions` | true | show your own sessions' model and response time |

A broken settings file falls back to the defaults.

## Quality gates

```
python -m unittest discover -s tests -t .      (49 tests, Python 3.8–3.13)
uvx ruff check . && uvx ruff format --check .
uvx mypy && uvx mypy --platform win32          (strict)
```

## Rules

1. Keep it simple for the user: double-click, a dashboard, no command windows, no installer.
2. Standard library only. No CDN and no external scripts in the page.
3. Never pass `--yolo`. Run the task in the empty `data/sandbox` folder. On timeout, kill the whole process tree.
4. Store no answers, no secrets and no `api_req_started` content. Mask credentials in error text.
   From the user's task logs, read only `ts`, event kinds, `modelInfo` and token counts. Only read those files, never change them.
   Exclude our own probe tasks, by task id and by prompt.
5. Local mode binds to 127.0.0.1 with Host and Origin checks. Server mode is opt-in (`vero_status_server.py`): keep the
   Origin check on POSTs, the admin key for settings, the viewer cooldown, and never expose paths or personal sessions.
6. Tests use the fake Vero only.
7. Commit messages and PR titles have the form `ASPF-1578: <summary>`. Update the CHANGELOG and this file when behaviour changes.
