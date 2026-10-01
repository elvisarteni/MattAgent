# Vero Availability Monitor 3.0.0: complete source for rebuild

**What this is.** The full source of the Vero Availability Monitor (Jira ASPF-1578), a local tool that checks
whether Vero (CLI, optionally Chat) is available and shows it on a status page. It is sent as a readable document because archives
and scripts cannot be attached. Nothing in it runs by itself. Read it before rebuilding.

- 59 files, all plain text, Python 3.8+ standard library only (no downloads, no pip).
- The HTML guide `VeroAvailabilityMonitor_Guide.html` is sent separately; put it in `docs/`.
- `VERO_CONTEXT.md` (included below) explains the architecture, contracts and rules.

---

## Instructions for the AI assistant (Vero CLI or other)

You are asked to recreate a project folder **exactly** from this document.

1. Create the folder `vero-availability-monitor/` in the location the user gives you (default: `C:\Tools\`).
2. For **every** section below that starts with `### FILE:`, create that file at that relative path,
   with the content of the code block that follows, **byte for byte**:
   - do not reformat, re-indent, translate, "improve", summarise or skip anything;
   - copy only the lines *between* the opening and closing fence (the fence is 4 or more backticks);
   - keep a trailing newline at the end of each file, exactly as in the block;
   - encoding UTF-8 without BOM.
3. Line endings: LF for every file, **except** those marked `CRLF` in the table (the `.bat` files and
   `START_HERE.txt`), which must use CRLF (Windows).
4. Create empty folders if needed: `data/` is **not** needed (the tool creates it).
5. Verify: save the Python block in the section *Verify the rebuild* as `verify_rebuild.py` next to this
   document (outside the project folder), then run
   `py verify_rebuild.py C:\Tools\vero-availability-monitor VeroAvailabilityMonitor_3.0.0_REBUILD.md`.
   It checks every file against its SHA-256 (computed on LF line endings) and fixes CRLF where needed.
   If it reports `DIFFERENT` or `MISSING`, recreate those files again from this document.
6. Then run the tests: `py -m unittest discover -s tests -t .` inside the folder. Expected: `OK` (64 tests, about 10 s).
7. Report the result to the user, then tell them to double-click `setup.bat` (see `START_HERE.txt`).

Do not run `setup.bat`, `install`, `doctor`, `check` or the real Vero CLI yourself unless the user asks.

---

## File list

| # | Path | Bytes | Line endings | SHA-256 (LF) |
|---|------|------:|:---:|---|
| 1 | `.ci/README.md` | 194 | LF | `84f4caf43cc1c411…` |
| 2 | `.gitattributes` | 134 | LF | `de5647982a8a835e…` |
| 3 | `.gitignore` | 209 | LF | `7756a240e02140de…` |
| 4 | `AGENTS.md` | 1423 | LF | `44800f1ef26c843a…` |
| 5 | `CHANGELOG.md` | 1325 | LF | `0cec48b50388071f…` |
| 6 | `CODEOWNERS` | 61 | LF | `695a47f89d8c8523…` |
| 7 | `CONTRIBUTING.md` | 502 | LF | `0309ecb367654505…` |
| 8 | `README.md` | 1983 | LF | `bbdf950dc7b1985c…` |
| 9 | `START_HERE.txt` | 1386 | CRLF | `a6edd8fc74e40964…` |
| 10 | `VERO_CONTEXT.md` | 9540 | LF | `e62427487f95e67c…` |
| 11 | `check_now.bat` | 154 | CRLF | `4bb4f1d8e7f19ffd…` |
| 12 | `config/monitor.example.json` | 878 | LF | `9e78c6a7a86a94f2…` |
| 13 | `docs/ARCHITECTURE.md` | 2230 | LF | `44ff1006d66b37de…` |
| 14 | `docs/DESIGN_SYSTEM.md` | 733 | LF | `fee93a3b440e1dab…` |
| 15 | `docs/PRD.md` | 1490 | LF | `884cfd889e035fe1…` |
| 16 | `docs/decisions/ADR-001_stdlib-only.md` | 388 | LF | `0e8be0912e36d2a9…` |
| 17 | `docs/decisions/ADR-002_availability-not-latency.md` | 570 | LF | `e1eba8243b818ec0…` |
| 18 | `docs/decisions/ADR-003_no-yolo-sandbox.md` | 623 | LF | `8ddb2cab993e4b50…` |
| 19 | `docs/decisions/ADR-004_vero-chat-handshake.md` | 635 | LF | `d2afb7b0b6032cf1…` |
| 20 | `pyproject.toml` | 1218 | LF | `536774c15d69d08e…` |
| 21 | `requirements.txt` | 106 | LF | `97a344f156562554…` |
| 22 | `scripts/_py.bat` | 580 | CRLF | `ee03008dcfe04647…` |
| 23 | `scripts/build_rebuild_md.py` | 6550 | LF | `d2630ee8d7d70ea5…` |
| 24 | `scripts/fake_vero.py` | 2865 | LF | `8ac166e8e0e0b845…` |
| 25 | `scripts/seed_demo_data.py` | 2302 | LF | `de8000130adac8dd…` |
| 26 | `setup.bat` | 957 | CRLF | `1676ff1a7460c049…` |
| 27 | `setup_demo.bat` | 372 | CRLF | `4881f05e4c2bfe05…` |
| 28 | `src/vero_monitor/__init__.py` | 145 | LF | `c77b5ab0da53e274…` |
| 29 | `src/vero_monitor/__main__.py` | 52 | LF | `13a1a5b340cdcfc1…` |
| 30 | `src/vero_monitor/checks/__init__.py` | 1593 | LF | `4e22f94dd92edc74…` |
| 31 | `src/vero_monitor/checks/process.py` | 3188 | LF | `bfeb6ac9be3fe90a…` |
| 32 | `src/vero_monitor/checks/vero_chat.py` | 3463 | LF | `f08bf1bf4287d3cc…` |
| 33 | `src/vero_monitor/checks/vero_cli.py` | 5375 | LF | `3ddceef9910b68e3…` |
| 34 | `src/vero_monitor/cli.py` | 13105 | LF | `4c4986cdc26cc381…` |
| 35 | `src/vero_monitor/config.py` | 7586 | LF | `e7d56144b413831f…` |
| 36 | `src/vero_monitor/domain.py` | 5100 | LF | `a6baf2d88794a41f…` |
| 37 | `src/vero_monitor/report.py` | 3403 | LF | `ecf99cc7db720040…` |
| 38 | `src/vero_monitor/runner.py` | 4826 | LF | `9c72b7358f12d5c0…` |
| 39 | `src/vero_monitor/scheduler.py` | 10977 | LF | `758cf1aba70498ae…` |
| 40 | `src/vero_monitor/server.py` | 7423 | LF | `42a1833e37c8f670…` |
| 41 | `src/vero_monitor/store.py` | 5943 | LF | `b144a73706a236cc…` |
| 42 | `src/vero_monitor/web/dashboard.html` | 18415 | LF | `d43abb27805424ff…` |
| 43 | `start_dashboard.bat` | 199 | CRLF | `c9b963844055acd4…` |
| 44 | `status.bat` | 169 | CRLF | `6a754b5b8c1f74cd…` |
| 45 | `tests/__init__.py` | 20 | LF | `7e9af23c4d8769e8…` |
| 46 | `tests/fixtures/.gitkeep` | 26 | LF | `2be8225f3a9ad9e9…` |
| 47 | `tests/fixtures/vero_task_stream.ndjson` | 937 | LF | `e4018110354d7118…` |
| 48 | `tests/helpers.py` | 1003 | LF | `0b35f2b3014752b8…` |
| 49 | `tests/integration/__init__.py` | 79 | LF | `629eee0283bc7304…` |
| 50 | `tests/integration/test_chat.py` | 3559 | LF | `4462c0068b40fc9d…` |
| 51 | `tests/integration/test_checks.py` | 4391 | LF | `d033eb5c33fbbed3…` |
| 52 | `tests/integration/test_runner_server.py` | 6369 | LF | `3bd30361d1bed252…` |
| 53 | `tests/unit/__init__.py` | 56 | LF | `34d8097b45b98a68…` |
| 54 | `tests/unit/test_config.py` | 3057 | LF | `b089b300e44f15ca…` |
| 55 | `tests/unit/test_domain.py` | 4177 | LF | `9401a448b001527c…` |
| 56 | `tests/unit/test_parsers.py` | 3486 | LF | `83b0765d6362af16…` |
| 57 | `tests/unit/test_scheduler.py` | 1904 | LF | `6d6460ec569ce5a1…` |
| 58 | `uninstall.bat` | 182 | CRLF | `bce5f932e3942a7e…` |
| 59 | `vam.py` | 273 | LF | `25f30ade67d0e13c…` |

---

## Files

### FILE: `.ci/README.md`

````markdown
# CI

Plan `QAI-vero-availability-monitor-PRGATE`: ruff check, mypy (strict), unit + integration tests, secret scan.

```
uvx ruff check .
uvx mypy
python -m unittest discover -s tests -t .
```
````

### FILE: `.gitattributes`

````text
* text=auto
*.py  text eol=lf
*.sh  text eol=lf
*.md  text
*.bat text eol=crlf
*.png binary
*.jpg binary
START_HERE.txt text eol=crlf
````

### FILE: `.gitignore`

````text
__pycache__/
*.py[cod]
.venv/
venv/
.env
.env.*
*.log
.idea/
.vscode/
dist/
build/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
data/
data-demo/
reports/
config/monitor.json
*.docx
*.xlsx
*.pdf
*.pptx
````

### FILE: `AGENTS.md`

````markdown
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
````

### FILE: `CHANGELOG.md`

````markdown
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
````

### FILE: `CODEOWNERS`

````text
# path            reviewers
*                 @qai-reviewers
````

### FILE: `CONTRIBUTING.md`

````markdown
# Contributing

- Branch per NXP internal strategy, with Jira key
- Commit and PR title: <JIRA-KEY>: <summary>
- PR into main: 1 peer approval required, SME optional

## PR checklist
- [ ] Jira key in branch, commits, title
- [ ] Tests added or updated (synthetic fixtures only)
- [ ] Check logic, AI agent, model or coverage change: golden set re-run, SME invited
- [ ] PRD / ARCHITECTURE / AGENTS updated if behaviour changed
- [ ] No secrets, office documents or run outputs
- [ ] CHANGELOG updated
````

### FILE: `README.md`

````markdown
# vero-availability-monitor

Purpose: answer one question continuously: **is Vero available right now?** A status page for Vero CLI (and optionally Vero Chat).
Owner: << OWNER >> (Quality AI Automation, GenAI Group 3)
Jira: ASPF-1578 (AES SW Process Framework) · Version 3.0.0 · Rules: SCMP (ASPF-1619), CONTRIBUTING.md

Guide: [docs/VeroAvailabilityMonitor_Guide.html](docs/VeroAvailabilityMonitor_Guide.html) · AI context: [VERO_CONTEXT.md](VERO_CONTEXT.md)

## What it checks (every 15 min by default)

| Check | How | Cost |
|---|---|---|
| `cli`  | `vero version`: installed and starts | free, ~1 s |
| `task` | `vero task --json -m <model> -t 180 -c <empty dir> "Reply with exactly: OK"`: end-to-end answer, `completion_result` event | 2 small model calls, ~1 min |
| `chat` (optional) | Vero Chat MCP `initialize` handshake, token from an environment variable | free, no model call |

Result per run: **available**, **degraded** (slow, unexpected answer, or a secondary check down), **unavailable**.

## Install (Windows)

Python 3.8+ only, no pip, no admin rights.

1. Get the folder to e.g. `C:\Tools\vero-availability-monitor\` (git clone, or rebuild from `VeroAvailabilityMonitor_3.0.0_REBUILD.md`).
2. Optional: `setup_demo.bat` (fake CLI + sample data).
3. `setup.bat`: questions -> one real test -> **Y** installs the scheduled check, the status page at logon and a desktop shortcut "Vero Status".
4. `status.bat` any time; `uninstall.bat` to remove (data kept).

## Commands

```
python vam.py configure | doctor | check | serve [--open] | install | uninstall | status | open | export | report | init [--demo]
```

## Develop

```
python -m unittest discover -s tests -t .     # 64 tests, fake CLI + fake MCP server only
uvx ruff check . && uvx ruff format --check .  # lint + format
uvx mypy && uvx mypy --platform win32          # strict typing, Linux and Windows
python scripts/build_rebuild_md.py             # dist/VeroAvailabilityMonitor_<ver>_REBUILD.md
```
````

### FILE: `START_HERE.txt`

````text
VERO AVAILABILITY MONITOR 3  (ASPF-1578)
========================================

Shows whether Vero is available right now, with history, on a local status page.
Needs Python 3.8+ only. No admin rights, no internet download, nothing to install with pip.

1. Put this folder somewhere local and fixed, e.g.  C:\Tools\vero-availability-monitor
   (not Downloads, not a OneDrive folder)

2. (optional) Double-click  setup_demo.bat   -> status page with a fake CLI and sample data

3. Double-click  setup.bat
     - answer the questions (Vero program, model, checks, timing; Enter = default)
     - it tests Vero once (the task check takes about a minute)
     - answer Y to install background monitoring
   The status page opens. Later: desktop shortcut "Vero Status" or http://127.0.0.1:8766/

Other files:
   start_dashboard.bat   open the status page (starts it if needed)
   check_now.bat         check Vero now
   status.bat            what is configured and running
   uninstall.bat         remove scheduled tasks and shortcut (data is kept)

If the old "Vero Latency Monitor" (0.x) is installed, run uninstall.bat in its folder:
both would call Vero every 15 minutes.

Full guide: docs\VeroAvailabilityMonitor_Guide.html
For Vero CLI / AI agents: VERO_CONTEXT.md
Problems:   status.bat, then data\monitor.log, then the guide, section Troubleshooting.
````

### FILE: `VERO_CONTEXT.md`

````markdown
# VERO_CONTEXT: vero-availability-monitor 3.0.0

> **For the AI reading this:** this file describes the whole project.
> - Use it to answer questions or make changes safely.
> - Read a file before editing it, and keep the rules in section 7.
> - Answer from this file and the repository only. Items marked `<< TO CONFIRM >>` are open, so do not guess.

## 1. What it is

A small local tool that answers one question continuously: **is Vero available right now?** It shows the answer on a status page at `http://127.0.0.1:8766`.

- **Jira:** ASPF-1578 (AES SW Process Framework). Quality AI Automation team, NXP.
- **Governed by:** the SCMP of ASPF-1619.
- **Runtime:** Python 3.8+ standard library only. Windows first; Linux and macOS work too.
- **History:** 3.0.0 replaces the 0.x "latency monitor" (ADR-002). Both can run side by side: they use different ports, task names and data folders.

## 2. Checks, every 15 min by default

| Check | Command / call | Up when | Degraded when | Down when | Cost |
|---|---|---|---|---|---|
| `cli` | `vero version` | exit 0 | – | not found, exit ≠ 0, or timeout (30 s) | free |
| `task` | `vero task --json -m {model} -t {timeout} -c {workdir} {prompt}` | a `completion_result` event arrives | slower than `thresholds_s.task_slow` (90 s), or the answer lacks `expect` | no `completion_result`, exit ≠ 0, or the hard limit is hit | 2 small model calls, about 1 min |
| `chat` (optional) | POST JSON-RPC `initialize` to Vero Chat MCP, `Authorization: Bearer $<token_env>` | a result with `serverInfo` | answer slower than 10 s | token variable missing, HTTP 401/403, unreachable, MCP error, or a reply that is not MCP | free, no model call |

Rules that tie the checks together:
- **Order:** `cli`, then `chat`, then `task`. If `cli` is down, `task` is not run and is recorded as down ("skipped").
- **Overall run status:**
  - DOWN if the primary check is down. The primary check is `task` when it is enabled, otherwise `cli`.
  - DEGRADED if any other check is down, or any check is degraded.
  - UP otherwise.
- **Availability** = runs that are not DOWN, divided by all runs.
- **Incident** = consecutive non-UP runs that include an outage, or a degradation lasting 2 or more runs. It ends at the next UP run.

### Vero CLI `--json` contract (Vero CLI 2.3.x, integration guide §3.3)

- The stream has one JSON object per line. The **only** answer is `say == "completion_result"`.
- Ignore `partial: true` fragments.
- Record `modelInfo.providerId` and `modelInfo.modelId`. Never assume them from the config.
- `task_started.taskId` identifies the task.
- `api_req_started.text` contains the full upstream prompt, so it is **never** stored or logged. The parser keeps only the fields above.
- Never pass `--yolo` (ADR-003). The task runs with `-c data/sandbox`, an empty folder.
- The process tree is killed at `-t + min(30 s, -t)`; with the defaults that is 210 s.

## 3. Structure

Dependencies point downwards only.

```
vam.py                         entry point (adds src/ to sys.path)
src/vero_monitor/
  domain.py        PURE: Status, Check, CheckResult, RunResult, Point, Incident; overall_status,
                   availability_percent, incidents, timeline, current_since, worst
  config.py        typed frozen dataclasses (Config, VeroSettings, ChatSettings); DEFAULTS; build/load/validate
  checks/
    process.py     run(args, timeout) -> ProcessResult; kill_tree; resolve (shutil.which)
    vero_cli.py    check_cli, check_task, parse_stream, task_command, hard_limit_s, clean (mask secrets)
    vero_chat.py   check_chat, parse_reply (JSON or SSE)
    __init__.py    enabled(cfg), run_all(cfg)  (contains crashes, skips task when cli down)
  store.py         SQLite data/availability.db: runs, checks (ON DELETE CASCADE)
  runner.py        run_once: RunLock (data/run.lock, stale recovery) -> run_all -> overall -> save -> prune -> manifest
  report.py        payload(cfg, store, hours) for the status page; static_html snapshot
  scheduler.py     Loop (in-process timer); Task Scheduler XML / cron install, remove, status; desktop shortcut
  server.py        HTTP: / , /api/status, /api/stream (SSE), POST /api/check, /api/export.csv, /api/health
  cli.py           commands (section 5)
  web/dashboard.html   status page, one file, vanilla JS, no CDN
scripts/  fake_vero.py (stand-in CLI), seed_demo_data.py, build_rebuild_md.py, _py.bat
tests/    unit/ (domain, parsers, config, scheduler)  integration/ (fake CLI, fake MCP, runner, HTTP)
docs/     guide HTML, PRD, ARCHITECTURE, DESIGN_SYSTEM, decisions/ADR-001..004
*.bat     setup, setup_demo, start_dashboard, check_now, status, uninstall
```

## 4. Data

**`config/monitor.json`**
- Defaults live in `config.DEFAULTS`, and `monitor.example.json` equals them.
- The JSON keys are:

| Key | Contents |
|---|---|
| `vero` | `command`, `model`, `prompt`, `expect`, `task_timeout_s`, `task_args`, `version_args`, `env` |
| `checks` | `cli`, `task`, `chat` |
| `chat` | `url`, `token_env`, `timeout_s`, `ca_bundle` |
| `thresholds_s` | `task_slow`, `chat_slow` |
| `schedule` | `interval_minutes`, `run_in_dashboard` |
| | `retention_days` |
| `server` | `host`, `port` (8766) |
| | `data_dir` |

- Validation raises `ConfigError` with a readable message. Among other things it enforces that the worst-case run (`timeout + min(30, timeout) + 30` s) fits inside the interval.
- The file is read as `utf-8-sig`, so a BOM from Notepad is fine. Environment variables in `data_dir` are expanded.

**SQLite**

| Table | Columns |
|---|---|
| `runs` | `run_id` (PK), `started_at`, `epoch`, `trigger`, `overall`, `reason`, `host`, `tool_version` |
| `checks` | `id`, `run_id` (FK cascade), `epoch`, `check_name`, `status`, `duration_ms`, `detail`, `version`, `provider_id`, `model_id` |

**Run manifest** (`data/runs/<YYYY-MM>/<run_id>.json`):

```json
{"run_id","component":"vero-availability","tool_version","trigger","host","started_at","overall","reason",
 "model":{"provider","id","configured_id"},"checks":[{"check","status","duration_ms","detail","version"}]}
```

The run_id format is `<YYYYMMDD-HHMM>-vero-availability`, with a `-2` suffix for a second run in the same minute.

## 5. Commands

Run as `python vam.py <command>`.

| Command | What it does |
|---|---|
| `configure` | Guided questions |
| `init [--demo]` | Writes the config. `--demo` uses the fake CLI and `data-demo/`. |
| `doctor` | Runs all checks once **without storing**. Exit 1 if the result is DOWN. |
| `check [--trigger] [-q]` | Stores one run. Exit 2 if DOWN; always 0 with `--trigger task`. |
| `serve [--open] [--port] [--no-scheduler]` | Status page. If one is already running, it only opens the browser. |
| `install [--every N] [--no-dashboard]` | Registers the Task Scheduler tasks `VeroAvailabilityCheck` (every N min: on battery, catch-up, no overlap) and `VeroAvailabilityDashboard` (at logon, hidden), adds the desktop shortcut "Vero Status", and sets `run_in_dashboard=false`. On Linux/macOS it uses cron instead. |
| `uninstall` | Removes the tasks and the shortcut. Data is kept. |
| `status` | Shows configuration, last run and task state |
| `open` | Opens the running status page |
| `export` | Writes CSV |
| `report --hours` | Writes a self-contained HTML snapshot |

## 6. Quality gates

```
uvx ruff check . && uvx ruff format --check .      # lint (incl. bandit S, bugbear B) + format, 130 cols
uvx mypy && uvx mypy --platform win32               # strict typing for Linux and Windows
python -m unittest discover -s tests -t .           # 64 tests, Python 3.8-3.13, warnings-as-errors clean
```

**Fake CLI modes** (`FAKE_VERO_MODE`):

| Mode | Behaviour |
|---|---|
| `ok` | Answers normally |
| `slow` | Answers late |
| `down` | Provider unavailable, exit 1 |
| `auth` | Unauthorised, with a decoy token in stderr (must be masked) |
| `nocompletion` | Exit 0 without a `completion_result` |
| `refuse` | Answers, but not with `OK` |
| `hang` | Never answers (must be killed) |
| `random` | Default; mostly ok, sometimes slow or failing |

`FAKE_VERO_DELAY` sets the answer delay. The fake emits a decoy secret in `api_req_started`, and a test proves it is never persisted.

## 7. Rules (do not break)

1. Standard library only, Python 3.8 compatible. No CDN, no pip dependencies.
2. Keep `domain.py` pure (no I/O). Never import upwards across the layers.
3. No `--yolo`. Only `completion_result` is an answer. Never persist the event stream, model answers, tokens or `vero.env` values.
4. Bind to 127.0.0.1 only, and keep the Host and Origin checks.
5. One run at a time, through `runner.run_once` (it takes `RunLock`).
6. Tests never call the real Vero. Every subprocess uses `creationflags=NO_WINDOW`, and every timeout kills the process tree.
7. Commit and PR title: `ASPF-1578: <summary>`. Never commit `data/`, `data-demo/`, `dist/`, `reports/` or `config/monitor.json`. Update the CHANGELOG, the guide and this file when behaviour changes.

## 8. Open items (`<< TO CONFIRM >>`)

- The owner, and the repository location in Bitbucket project QAI.
- Whether Vero is an approved platform component at all. SCMP v0.5 does not mention it (integration guide §9).
- The cheapest pinned model id. The default is Haiku 4.5 on Bedrock, as measured.
- The `task_slow` threshold (default 90 s, based on the measured p95 of 59 s).
- Whether `vero task` without `--yolo` ever waits for approval on newer Vero versions (ADR-003).
- Who owns the Vero Chat token, if the `chat` check is enabled (a functional account, per the SCMP).
````

### FILE: `check_now.bat`

````bat
@echo off
rem Runs all enabled checks once and stores the result.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py check
pause
````

### FILE: `config/monitor.example.json`

````json
{
  "vero": {
    "command": "vero",
    "model": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    "prompt": "Reply with exactly: OK",
    "expect": "OK",
    "task_timeout_s": 180,
    "task_args": [
      "task",
      "--json",
      "-m",
      "{model}",
      "-t",
      "{timeout}",
      "-c",
      "{workdir}",
      "{prompt}"
    ],
    "version_args": [
      "version"
    ],
    "env": {}
  },
  "checks": {
    "cli": true,
    "task": true,
    "chat": false
  },
  "chat": {
    "url": "https://verostudio.sw.nxp.com/mcp",
    "token_env": "VERO_CHAT_TOKEN",
    "timeout_s": 30,
    "ca_bundle": ""
  },
  "thresholds_s": {
    "task_slow": 90,
    "chat_slow": 10
  },
  "schedule": {
    "interval_minutes": 15,
    "run_in_dashboard": true
  },
  "retention_days": 90,
  "server": {
    "host": "127.0.0.1",
    "port": 8766
  },
  "data_dir": "data"
}
````

### FILE: `docs/ARCHITECTURE.md`

````markdown
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
````

### FILE: `docs/DESIGN_SYSTEM.md`

````markdown
# Design system: vero-availability-monitor

## Colours
SCMP tokens: available `#1f7a45`, degraded `#a8500b`, unavailable `#9b1c2e`, no data `#b7bfcb`, brand `#0a6aa1`; tinted
backgrounds for the status banner; full dark-mode token set.

## Typography
IBM Plex Sans / Segoe UI; tabular numbers for figures.

## Components
Status banner (icon, title, since, reason), component card (dot, name, status, facts), availability tile, status
timeline (bars = worst status per slot), incident table, recent-checks table with per-check dots, live pill.

## Rules
Words, not only colour: every status has a label (available / degraded / unavailable / no data). The banner says
what users need first: is Vero available, since when, and why not.
````

### FILE: `docs/PRD.md`

````markdown
# PRD: vero-availability-monitor

## Problem
The Quality AI Automation team depends on Vero (Vero CLI, Vero Chat). When Vero is unavailable nobody knows until a workflow fails, and there is no record of how often it happens.

## Goal
Know at a glance whether Vero is available now, since when, and how available it has been over 24 h, 7 d and 30 d, at the lowest possible cost.

## Users
Quality Lead (owner of the figures), Quality AI Automation team, SW QA Engineers.

## Requirements
| ID | Requirement | Jira |
|----|-------------|------|
| VAM-001 | Use the cheapest possible end-to-end call (fixed minimal prompt, pinned cheap model) plus free checks | ASPF-1578 AC1 |
| VAM-002 | Time trigger: Task Scheduler (laptop-safe) / cron, or the status page's own timer | ASPF-1578 AC2 |
| VAM-003 | Record every run (SQLite + run manifest) and show it on a status page | ASPF-1578 AC3 |
| VAM-004 | Fully automated after setup (scheduled checks, status page at logon, pruning, log rotation) | ASPF-1578 AC4 |
| VAM-005 | Status per run: available / degraded / unavailable, with the reason | ASPF-1578 |
| VAM-006 | Availability 24 h / 7 d / 30 d, status timeline, incidents | ASPF-1578 |
| VAM-007 | Optional Vero Chat check without any model call | ASPF-1578 |
| VAM-008 | Install from a guided script; distributable as a readable document | ASPF-1578 |

## Out of scope
Latency analytics (0.x tool), alerting by e-mail/Teams, measuring interactive sessions, Vero use in pipeline stage 4.
````

### FILE: `docs/decisions/ADR-001_stdlib-only.md`

````markdown
# ADR-001: Python standard library only
Status: accepted (kept from 0.x)

Context: distributed to laptops without admin rights or PyPI access; archives and scripts are often blocked.
Decision: Python 3.8+ standard library only; dashboard is one HTML file with inline JS/CSS, no CDN.
Consequences: nothing to install or patch; dev tools (ruff, mypy) are used only by developers via `uvx`.
````

### FILE: `docs/decisions/ADR-002_availability-not-latency.md`

````markdown
# ADR-002: Monitor availability, not latency
Status: accepted (3.0.0)

Context: Vero CLI `task` latency is dominated by start-up and agent orchestration (~52 s for "Reply with OK",
integration guide 3.4). Latency analytics of a cold-start agent say little; what the team needs is "is Vero usable now".
Decision: the tool reports available / degraded / unavailable per run, availability %, timeline and incidents.
Duration is kept only as a check attribute and as the "slow" (degraded) criterion.
Consequences: simpler status page; the 0.x latency monitor is superseded.
````

### FILE: `docs/decisions/ADR-003_no-yolo-sandbox.md`

````markdown
# ADR-003: No --yolo; run the task in an empty sandbox folder
Status: accepted (3.0.0)

Context: `vero task` starts an agent that can read/write files and run shell commands; `--yolo` auto-approves them
(integration guide 3.7). The availability probe only needs `attempt_completion`.
Decision: never pass `--yolo`; pass `-c data/sandbox` (an empty folder) and `-t` (timeout); kill the process tree at
`-t + min(30 s, -t)`. The prompt is fixed and harmless.
Consequences: if a Vero version starts asking for approval even for completion, the task check reports DOWN
("no completion"); the guide explains how to diagnose it.
````

### FILE: `docs/decisions/ADR-004_vero-chat-handshake.md`

````markdown
# ADR-004: Vero Chat checked by MCP handshake, token from an environment variable
Status: accepted (3.0.0)

Context: Vero Chat is an MCP server; a `tools/call` runs an agent that can take minutes. The `initialize` handshake
proves the endpoint and the token work without any model call. Tokens must never be stored in config or Git.
Decision: the optional `chat` check sends `initialize` only; the bearer token is read from the environment variable
named in `chat.token_env` (default `VERO_CHAT_TOKEN`) at run time.
Consequences: free and fast; it does not prove the Chat agent can answer (secondary check: its failure only degrades).
````

### FILE: `pyproject.toml`

````toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "vero-availability-monitor"
version = "3.0.0"
description = "Is Vero available? Status dashboard for Vero CLI and Vero Chat (ASPF-1578)"
requires-python = ">=3.8"
dependencies = []

[project.scripts]
vam = "vero_monitor.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
vero_monitor = ["web/*.html"]

[tool.ruff]
line-length = 130
target-version = "py38"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "S", "SIM", "RUF"]
ignore = [
  "S603", "S607",   # subprocess calls are the purpose of this tool (fixed argument lists, no shell)
  "S310",           # urlopen on a configured https URL (Vero Chat)
  "S104",           # 0.0.0.0 only compared, never bound by default
  "UP006", "UP007", "UP035", "UP045",  # keep typing.List/Optional for Python 3.8 readability
  "RUF001", "RUF003",
]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "S108", "S105", "S106", "S314"]  # S314: parses XML the tool itself generated
"scripts/**" = ["S311"]

[tool.mypy]
python_version = "3.9"
files = ["src"]
strict = true
warn_unused_ignores = true
````

### FILE: `requirements.txt`

````text
# No third-party dependencies: Python 3.8+ standard library only (docs/decisions/ADR-001_stdlib-only.md).
````

### FILE: `scripts/_py.bat`

````bat
@echo off
rem Finds Python 3.8+ and sets PY. Called by the other .bat files.
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY goto nopy
%PY% -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul || goto nopy
exit /b 0
:nopy
echo.
echo  Python 3.8 or newer was not found.
echo  Install it from Software Center, or python.org (tick "Add python.exe to PATH"),
echo  or run:  winget install Python.Python.3.12
echo  Then run this file again.
echo.
pause
exit /b 1
````

### FILE: `scripts/build_rebuild_md.py`

`````python
#!/usr/bin/env python3
"""Build dist/VeroAvailabilityMonitor_<version>_REBUILD.md: the complete source as one Markdown document.

For channels that accept no archives and no scripts. Every file is a readable fenced code block;
an AI assistant (or a person) recreates the folder from it and checks each file with SHA-256.
The HTML guide is left out (it is sent as its own file); everything else is included."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vero_monitor import __version__  # noqa: E402

SKIP_DIRS = {
    "data",
    "data-demo",
    "reports",
    "dist",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    ".git",
}
SKIP_FILES = {"config/monitor.json", "docs/VeroAvailabilityMonitor_Guide.html"}
CRLF_SUFFIXES = (".bat",)
CRLF_FILES = {"START_HERE.txt"}
LANG = {".py": "python", ".json": "json", ".md": "markdown", ".html": "html", ".bat": "bat", ".toml": "toml", ".txt": "text"}


def lf_sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def fence_for(text: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    return "`" * max(4, longest + 1)


def files():
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if f.is_dir() or SKIP_DIRS & set(rel.parts) or rel.as_posix() in SKIP_FILES or f.suffix in (".pyc", ".log"):
            continue
        yield rel.as_posix(), f.read_bytes().decode("utf-8")


VERIFY = r"""import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vero-availability-monitor")
md = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "REBUILD.md").read_text(encoding="utf-8")
manifest = json.loads(re.search(r"<!-- MANIFEST\n(.*?)\n-->", md, re.S).group(1))
bad = 0
for path, info in manifest["files"].items():
    p = root / path
    if not p.exists():
        print("MISSING ", path); bad += 1; continue
    text = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != info["sha256_lf"]:
        print("DIFFERENT", path); bad += 1
    elif info["crlf"] and b"\r\n" not in p.read_bytes():
        p.write_bytes(text.replace("\n", "\r\n").encode("utf-8")); print("fixed CRLF", path)
print("OK: all files match" if not bad else f"{bad} file(s) wrong: recreate them from the document")
sys.exit(1 if bad else 0)
"""


def main() -> None:
    items = list(files())
    manifest = {
        "version": __version__,
        "files": {
            p: {"sha256_lf": lf_sha(t), "crlf": p.endswith(CRLF_SUFFIXES) or p in CRLF_FILES, "bytes": len(t.encode("utf-8"))}
            for p, t in items
        },
    }
    out = ROOT / "dist" / f"VeroAvailabilityMonitor_{__version__}_REBUILD.md"
    out.parent.mkdir(exist_ok=True)
    w = []
    w.append(f"""# Vero Availability Monitor {__version__}: complete source for rebuild

**What this is.** The full source of the Vero Availability Monitor (Jira ASPF-1578), a local tool that checks
whether Vero (CLI, optionally Chat) is available and shows it on a status page. It is sent as a readable document because archives
and scripts cannot be attached. Nothing in it runs by itself. Read it before rebuilding.

- {len(items)} files, all plain text, Python 3.8+ standard library only (no downloads, no pip).
- The HTML guide `VeroAvailabilityMonitor_Guide.html` is sent separately; put it in `docs/`.
- `VERO_CONTEXT.md` (included below) explains the architecture, contracts and rules.

---

## Instructions for the AI assistant (Vero CLI or other)

You are asked to recreate a project folder **exactly** from this document.

1. Create the folder `vero-availability-monitor/` in the location the user gives you (default: `C:\\Tools\\`).
2. For **every** section below that starts with `### FILE:`, create that file at that relative path,
   with the content of the code block that follows, **byte for byte**:
   - do not reformat, re-indent, translate, "improve", summarise or skip anything;
   - copy only the lines *between* the opening and closing fence (the fence is 4 or more backticks);
   - keep a trailing newline at the end of each file, exactly as in the block;
   - encoding UTF-8 without BOM.
3. Line endings: LF for every file, **except** those marked `CRLF` in the table (the `.bat` files and
   `START_HERE.txt`), which must use CRLF (Windows).
4. Create empty folders if needed: `data/` is **not** needed (the tool creates it).
5. Verify: save the Python block in the section *Verify the rebuild* as `verify_rebuild.py` next to this
   document (outside the project folder), then run
   `py verify_rebuild.py C:\\Tools\\vero-availability-monitor VeroAvailabilityMonitor_{__version__}_REBUILD.md`.
   It checks every file against its SHA-256 (computed on LF line endings) and fixes CRLF where needed.
   If it reports `DIFFERENT` or `MISSING`, recreate those files again from this document.
6. Then run the tests: `py -m unittest discover -s tests -t .` inside the folder. Expected: `OK` (64 tests, about 10 s).
7. Report the result to the user, then tell them to double-click `setup.bat` (see `START_HERE.txt`).

Do not run `setup.bat`, `install`, `doctor`, `check` or the real Vero CLI yourself unless the user asks.

---

## File list

| # | Path | Bytes | Line endings | SHA-256 (LF) |
|---|------|------:|:---:|---|
""")
    for i, (p, _text) in enumerate(items, 1):
        m = manifest["files"][p]
        w.append(f"| {i} | `{p}` | {m['bytes']} | {'CRLF' if m['crlf'] else 'LF'} | `{m['sha256_lf'][:16]}…` |\n")
    w.append("\n---\n\n## Files\n\n")
    for p, t in items:
        text = t.replace("\r\n", "\n")
        f = fence_for(text)
        lang = LANG.get(Path(p).suffix, "") if not p.endswith(("CODEOWNERS", ".gitignore", ".gitattributes")) else "text"
        body = text if text.endswith("\n") else text + "\n"
        w.append(f"### FILE: `{p}`\n\n{f}{lang}\n{body}{f}\n\n")
    w.append("---\n\n## Verify the rebuild\n\n")
    w.append("Save as `verify_rebuild.py` (outside the project folder) and run it as described in step 5.\n\n")
    w.append(f"````python\n{VERIFY}````\n\n")
    w.append("<!-- MANIFEST\n" + json.dumps(manifest, indent=1) + "\n-->\n")
    out.write_text("".join(w), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({len(items)} files, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
`````

### FILE: `scripts/fake_vero.py`

````python
#!/usr/bin/env python3
"""Stand-in for the Vero CLI (demo and tests). Emulates `vero version` and
`vero task --json -m <model> -t <s> -c <dir> <prompt>` with the event stream of Vero CLI 2.3.x.

FAKE_VERO_MODE: ok | slow | down | auth | nocompletion | refuse | hang | random (default)
FAKE_VERO_DELAY: seconds before the answer (default: about 1-3 s)
"""

import json
import os
import random
import sys
import time

MODEL = {"providerId": "bedrock", "modelId": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "mode": "act"}


def emit(obj):
    print(json.dumps(obj), flush=True)


def main(argv):
    if not argv or argv[0] in ("version", "--version", "-V"):
        print("vero 2.3.3 (fake0000)")
        return 0
    if argv[0] not in ("task", "t"):
        print(f"unknown command {argv[0]}", file=sys.stderr)
        return 2
    args = argv[1:]
    model = MODEL["modelId"]
    if "-m" in args:
        model = args[args.index("-m") + 1]
    prompt = args[-1] if args else ""
    mode = os.environ.get("FAKE_VERO_MODE", "random")
    if mode == "random":
        r = random.random()
        mode = "down" if r < 0.03 else "nocompletion" if r < 0.05 else "slow" if r < 0.09 else "ok"
    delay = float(os.environ.get("FAKE_VERO_DELAY", random.uniform(1.0, 3.0)))
    info = dict(MODEL, modelId=model)
    ts = int(time.time() * 1000)
    if "--json" in args:
        emit({"type": "task_started", "taskId": str(ts)})
        emit({"ts": ts, "type": "say", "say": "task", "text": prompt, "modelInfo": info})
        # the real CLI puts the full upstream prompt here; the monitor must never keep it
        emit(
            {
                "ts": ts,
                "type": "say",
                "say": "api_req_started",
                "text": json.dumps({"request": "SYSTEM PROMPT ... FAKE-SECRET-api_req_started ..."}),
                "modelInfo": info,
            }
        )
    if mode == "hang":
        time.sleep(3600)
    if mode == "auth":
        print("error: Unauthorized (token=abc123secret) - run vero auth", file=sys.stderr)
        return 1
    if mode == "down":
        time.sleep(min(delay, 1))
        print("error: provider unavailable: connect ETIMEDOUT bedrock-runtime.us-west-2", file=sys.stderr)
        return 1
    time.sleep(delay * (6 if mode == "slow" else 1))
    answer = "I cannot help with that." if mode == "refuse" else "OK"
    if "--json" in args:
        emit({"ts": ts, "type": "say", "say": "text", "text": answer[:1], "partial": True, "modelInfo": info})
        emit({"ts": ts, "type": "say", "say": "text", "text": answer, "partial": False, "modelInfo": info})
        if mode != "nocompletion":
            emit({"ts": ts, "type": "say", "say": "completion_result", "text": answer, "modelInfo": info})
    else:
        print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
````

### FILE: `scripts/seed_demo_data.py`

````python
#!/usr/bin/env python3
"""Fill data-demo/ with 7 days of synthetic checks (with a few incidents) so the status page
can be shown before Vero is connected. Refuses any data folder other than data-demo."""

import datetime as dt
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vero_monitor import config  # noqa: E402
from vero_monitor.domain import Check, CheckResult, RunResult, Status, overall_status  # noqa: E402
from vero_monitor.runner import iso  # noqa: E402
from vero_monitor.store import Store  # noqa: E402

cfg = config.load()
if not cfg.data_dir.name.startswith("data-demo"):
    sys.exit(f"refusing to seed demo data into {cfg.data_dir}: run  vam init --demo  first")
store = Store(cfg.data_dir)
rnd = random.Random(1578)
now = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0)
t = now - dt.timedelta(days=7)
outages = [
    (now - dt.timedelta(days=5, hours=3), 70),
    (now - dt.timedelta(days=2, hours=9), 35),
    (now - dt.timedelta(hours=20), 25),
]
n = 0
while t < now:
    down = any(s <= t < s + dt.timedelta(minutes=m) for s, m in outages)
    task_s = rnd.lognormvariate(0, 0.12) * 52
    checks = [CheckResult(Check.CLI, Status.UP, rnd.uniform(800, 1500), version="vero 2.3.3 (demo)")]
    if down:
        checks.append(
            CheckResult(
                Check.TASK, Status.DOWN, 210000.0, "no completion within 210 s", provider_id="bedrock", model_id=cfg.vero.model
            )
        )
    elif rnd.random() < 0.04:
        checks.append(
            CheckResult(
                Check.TASK,
                Status.DEGRADED,
                task_s * 2000,
                f"slow: {task_s * 2:.0f} s > 90 s",
                provider_id="bedrock",
                model_id=cfg.vero.model,
            )
        )
    else:
        checks.append(CheckResult(Check.TASK, Status.UP, task_s * 1000, provider_id="bedrock", model_id=cfg.vero.model))
    run_id = f"{t:%Y%m%d-%H%M}-vero-availability-demo"
    if not store.run_exists(run_id):
        store.save(RunResult(run_id, iso(t), t.timestamp(), "demo", tuple(checks), overall_status(checks)), "demo", "demo")
        n += 1
    t += dt.timedelta(minutes=15)
print(f"seeded {n} demo runs into {store.path}")
````

### FILE: `setup.bat`

````bat
@echo off
rem Guided first-time setup: configure -> test -> install background monitoring.
setlocal
cd /d "%~dp0"
title Vero availability monitor - setup
call scripts\_py.bat || exit /b 1
echo.
echo  Vero availability monitor 3  (Python: %PY%)
echo  ------------------------------------------------------------
:configure
%PY% vam.py configure
if errorlevel 1 goto again
echo.
echo  Testing Vero once (nothing stored). The task check can take about a minute...
%PY% vam.py doctor
if errorlevel 1 goto again
echo.
choice /C YN /M " Install background monitoring (check on a timer + status page at every logon)"
if errorlevel 2 goto manual
%PY% vam.py install
%PY% vam.py open
goto end
:manual
echo.
echo  Not installed. Use start_dashboard.bat (it also checks while its window is open).
goto end
:again
echo.
choice /C YN /M " Not ready. Run the configuration again"
if errorlevel 2 goto end
goto configure
:end
echo.
pause
````

### FILE: `setup_demo.bat`

````bat
@echo off
rem Demo: fake Vero CLI + 7 days of sample data in data-demo\ (separate from real data).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py init --demo --force || goto end
%PY% scripts\seed_demo_data.py || goto end
echo.
echo  Demo ready. The status page opens now; close this window to stop it.
%PY% vam.py serve --open
:end
pause
````

### FILE: `src/vero_monitor/__init__.py`

````python
"""Vero availability monitor (ASPF-1578): is Vero CLI / Vero Chat available right now?"""

__version__ = "3.0.0"
COMPONENT = "vero-availability"
````

### FILE: `src/vero_monitor/__main__.py`

````python
import sys

from .cli import main

sys.exit(main())
````

### FILE: `src/vero_monitor/checks/__init__.py`

````python
"""Check registry: which checks run, in which order. Cheap checks first."""

from __future__ import annotations

import logging
import time
from typing import Callable, List, Tuple

from ..config import Config
from ..domain import Check, CheckResult, Status
from .vero_chat import check_chat
from .vero_cli import check_cli, check_task

log = logging.getLogger("vero_monitor")

CheckFn = Callable[[Config], CheckResult]


def enabled(cfg: Config) -> List[Tuple[Check, CheckFn]]:
    plan: List[Tuple[Check, CheckFn]] = []
    if cfg.check_cli:
        plan.append((Check.CLI, check_cli))
    if cfg.check_chat:
        plan.append((Check.CHAT, check_chat))
    if cfg.check_task:
        plan.append((Check.TASK, check_task))
    return plan


def run_all(cfg: Config) -> List[CheckResult]:
    results: List[CheckResult] = []
    cli_down = False
    for name, fn in enabled(cfg):
        if name is Check.TASK and cli_down:
            # no point spending a minute on a task when the CLI cannot even start
            results.append(CheckResult(Check.TASK, Status.DOWN, None, "skipped: Vero CLI not available"))
            continue
        t0 = time.perf_counter()
        try:
            res = fn(cfg)
        except Exception as e:  # a bug in one check must not hide the others
            log.exception("check %s crashed", name.value)
            res = CheckResult(name, Status.DOWN, (time.perf_counter() - t0) * 1000, f"monitor error: {type(e).__name__}")
        results.append(res)
        cli_down = cli_down or (name is Check.CLI and res.status is Status.DOWN)
    return results
````

### FILE: `src/vero_monitor/checks/process.py`

````python
"""Run one external process with a hard timeout. Kills the whole process tree on timeout
(vero.cmd -> node -> ...), never opens a console window on Windows."""

from __future__ import annotations

import contextlib
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from typing import List, Mapping, Optional, Sequence

IS_WINDOWS = os.name == "nt"
NO_WINDOW = 0x08000000 if IS_WINDOWS else 0  # CREATE_NO_WINDOW


@dataclass(frozen=True)
class ProcessResult:
    started: bool
    exit_code: Optional[int]
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool


def resolve(program: str) -> Optional[str]:
    """Full path of the program, or None. Finds vero.cmd / vero.exe for 'vero' on Windows."""
    return shutil.which(program)


def kill_tree(proc: subprocess.Popen[bytes]) -> None:
    """Kill the process and everything it started (vero.cmd -> node -> ...)."""
    with contextlib.suppress(OSError):
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, creationflags=NO_WINDOW, check=False
            )
        else:
            os.killpg(proc.pid, signal.SIGKILL)  # own process group: start_new_session=True
    with contextlib.suppress(OSError):
        proc.kill()


def run(
    args: Sequence[str], timeout_s: float, env: Optional[Mapping[str, str]] = None, cwd: Optional[str] = None
) -> ProcessResult:
    full_env = dict(os.environ)
    full_env.update(env or {})
    t0 = time.perf_counter()
    try:
        proc = subprocess.Popen(
            list(args),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=full_env,
            cwd=cwd,
            creationflags=NO_WINDOW,
            start_new_session=not IS_WINDOWS,
        )
    except OSError as e:
        return ProcessResult(False, None, "", f"cannot start {args[0]!r}: {e}", 0.0, False)

    out: List[bytes] = []
    err: List[bytes] = []
    stdout, stderr = proc.stdout, proc.stderr
    if stdout is None or stderr is None:  # cannot happen with PIPE; keeps the types honest
        kill_tree(proc)
        return ProcessResult(False, None, "", "no output pipes", 0.0, False)
    readers = [
        threading.Thread(target=lambda: out.append(stdout.read()), daemon=True),
        threading.Thread(target=lambda: err.append(stderr.read()), daemon=True),
    ]
    for r in readers:
        r.start()
    timed_out = False
    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_tree(proc)
        proc.wait()
    duration = (time.perf_counter() - t0) * 1000
    for r in readers:
        r.join(timeout=5)
    stdout.close()  # release OS handles (long-running dashboard on Windows)
    stderr.close()
    return ProcessResult(
        started=True,
        exit_code=proc.returncode,
        stdout=b"".join(out).decode("utf-8", "replace"),
        stderr=b"".join(err).decode("utf-8", "replace"),
        duration_ms=duration,
        timed_out=timed_out,
    )
````

### FILE: `src/vero_monitor/checks/vero_chat.py`

````python
"""Vero Chat check: MCP `initialize` handshake over streamable HTTP (integration guide 2.1).

No tool is called, so no model runs and nothing is billed. The reply may be plain JSON or
Server-Sent Events (`data:` lines). The bearer token comes from an environment variable;
it is never stored, logged or shown.
"""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .. import __version__
from ..config import Config
from ..domain import Check, CheckResult, Status
from .vero_cli import clean

INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "vero-availability-monitor", "version": __version__},
    },
}


def parse_reply(body: str) -> Optional[Dict[str, Any]]:
    """Return the JSON-RPC message from a JSON or SSE body, or None."""
    candidates = [body.strip()]
    candidates += [ln[5:].strip() for ln in body.splitlines() if ln.startswith("data:")]
    for c in candidates:
        if not c.startswith("{"):
            continue
        try:
            msg = json.loads(c)
        except json.JSONDecodeError:
            continue
        if isinstance(msg, dict) and ("result" in msg or "error" in msg):
            return msg
    return None


def check_chat(cfg: Config) -> CheckResult:
    token = os.environ.get(cfg.chat.token_env, "").strip()
    if not token:
        return CheckResult(
            Check.CHAT, Status.DOWN, None, f"environment variable {cfg.chat.token_env} is not set (see guide: Vero Chat token)"
        )
    req = urllib.request.Request(
        cfg.chat.url,
        data=json.dumps(INITIALIZE).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    ctx = ssl.create_default_context(cafile=cfg.chat.ca_bundle or None)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=cfg.chat.timeout_s, context=ctx) as r:
            body = r.read(256 * 1024).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        hint = " (token rejected or expired)" if e.code in (401, 403) else ""
        return CheckResult(Check.CHAT, Status.DOWN, (time.perf_counter() - t0) * 1000, f"HTTP {e.code}{hint}")
    except (urllib.error.URLError, OSError, ValueError) as e:
        reason = getattr(e, "reason", e)
        return CheckResult(Check.CHAT, Status.DOWN, (time.perf_counter() - t0) * 1000, clean(f"unreachable: {reason}"))
    ms = (time.perf_counter() - t0) * 1000
    msg = parse_reply(body)
    if msg is None:
        return CheckResult(Check.CHAT, Status.DOWN, ms, "reply is not an MCP JSON-RPC message")
    if "error" in msg:
        err = msg["error"] if isinstance(msg["error"], dict) else {}
        return CheckResult(Check.CHAT, Status.DOWN, ms, clean(f"MCP error: {err.get('message', msg['error'])}"))
    info = (msg.get("result") or {}).get("serverInfo") or {}
    version = clean(f"{info.get('name', '?')} {info.get('version', '')}".strip())
    slow = ms > cfg.chat_slow_s * 1000
    return CheckResult(
        Check.CHAT, Status.DEGRADED if slow else Status.UP, ms, f"slow: {ms / 1000:.1f} s" if slow else "", version=version
    )
````

### FILE: `src/vero_monitor/checks/vero_cli.py`

````python
"""Vero CLI checks.

cli  : `vero version`          -> installed and starts. Free, a few seconds.
task : `vero task --json ...`  -> end-to-end: the agent reaches the model and completes.

Contract of the --json stream (Vero CLI 2.3.x, see the integration guide section 3.3):
one JSON object per line; the answer is ONLY the `say == "completion_result"` event; `partial: true`
fragments are ignored; `modelInfo` gives the real provider/model; `task_started` gives the taskId.
`api_req_started.text` holds the full upstream prompt and is never kept or logged.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from ..config import Config
from ..domain import Check, CheckResult, Status
from . import process

DETAIL_MAX = 200
_SECRETISH = re.compile(r"(?i)(bearer\s+\S+|token[=:]\s*\S+|aws_secret\S*|password[=:]\s*\S+)")


def clean(text: str) -> str:
    """One short line, with anything that looks like a credential masked."""
    line = " ".join(text.split())
    return _SECRETISH.sub("[masked]", line)[:DETAIL_MAX]


@dataclass(frozen=True)
class TaskStream:
    task_id: Optional[str]
    completion: Optional[str]
    provider_id: Optional[str]
    model_id: Optional[str]
    error: Optional[str]
    events: int


def parse_stream(lines: Iterable[str]) -> TaskStream:
    task_id = completion = provider = model = error = None
    events = 0
    for raw in lines:
        raw = raw.strip()
        if not raw.startswith("{"):
            continue
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(ev, dict):
            continue
        events += 1
        if ev.get("type") == "task_started" and ev.get("taskId") is not None:
            task_id = str(ev["taskId"])
        info = ev.get("modelInfo")
        if isinstance(info, dict):
            provider = info.get("providerId") or provider
            model = info.get("modelId") or model
        if ev.get("partial") is True:
            continue
        say = ev.get("say")
        if say == "completion_result":
            completion = str(ev.get("text") or "")
        elif say in ("error", "api_req_failed") or ev.get("type") == "error":
            error = clean(str(ev.get("text") or ev.get("message") or say))
    return TaskStream(task_id, completion, provider, model, error, events)


def _program(cfg: Config) -> Optional[str]:
    return process.resolve(cfg.vero.command)


def check_cli(cfg: Config) -> CheckResult:
    exe = _program(cfg)
    if not exe:
        return CheckResult(Check.CLI, Status.DOWN, None, f"'{cfg.vero.command}' not found on PATH")
    r = process.run([exe, *cfg.vero.version_args], 30, dict(cfg.vero.env))
    if r.timed_out:
        return CheckResult(Check.CLI, Status.DOWN, r.duration_ms, "version command timed out")
    if r.exit_code != 0:
        return CheckResult(Check.CLI, Status.DOWN, r.duration_ms, f"exit {r.exit_code}: {clean(r.stderr or r.stdout)}")
    first = (r.stdout.strip().splitlines() or [""])[0]
    return CheckResult(Check.CLI, Status.UP, r.duration_ms, "", version=clean(first)[:80])


def task_command(cfg: Config, exe: str, workdir: Path) -> list[str]:
    fill = {
        "{model}": cfg.vero.model,
        "{timeout}": str(int(cfg.vero.task_timeout_s)),
        "{workdir}": str(workdir),
        "{prompt}": cfg.vero.prompt,
    }
    args = [exe]
    for a in cfg.vero.task_args:
        for k, v in fill.items():
            a = a.replace(k, v)
        args.append(a)
    return args


def hard_limit_s(cfg: Config) -> float:
    """Our own kill deadline: Vero's -t plus a grace period (min(30 s, -t)) in case the CLI ignores -t."""
    return cfg.vero.task_timeout_s + min(30.0, cfg.vero.task_timeout_s)


def check_task(cfg: Config) -> CheckResult:
    exe = _program(cfg)
    if not exe:
        return CheckResult(Check.TASK, Status.DOWN, None, f"'{cfg.vero.command}' not found on PATH")
    workdir = cfg.data_dir / "sandbox"  # empty folder: the agent has nothing to read or change
    workdir.mkdir(parents=True, exist_ok=True)
    limit = hard_limit_s(cfg)
    r = process.run(task_command(cfg, exe, workdir), limit, dict(cfg.vero.env), str(workdir))
    if not r.started:
        return CheckResult(Check.TASK, Status.DOWN, None, clean(r.stderr))
    s = parse_stream(r.stdout.splitlines())

    def result(status: Status, detail: str) -> CheckResult:
        return CheckResult(Check.TASK, status, r.duration_ms, clean(detail), provider_id=s.provider_id, model_id=s.model_id)

    if r.timed_out:
        return result(Status.DOWN, f"no completion within {limit:g} s")
    if s.completion is None:
        why = s.error or (f"exit {r.exit_code}: {r.stderr}" if r.exit_code else "")
        why = why or ("no JSON events: is --json in vero.task_args?" if s.events == 0 else "no completion_result")
        return result(Status.DOWN, why)
    notes = []
    if cfg.vero.expect and cfg.vero.expect.lower() not in s.completion.lower():
        notes.append(f"answered, but not with {cfg.vero.expect!r} ({len(s.completion)} chars)")
    if r.duration_ms > cfg.task_slow_s * 1000:
        notes.append(f"slow: {r.duration_ms / 1000:.0f} s > {cfg.task_slow_s:g} s")
    return result(Status.DEGRADED if notes else Status.UP, "; ".join(notes))
````

### FILE: `src/vero_monitor/cli.py`

````python
"""Command line: python vam.py <command>. Run with -h for help."""

from __future__ import annotations

import argparse
import csv
import logging
import logging.handlers
import os
import shutil
import sys
import time
import webbrowser
from pathlib import Path
from typing import Callable, Dict, List, Optional

from . import __version__, config, scheduler
from .checks import run_all
from .checks.vero_cli import task_command
from .config import ROOT, Config, ConfigError
from .domain import Status, overall_status
from .report import static_html
from .runner import in_progress, run_once
from .server import already_running, serve
from .store import CSV_HEADER, Store

log = logging.getLogger("vero_monitor")
FAKE = ROOT / "scripts" / "fake_vero.py"
ICON = {"up": "UP  ", "degraded": "WARN", "down": "DOWN", "unknown": "  ? "}


def setup_logging(data_dir: Path, verbose: bool) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    handlers: List[logging.Handler] = [
        logging.handlers.RotatingFileHandler(data_dir / "monitor.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    ]
    if sys.stdout is not None:  # None under pythonw (Task Scheduler)
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        handlers=handlers,
        format="%(asctime)s %(levelname)s %(message)s",
        force=True,
    )


def ask(question: str, default: str) -> str:
    try:
        answer = input(f"{question} [{default}]: ").strip()
    except EOFError:
        answer = ""
    return answer or default


def yes(question: str, default: bool) -> bool:
    return ask(question + " (y/n)", "y" if default else "n").lower().startswith("y")


# commands without a loaded config -------------------------------------------------


def cmd_init(a: argparse.Namespace) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    if target.exists() and not a.force:
        print(f"{target} already exists (--force to overwrite, or: vam configure)")
        return 0
    raw = config.read_json(config.EXAMPLE_FILE)
    if a.demo:
        # the fake CLI is a Python script: run it with this Python, script path as first argument
        raw["vero"]["command"] = sys.executable
        raw["vero"]["version_args"] = [str(FAKE)] + raw["vero"]["version_args"]
        raw["vero"]["task_args"] = [str(FAKE)] + raw["vero"]["task_args"]
        raw["schedule"]["interval_minutes"] = 2
        raw["vero"]["task_timeout_s"] = 30
        raw["thresholds_s"]["task_slow"] = 8
        raw["data_dir"] = "data-demo"  # never mixed with real measurements
    config.write_json(target, raw)
    print(f"wrote {target}" + ("  (demo: fake Vero CLI, data in data-demo/)" if a.demo else ""))
    return 0


def cmd_configure(a: argparse.Namespace) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    raw = config.read_json(config.EXAMPLE_FILE)
    if target.exists():
        try:
            cur = config.read_json(target)
            if not str(cur.get("data_dir", "")).startswith("data-demo"):
                raw = config.merge(raw, cur)
        except ConfigError as e:
            print(f"current config is broken, starting from the defaults ({e})")
    raw = config.merge(config.DEFAULTS, raw)
    v = raw["vero"]
    print("\nVero availability monitor: configuration. Enter keeps the value in [brackets].\n")
    while True:
        v["command"] = ask("1. Vero CLI program (name or full path; `where vero` shows it)", v["command"]).strip('"')
        found = shutil.which(v["command"])
        if found:
            print(f"   found: {found}")
            break
        print(f"   '{v['command']}' was not found on PATH.")
        if yes("   Keep it anyway", False):
            break
    v["model"] = ask("2. Model id to pin (-m), cheapest first", v["model"])
    raw["checks"]["task"] = yes("3. End-to-end task check (~1 min, 2 small model calls per run)", raw["checks"]["task"])
    raw["checks"]["chat"] = yes("4. Also check Vero Chat (MCP handshake, free; needs a token variable)", raw["checks"]["chat"])
    if raw["checks"]["chat"]:
        raw["chat"]["token_env"] = ask(
            "   Name of the environment variable holding the Vero Chat token", raw["chat"]["token_env"]
        )
        if not os.environ.get(raw["chat"]["token_env"]):
            print(f"   note: {raw['chat']['token_env']} is not set in this session (see guide, Vero Chat token)")
    try:
        raw["schedule"]["interval_minutes"] = int(ask("5. Check every N minutes", str(raw["schedule"]["interval_minutes"])))
        v["task_timeout_s"] = float(ask("6. Task timeout, seconds", f"{float(v['task_timeout_s']):g}"))
        raw["thresholds_s"]["task_slow"] = float(
            ask("7. Task counts as slow (degraded) above, seconds", f"{float(raw['thresholds_s']['task_slow']):g}")
        )
        config.build(raw, target)
    except (ConfigError, ValueError) as e:
        print(f"\nnot saved: {e}")
        return 1
    config.write_json(target, raw)
    print(f"\nsaved {target}")
    return 0


# commands with a config ----------------------------------------------------------


def cmd_doctor(a: argparse.Namespace, cfg: Config) -> int:
    print(f"config    {cfg.path}\ndata      {cfg.data_dir}")
    print(f"program   {cfg.vero.command} -> {shutil.which(cfg.vero.command) or 'NOT FOUND'}")
    if cfg.check_task:
        exe = shutil.which(cfg.vero.command) or cfg.vero.command
        cmd = task_command(cfg, exe, cfg.data_dir / "sandbox")
        print("task cmd  " + " ".join(f'"{a}"' if " " in a else a for a in cmd))
    print("running the enabled checks once (nothing is stored)...")
    results = run_all(cfg)
    for r in results:
        ms = f"{r.duration_ms / 1000:6.1f} s" if r.duration_ms is not None else "      - "
        extra = " ".join(x for x in (r.version or "", r.model_id or "", r.detail) if x)
        print(f"  {ICON[r.status.value]}  {r.check.value:<5} {ms}  {extra}")
    overall = overall_status(results)
    print(
        f"RESULT    {overall.value.upper()}"
        + ("  -> ready" if overall is not Status.DOWN else "  -> fix the items above (guide: Troubleshooting)")
    )
    return 0 if overall is not Status.DOWN else 1


def cmd_check(a: argparse.Namespace, cfg: Config) -> int:
    run = run_once(cfg, Store(cfg.data_dir), a.trigger)
    if run is None:
        print("another run is in progress; skipped")
        return 0
    if not a.quiet:
        for r in run.checks:
            print(f"  {ICON[r.status.value]}  {r.check.value:<5} {r.detail}")
        print(f"{run.run_id}: {run.overall.value.upper()}")
    if a.trigger == "task":
        return 0  # a DOWN result is data, not a task failure (Task Scheduler 'Last Result' stays 0)
    return 0 if run.overall is not Status.DOWN else 2


def cmd_serve(a: argparse.Namespace, cfg: Config) -> int:
    if a.port:
        cfg = config.build({**config.read_json(cfg.path), "server": {"host": cfg.host, "port": a.port}}, cfg.path)
    return serve(cfg, Store(cfg.data_dir), cfg.run_in_dashboard and not a.no_scheduler, a.open)


def _set_run_in_dashboard(cfg: Config, value: bool) -> None:
    raw = config.read_json(cfg.path)
    raw.setdefault("schedule", {})["run_in_dashboard"] = value
    config.write_json(cfg.path, raw)


def cmd_install(a: argparse.Namespace, cfg: Config) -> int:
    every = int(a.every or cfg.interval_minutes)
    if not 1 <= every <= 1440:
        print("--every must be between 1 and 1440")
        return 1
    url = f"http://127.0.0.1:{cfg.port}/"
    for line in scheduler.install(every, url, dashboard=not a.no_dashboard):
        print(line)
    _set_run_in_dashboard(cfg, False)
    print(f"config: schedule.run_in_dashboard = false\nopen the dashboard: {url}")
    return 0


def cmd_uninstall(a: argparse.Namespace, cfg: Config) -> int:
    for line in scheduler.remove():
        print(line)
    _set_run_in_dashboard(cfg, True)
    print(f"config: schedule.run_in_dashboard = true. Data kept in {cfg.data_dir}")
    return 0


def cmd_status(a: argparse.Namespace, cfg: Config) -> int:
    store = Store(cfg.data_dir)
    last = store.runs(limit=1)
    print(f"version   {__version__}\nconfig    {cfg.path}\ndata      {cfg.data_dir} ({store.count()} runs)")
    if last:
        r = last[0]
        print(f"last run  {r['run_id']}  {r['overall'].upper()}  {r['reason'] or ''}")
    else:
        print("last run  none yet")
    print(f"running   {'yes' if in_progress(cfg) else 'no'}")
    up = already_running(cfg.port)
    print(f"dashboard {f'up at http://127.0.0.1:{cfg.port}/' if up else 'not running'}\n")
    print(scheduler.status())
    return 0


def cmd_open(a: argparse.Namespace, cfg: Config) -> int:
    url = f"http://127.0.0.1:{cfg.port}/"
    deadline = time.time() + a.wait
    while not already_running(cfg.port):
        if time.time() > deadline:
            print(f"dashboard not running at {url}: use start_dashboard.bat, see data/monitor.log")
            return 1
        time.sleep(1)
    webbrowser.open(url)
    print(f"opened {url}")
    return 0


def cmd_export(a: argparse.Namespace, cfg: Config) -> int:
    out = Path(a.out or "vero_availability.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = Store(cfg.data_dir).csv_rows(time.time() - a.hours * 3600 if a.hours else 0)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CSV_HEADER)
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)")
    return 0


def cmd_report(a: argparse.Namespace, cfg: Config) -> int:
    out = Path(a.out or "vero_status_report.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(static_html(cfg, Store(cfg.data_dir), a.hours), encoding="utf-8")
    print(f"wrote {out} (last {a.hours} h, self-contained)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vam", description="Vero availability monitor (ASPF-1578)")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--config", help="config file (default config/monitor.json, or env VAM_CONFIG)")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", metavar="command")
    sub.required = True
    s = sub.add_parser("init", help="create config/monitor.json from the example")
    s.add_argument("--demo", action="store_true", help="bundled fake Vero CLI, data in data-demo/")
    s.add_argument("--force", action="store_true")
    sub.add_parser("configure", help="guided configuration")
    sub.add_parser("doctor", help="run the checks once without storing, and explain the result")
    s = sub.add_parser("check", help="run the checks now and store the result")
    s.add_argument("--trigger", default="manual", choices=["manual", "task", "schedule", "dashboard"])
    s.add_argument("-q", "--quiet", action="store_true")
    s = sub.add_parser("serve", help="status dashboard (with the built-in timer unless installed)")
    s.add_argument("--port", type=int)
    s.add_argument("--no-scheduler", action="store_true")
    s.add_argument("--open", action="store_true")
    s = sub.add_parser("install", help="scheduled check + dashboard at logon + desktop shortcut")
    s.add_argument("--every", type=int)
    s.add_argument("--no-dashboard", action="store_true")
    sub.add_parser("uninstall", help="remove the tasks and the shortcut (data is kept)")
    sub.add_parser("status", help="configuration, last run, dashboard and task state")
    s = sub.add_parser("open", help="open the running dashboard")
    s.add_argument("--wait", type=float, default=20)
    s = sub.add_parser("export", help="CSV of runs and checks")
    s.add_argument("--hours", type=float, default=0)
    s.add_argument("--out")
    s = sub.add_parser("report", help="self-contained HTML snapshot")
    s.add_argument("--hours", type=int, default=168, choices=[1, 6, 24, 168, 720])
    s.add_argument("--out")
    return p


HANDLERS: Dict[str, Callable[[argparse.Namespace, Config], int]] = {
    "doctor": cmd_doctor,
    "check": cmd_check,
    "serve": cmd_serve,
    "install": cmd_install,
    "uninstall": cmd_uninstall,
    "status": cmd_status,
    "open": cmd_open,
    "export": cmd_export,
    "report": cmd_report,
}


def main(argv: Optional[List[str]] = None) -> int:
    a = build_parser().parse_args(argv)
    try:
        if a.cmd == "init":
            return cmd_init(a)
        if a.cmd == "configure":
            return cmd_configure(a)
        cfg = config.load(a.config)
    except ConfigError as e:
        print(f"config error: {e}")
        return 1
    setup_logging(cfg.data_dir, a.verbose)
    try:
        return HANDLERS[a.cmd](a, cfg)
    except KeyboardInterrupt:
        return 130
    except (RuntimeError, OSError) as e:
        log.error("%s failed: %s", a.cmd, e)
        return 1
    except Exception:
        log.exception("%s crashed", a.cmd)  # visible in data/monitor.log even under pythonw
        return 1
````

### FILE: `src/vero_monitor/config.py`

````python
"""Typed configuration loaded from config/monitor.json. Non-secret settings only:
the Vero Chat token is read from an environment variable named in the config, never stored."""

from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = ROOT / "config" / "monitor.json"
EXAMPLE_FILE = ROOT / "config" / "monitor.example.json"

DEFAULTS: Dict[str, Any] = {
    "vero": {
        "command": "vero",
        "model": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
        "prompt": "Reply with exactly: OK",
        "expect": "OK",
        "task_timeout_s": 180,
        "task_args": ["task", "--json", "-m", "{model}", "-t", "{timeout}", "-c", "{workdir}", "{prompt}"],
        "version_args": ["version"],
        "env": {},
    },
    "checks": {"cli": True, "task": True, "chat": False},
    "chat": {
        "url": "https://verostudio.sw.nxp.com/mcp",
        "token_env": "VERO_CHAT_TOKEN",
        "timeout_s": 30,
        "ca_bundle": "",
    },
    "thresholds_s": {"task_slow": 90, "chat_slow": 10},
    "schedule": {"interval_minutes": 15, "run_in_dashboard": True},
    "retention_days": 90,
    "server": {"host": "127.0.0.1", "port": 8766},
    "data_dir": "data",
}


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class VeroSettings:
    command: str
    model: str
    prompt: str
    expect: str
    task_timeout_s: float
    task_args: Tuple[str, ...]
    version_args: Tuple[str, ...]
    env: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class ChatSettings:
    url: str
    token_env: str
    timeout_s: float
    ca_bundle: str


@dataclass(frozen=True)
class Config:
    vero: VeroSettings
    chat: ChatSettings
    check_cli: bool
    check_task: bool
    check_chat: bool
    task_slow_s: float
    chat_slow_s: float
    interval_minutes: int
    run_in_dashboard: bool
    retention_days: int
    host: str
    port: int
    data_dir: Path
    path: Path

    def public(self) -> Dict[str, Any]:
        """What the dashboard may show. No env values, no token, no token variable value."""
        return {
            "model": self.vero.model,
            "prompt": self.vero.prompt,
            "checks": {"cli": self.check_cli, "task": self.check_task, "chat": self.check_chat},
            "chat_url": self.chat.url if self.check_chat else None,
            "interval_minutes": self.interval_minutes,
            "task_timeout_s": self.vero.task_timeout_s,
            "task_slow_s": self.task_slow_s,
            "retention_days": self.retention_days,
        }


def merge(base: Dict[str, Any], over: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out


def read_json(path: Path) -> Dict[str, Any]:
    try:
        text = Path(path).read_text(encoding="utf-8-sig")  # Notepad may add a BOM
    except OSError as e:
        raise ConfigError(f"cannot read {path}: {e}") from e
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        hint = " (Windows paths: C:\\\\Tools\\\\x or C:/Tools/x)" if "escape" in str(e).lower() else ""
        raise ConfigError(f"{path}: invalid JSON: {e}{hint}") from e
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: the top level must be a JSON object")
    return data


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _str_list(value: Any, name: str) -> Tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(a, str) for a in value):
        raise ConfigError(f"{name} must be a list of strings")
    return tuple(value)


def _positive(value: Any, name: str, kind: type = float) -> Any:
    try:
        v = kind(value)
    except (TypeError, ValueError) as e:
        raise ConfigError(f"{name} must be a number, got {value!r}") from e
    if v <= 0:
        raise ConfigError(f"{name} must be > 0")
    return v


def build(raw: Dict[str, Any], path: Path) -> Config:
    d = merge(DEFAULTS, raw)
    v, c, ch = d["vero"], d["checks"], d["chat"]
    task_args = _str_list(v["task_args"], "vero.task_args")
    if not any("{prompt}" in a for a in task_args):
        raise ConfigError("vero.task_args needs a {prompt} placeholder")
    if not isinstance(v["command"], str) or not v["command"].strip():
        raise ConfigError('vero.command must be the program name or full path, e.g. "vero"')
    env = {} if v.get("env") is None else v["env"]
    if not isinstance(env, dict):
        raise ConfigError('vero.env must be an object, e.g. {"HTTPS_PROXY": "..."}')
    flags = {k: c.get(k) for k in ("cli", "task", "chat")}
    if any(not isinstance(x, bool) for x in flags.values()):
        raise ConfigError("checks.cli / checks.task / checks.chat must be true or false")
    if not (flags["cli"] or flags["task"] or flags["chat"]):
        raise ConfigError("enable at least one check")
    interval = _positive(d["schedule"]["interval_minutes"], "schedule.interval_minutes", int)
    if interval > 1440:
        raise ConfigError("schedule.interval_minutes must be between 1 and 1440")
    timeout = _positive(v["task_timeout_s"], "vero.task_timeout_s")
    worst_case = timeout + min(30.0, timeout) + 30  # task hard limit + cli/chat checks
    if flags["task"] and worst_case > interval * 60:
        raise ConfigError(
            f"a run can take up to {worst_case:g} s, longer than the {interval} min interval:"
            " lower vero.task_timeout_s or raise schedule.interval_minutes"
        )
    data_dir = Path(os.path.expandvars(os.path.expanduser(str(d["data_dir"]))))
    return Config(
        vero=VeroSettings(
            command=v["command"].strip(),
            model=str(v["model"]),
            prompt=str(v["prompt"]),
            expect=str(v["expect"]),
            task_timeout_s=timeout,
            task_args=task_args,
            version_args=_str_list(v["version_args"], "vero.version_args"),
            env=tuple((str(k), str(x)) for k, x in env.items()),
        ),
        chat=ChatSettings(
            url=str(ch["url"]),
            token_env=str(ch["token_env"]),
            timeout_s=_positive(ch["timeout_s"], "chat.timeout_s"),
            ca_bundle=str(ch["ca_bundle"]),
        ),
        check_cli=flags["cli"],
        check_task=flags["task"],
        check_chat=flags["chat"],
        task_slow_s=_positive(d["thresholds_s"]["task_slow"], "thresholds_s.task_slow"),
        chat_slow_s=_positive(d["thresholds_s"]["chat_slow"], "thresholds_s.chat_slow"),
        interval_minutes=interval,
        run_in_dashboard=bool(d["schedule"]["run_in_dashboard"]),
        retention_days=_positive(d["retention_days"], "retention_days", int),
        host=str(d["server"]["host"]),
        port=_positive(d["server"]["port"], "server.port", int),
        data_dir=data_dir if data_dir.is_absolute() else ROOT / data_dir,
        path=path,
    )


def load(path: Path | str | None = None) -> Config:
    p = Path(path or os.environ.get("VAM_CONFIG") or CONFIG_FILE)
    if not p.exists():
        raise ConfigError(f"config not found: {p} (run setup.bat, or: python vam.py configure)")
    return build(read_json(p), p)
````

### FILE: `src/vero_monitor/domain.py`

````python
"""Domain model and pure rules. No I/O here: everything is unit-testable.

Vocabulary
- check:    one probe of one component (cli, task, chat) -> CheckResult
- run:      all enabled checks at one moment            -> RunResult with an overall Status
- incident: consecutive runs whose overall status is not UP
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence


class Status(str, Enum):
    UP = "up"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"  # no data

    @property
    def rank(self) -> int:
        return {"unknown": 0, "up": 1, "degraded": 2, "down": 3}[self.value]


def worst(statuses: Iterable[Status]) -> Status:
    result = Status.UNKNOWN
    for s in statuses:
        if s.rank > result.rank:
            result = s
    return result


class Check(str, Enum):
    CLI = "cli"  # `vero version`: installed and starts (free, seconds)
    TASK = "task"  # `vero task --json`: end-to-end answer through the model (2 API calls, ~1 min)
    CHAT = "chat"  # Vero Chat MCP `initialize` handshake (free, no model call)


@dataclass(frozen=True)
class CheckResult:
    check: Check
    status: Status
    duration_ms: float | None
    detail: str = ""
    version: str | None = None  # cli version or chat server version
    provider_id: str | None = None  # from task modelInfo (never assumed from config)
    model_id: str | None = None


@dataclass(frozen=True)
class RunResult:
    run_id: str
    started_at: str
    epoch: float
    trigger: str
    checks: tuple[CheckResult, ...]
    overall: Status = field(default=Status.UNKNOWN)


def overall_status(results: Sequence[CheckResult]) -> Status:
    """DOWN if the primary check is down (task when enabled, else cli).
    DEGRADED if any other check is down or any check is degraded. UP otherwise."""
    if not results:
        return Status.UNKNOWN
    by = {r.check: r for r in results}
    primary = by.get(Check.TASK) or by.get(Check.CLI) or results[0]
    if primary.status is Status.DOWN:
        return Status.DOWN
    if any(r.status in (Status.DOWN, Status.DEGRADED) for r in results):
        return Status.DEGRADED
    return Status.UP


def availability_percent(statuses: Sequence[Status]) -> float | None:
    """Share of runs where Vero answered (UP or DEGRADED)."""
    known = [s for s in statuses if s is not Status.UNKNOWN]
    if not known:
        return None
    return round(sum(1 for s in known if s is not Status.DOWN) / len(known) * 100, 2)


@dataclass(frozen=True)
class Point:
    """One run on the time axis (what the incident and timeline rules need)."""

    epoch: float
    status: Status
    reason: str = ""


@dataclass(frozen=True)
class Incident:
    start: float
    end: float | None  # None = ongoing
    worst: Status
    runs: int
    reason: str

    def duration_s(self, now: float) -> float:
        return (self.end if self.end is not None else now) - self.start


def incidents(points: Sequence[Point], min_degraded_runs: int = 2) -> list[Incident]:
    """Group consecutive non-UP runs; the incident ends at the first UP run after it.
    Any outage (DOWN) is an incident; a degradation only when it lasts min_degraded_runs runs,
    so one slow answer does not flood the list (it still shows on the timeline)."""
    out: list[Incident] = []
    cur: list[Point] = []
    for p in sorted(points, key=lambda x: x.epoch):
        if p.status in (Status.DOWN, Status.DEGRADED):
            cur.append(p)
            continue
        if cur and p.status is Status.UP:
            out.append(_incident(cur, end=p.epoch))
            cur = []
    if cur:
        out.append(_incident(cur, end=None))
    return [i for i in out if i.worst is Status.DOWN or i.runs >= min_degraded_runs]


def _incident(group: list[Point], end: float | None) -> Incident:
    w = worst(p.status for p in group)
    reason = next((p.reason for p in group if p.status is w and p.reason), "")
    return Incident(start=group[0].epoch, end=end, worst=w, runs=len(group), reason=reason)


def timeline(points: Sequence[Point], start: float, end: float, bins: int) -> list[tuple[float, Status, int]]:
    """Split [start, end) into equal bins; each bin shows the worst status in it (UNKNOWN if empty)."""
    if bins <= 0 or end <= start:
        return []
    width = (end - start) / bins
    acc: list[list[Status]] = [[] for _ in range(bins)]
    for p in points:
        if start <= p.epoch < end:
            acc[min(int((p.epoch - start) / width), bins - 1)].append(p.status)
    return [(start + i * width, worst(a), len(a)) for i, a in enumerate(acc)]


def current_since(points: Sequence[Point]) -> tuple[Status, float | None]:
    """Current overall status and since when it has been continuously so."""
    pts = sorted(points, key=lambda x: x.epoch)
    if not pts:
        return Status.UNKNOWN, None
    status = pts[-1].status
    since = pts[-1].epoch
    for p in reversed(pts):
        if p.status is not status:
            break
        since = p.epoch
    return status, since
````

### FILE: `src/vero_monitor/report.py`

````python
"""Builds the status-page payload (JSON) from stored runs, using the pure domain rules."""

from __future__ import annotations

import datetime as dt
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

from . import __version__
from .config import Config
from .domain import Check, Status, availability_percent, current_since, incidents, timeline
from .store import Store

RANGES = {1: 60, 6: 72, 24: 96, 168: 168, 720: 120}  # hours -> timeline bars
WEB = Path(__file__).parent / "web"


def parse_hours(value: Optional[str], default: int = 24) -> int:
    try:
        h = int(float(value)) if value is not None else default
    except ValueError:
        return default
    return h if h in RANGES else default


def payload(
    cfg: Config,
    store: Store,
    hours: int,
    *,
    running: bool = False,
    scheduler: str = "external",
    next_run: Optional[float] = None,
    now: Optional[float] = None,
) -> Dict[str, Any]:
    now = time.time() if now is None else now
    start = now - hours * 3600
    month = store.points(now - 30 * 86400)
    in_range = [p for p in month if p.epoch >= start] if hours <= 720 else store.points(start)
    status, since = current_since(month)

    def window(h: int) -> Optional[float]:
        return availability_percent([p.status for p in month if p.epoch >= now - h * 3600])

    components = {}
    for chk, on in ((Check.CLI, cfg.check_cli), (Check.TASK, cfg.check_task), (Check.CHAT, cfg.check_chat)):
        last = store.latest_check(chk.value) if on else None
        components[chk.value] = {
            "enabled": on,
            **(
                {k: last[k] for k in ("status", "epoch", "duration_ms", "detail", "version", "provider_id", "model_id")}
                if last
                else {}
            ),
        }

    incs = sorted(incidents(in_range), key=lambda i: -i.start)[:20]
    return {
        "generated_at": dt.datetime.fromtimestamp(now, dt.timezone.utc).isoformat(timespec="seconds"),
        "now": now,
        "tool_version": __version__,
        "range_hours": hours,
        "config": cfg.public(),
        "state": {"running": running, "scheduler": scheduler, "next_run_epoch": next_run},
        "current": {"status": status.value, "since": since},
        "availability": {"24h": window(24), "7d": window(168), "30d": window(720)},
        "counts": {s.value: sum(1 for p in in_range if p.status is s) for s in (Status.UP, Status.DEGRADED, Status.DOWN)},
        "timeline": [{"t": t, "status": s.value, "n": n} for t, s, n in timeline(in_range, start, now, RANGES[hours])],
        "incidents": [
            {
                "start": i.start,
                "end": i.end,
                "worst": i.worst.value,
                "runs": i.runs,
                "duration_s": round(i.duration_s(now)),
                "reason": i.reason,
            }
            for i in incs
        ],
        "components": components,
        "recent": store.runs(start, limit=20),
    }


def static_html(cfg: Config, store: Store, hours: int) -> str:
    """Self-contained HTML snapshot (e-mailable). Every '<' in the data is escaped."""
    blob = json.dumps(payload(cfg, store, hours)).replace("<", "\\u003c")
    html = (WEB / "dashboard.html").read_text(encoding="utf-8")
    return html.replace("<!--STATIC_DATA-->", f"<script>window.STATIC_DATA={blob};</script>", 1)
````

### FILE: `src/vero_monitor/runner.py`

````python
"""Application service: one monitoring run = lock -> checks -> overall status -> store -> manifest."""

from __future__ import annotations

import contextlib
import datetime as dt
import json
import logging
import os
import platform
import time
from pathlib import Path
from typing import Callable, List, Optional

from . import COMPONENT, __version__
from .checks import run_all
from .checks.vero_cli import hard_limit_s
from .config import Config
from .domain import CheckResult, RunResult, overall_status
from .store import Store, reason_of

log = logging.getLogger("vero_monitor")


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def new_run_id(store: Store, when: dt.datetime) -> str:
    """SCMP naming <YYYYMMDD-HHMM>-<component>, suffix -2, -3 within the same minute."""
    base = f"{when.astimezone(dt.timezone.utc):%Y%m%d-%H%M}-{COMPONENT}"
    run_id, n = base, 2
    while store.run_exists(run_id):
        run_id, n = f"{base}-{n}", n + 1
    return run_id


def stale_after_s(cfg: Config) -> float:
    """A lock older than the longest possible run is left over from a crash."""
    return hard_limit_s(cfg) + cfg.chat.timeout_s + 30 + 120


class RunLock:
    """Cross-process lock file. A Task Scheduler run and a dashboard run never overlap."""

    def __init__(self, data_dir: Path, stale_s: float):
        self.path = Path(data_dir) / "run.lock"
        self.stale_s = stale_s
        self.held = False

    def __enter__(self) -> RunLock:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > self.stale_s:
                        self.path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                return self
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            self.held = True
            return self
        return self

    def __exit__(self, *exc: object) -> None:
        if self.held:
            with contextlib.suppress(FileNotFoundError):
                self.path.unlink()


def in_progress(cfg: Config) -> bool:
    try:
        return time.time() - (cfg.data_dir / "run.lock").stat().st_mtime < stale_after_s(cfg)
    except FileNotFoundError:
        return False


Checker = Callable[[Config], List[CheckResult]]


def run_once(cfg: Config, store: Store, trigger: str, checker: Checker = run_all) -> Optional[RunResult]:
    """Run every enabled check once. None if another run holds the lock."""
    with RunLock(cfg.data_dir, stale_after_s(cfg)) as lock:
        if not lock.held:
            log.info("another run is in progress; skipped")
            return None
        now = dt.datetime.now(dt.timezone.utc)
        run_id = new_run_id(store, now)
        results = checker(cfg)
        run = RunResult(
            run_id=run_id,
            started_at=iso(now),
            epoch=now.timestamp(),
            trigger=trigger,
            checks=tuple(results),
            overall=overall_status(results),
        )
        store.save(run, platform.node(), __version__)
        store.prune(cfg.retention_days)
        write_manifest(cfg, run)
        log.info("%s %s %s", run_id, run.overall.value.upper(), " ".join(f"{r.check.value}={r.status.value}" for r in results))
        return run


def write_manifest(cfg: Config, run: RunResult) -> Path:
    """SCMP run manifest: what was checked, with which CLI/model, and the outcome."""
    task = next((c for c in run.checks if c.check.value == "task"), None)
    manifest = {
        "run_id": run.run_id,
        "component": COMPONENT,
        "tool_version": __version__,
        "trigger": run.trigger,
        "host": platform.node(),
        "started_at": run.started_at,
        "overall": run.overall.value,
        "reason": reason_of(run),
        "model": {
            "provider": task.provider_id if task else None,
            "id": task.model_id if task else None,
            "configured_id": cfg.vero.model,
        },
        "checks": [
            {
                "check": c.check.value,
                "status": c.status.value,
                "duration_ms": None if c.duration_ms is None else round(c.duration_ms, 1),
                "detail": c.detail,
                "version": c.version,
            }
            for c in run.checks
        ],
    }
    d = cfg.data_dir / "runs" / run.started_at[:7]
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{run.run_id}.json"
    p.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return p
````

### FILE: `src/vero_monitor/scheduler.py`

````python
"""Time triggers.

- Loop: in-process scheduler used while the dashboard runs in "dashboard" mode.
- install()/remove()/status(): the OS scheduler for unattended use.
  Windows: two Task Scheduler tasks, registered from XML so laptop-safe settings apply
  (runs on battery, catches up after sleep, never two at once):
    VeroAvailabilityCheck     every N minutes: pythonw vam.py check --trigger task
    VeroAvailabilityDashboard at logon:        pythonw vam.py serve --no-scheduler (hidden, background)
  Linux/macOS: two crontab lines (check every N minutes, dashboard @reboot).
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from xml.sax.saxutils import escape

from .checks.process import NO_WINDOW
from .config import ROOT, Config
from .runner import run_once
from .store import Store

log = logging.getLogger("vero_monitor")

PROBE_TASK = "VeroAvailabilityCheck"
DASH_TASK = "VeroAvailabilityDashboard"
CRON_MARK = "# vero-availability-monitor"
SHORTCUT = "Vero Status.url"


def next_aligned(interval_s: int, now: float | None = None) -> float:
    """Next wall-clock boundary (:00, :15, ...). Task Scheduler and the Loop use the same grid."""
    now = time.time() if now is None else now
    return (now // interval_s + 1) * interval_s


class Loop:
    """Runs the checks every interval while the dashboard is open."""

    def __init__(self, cfg: Config, store: Store):
        self.cfg, self.store = cfg, store
        self.interval = cfg.interval_minutes * 60
        self.active = False
        self.next_run: float | None = None
        self.running = False
        self._stop = threading.Event()
        self._busy = threading.Lock()

    def expected_next(self) -> float:
        """Next run time; in external mode the OS scheduler uses the same aligned grid."""
        return self.next_run if self.active and self.next_run else next_aligned(self.interval)

    def trigger(self, source: str) -> bool:
        """Start a cycle in the background. False if one is already running here."""
        if not self._busy.acquire(blocking=False):
            return False

        def work() -> None:
            self.running = True
            try:
                run_once(self.cfg, self.store, source)
            except Exception:
                log.exception("run failed")
            finally:
                self.running = False
                self._busy.release()

        threading.Thread(target=work, daemon=True).start()
        return True

    def start(self) -> None:
        self.active = True

        def loop() -> None:
            self.next_run = next_aligned(self.interval)
            while not self._stop.wait(max(0.0, self.next_run - time.time())):
                self.trigger("schedule")
                self.next_run = next_aligned(self.interval)

        threading.Thread(target=loop, daemon=True).start()

    def stop(self) -> None:
        self._stop.set()


# commands the OS scheduler runs ------------------------------------------------


def _python(background: bool) -> str:
    exe = Path(sys.executable)
    if os.name == "nt" and background:
        w = exe.with_name("pythonw.exe")  # no console window
        if w.exists():
            return str(w)
    return str(exe)


def probe_command() -> list[str]:
    return [_python(True), str(ROOT / "vam.py"), "check", "--trigger", "task", "--quiet"]


def dashboard_command() -> list[str]:
    return [_python(True), str(ROOT / "vam.py"), "serve", "--no-scheduler"]


# Windows ------------------------------------------------------------------------


def _win_user() -> str:
    user = os.environ.get("USERNAME", "")
    dom = os.environ.get("USERDOMAIN", "")
    return f"{dom}\\{user}" if dom and user else user


def _args(cmd: list[str]) -> str:
    return " ".join(f'"{a}"' if (" " in a or a.endswith(".py")) else a for a in cmd)


def _task_xml(description: str, trigger_xml: str, cmd: list[str], time_limit: str) -> str:
    user = escape(_win_user())
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>{escape(description)}</Description></RegistrationInfo>
  <Triggers>{trigger_xml}</Triggers>
  <Principals><Principal id="Author"><UserId>{user}</UserId><LogonType>InteractiveToken</LogonType>
    <RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <ExecutionTimeLimit>{time_limit}</ExecutionTimeLimit>
    <RestartOnFailure><Interval>PT1M</Interval><Count>3</Count></RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{escape(cmd[0])}</Command>
      <Arguments>{escape(_args(cmd[1:]))}</Arguments>
      <WorkingDirectory>{escape(str(ROOT))}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def probe_task_xml(interval_minutes: int) -> str:
    start = dt.datetime.fromtimestamp(next_aligned(interval_minutes * 60)).strftime("%Y-%m-%dT%H:%M:%S")
    trig = (
        f"<TimeTrigger><Repetition><Interval>PT{interval_minutes}M</Interval>"
        f"<StopAtDurationEnd>false</StopAtDurationEnd></Repetition>"
        f"<StartBoundary>{start}</StartBoundary><Enabled>true</Enabled></TimeTrigger>"
    )
    return _task_xml("Vero availability check (ASPF-1578)", trig, probe_command(), "PT1H")


def dashboard_task_xml() -> str:
    trig = f"<LogonTrigger><Enabled>true</Enabled><UserId>{escape(_win_user())}</UserId></LogonTrigger>"
    return _task_xml("Vero status dashboard, http://127.0.0.1 (ASPF-1578)", trig, dashboard_command(), "PT0S")


def _schtasks(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    r = subprocess.run(["schtasks", *args], capture_output=True, text=True, creationflags=NO_WINDOW)
    if check and r.returncode != 0:
        raise RuntimeError(f"schtasks {args[0]} failed: {(r.stderr or r.stdout).strip()}")
    return r


def _register(name: str, xml: str) -> None:
    fd, path = tempfile.mkstemp(suffix=".xml")
    os.close(fd)
    try:
        Path(path).write_text(xml, encoding="utf-16")
        _schtasks("/Create", "/F", "/TN", name, "/XML", path)
    finally:
        os.unlink(path)


def _desktop() -> Path:
    """The real Desktop folder (it may be redirected to OneDrive on Windows)."""
    if sys.platform == "win32":
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            ) as key:
                value = winreg.QueryValueEx(key, "Desktop")[0]
            return Path(os.path.expandvars(str(value)))
        except OSError:
            pass
    return Path.home() / "Desktop"


def _shortcut(url: str) -> Path | None:
    d = _desktop()
    if not d.is_dir():
        return None
    p = d / SHORTCUT
    p.write_text(f"[InternetShortcut]\nURL={url}\n", encoding="utf-8")
    return p


# public -----------------------------------------------------------------------


def install(interval_minutes: int, url: str, dashboard: bool = True) -> list[str]:
    out = []
    if os.name == "nt":
        _register(PROBE_TASK, probe_task_xml(interval_minutes))
        out.append(f"task '{PROBE_TASK}': check every {interval_minutes} min (also on battery, catches up after sleep)")
        if dashboard:
            _register(DASH_TASK, dashboard_task_xml())
            _schtasks("/Run", "/TN", DASH_TASK, check=False)
            out.append(f"task '{DASH_TASK}': dashboard starts hidden at every logon (started now)")
    else:
        lines = [ln for ln in _crontab_lines() if CRON_MARK not in ln]
        lines.append(f"{_cron_expr(interval_minutes)} {' '.join(_sh(c) for c in probe_command())} {CRON_MARK}")
        if dashboard:
            lines.append(f"@reboot {' '.join(_sh(c) for c in dashboard_command())} >/dev/null 2>&1 {CRON_MARK}")
            subprocess.Popen(dashboard_command(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        _write_crontab(lines)
        out.append(f"cron: check every {interval_minutes} min" + (", dashboard @reboot (started now)" if dashboard else ""))
    if dashboard:
        sc = _shortcut(url)
        out.append(f"desktop shortcut: {sc}" if sc else "no desktop folder found; open " + url)
    return out


def remove() -> list[str]:
    out = []
    if os.name == "nt":
        _schtasks("/End", "/TN", DASH_TASK, check=False)
        for name in (PROBE_TASK, DASH_TASK):
            r = _schtasks("/Delete", "/F", "/TN", name, check=False)
            out.append(f"task '{name}': " + ("removed" if r.returncode == 0 else "not installed"))
    else:
        _write_crontab([ln for ln in _crontab_lines() if CRON_MARK not in ln])
        out.append("cron entries removed (a running dashboard stops at the next reboot or with Ctrl+C)")
    sc = _desktop() / SHORTCUT
    if sc.exists():
        sc.unlink()
        out.append("desktop shortcut removed")
    return out


def status() -> str:
    if os.name == "nt":
        parts = []
        for name in (PROBE_TASK, DASH_TASK):
            r = _schtasks("/Query", "/TN", name, "/FO", "LIST", check=False)
            parts.append(r.stdout.strip() if r.returncode == 0 else f"{name}: not installed")
        return "\n\n".join(parts)
    try:
        mine = [ln for ln in _crontab_lines() if CRON_MARK in ln]
    except RuntimeError as e:
        return f"OS scheduler: {e}"
    return "\n".join(mine) if mine else "cron entries not installed"


def _cron_expr(minutes: int) -> str:
    if minutes < 60:
        return f"*/{minutes} * * * *"
    if minutes % 60 == 0 and minutes < 1440:
        return f"0 */{minutes // 60} * * *"
    return "0 0 * * *"


def _sh(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'" if any(c in s for c in " '\"$") else s


def _crontab_lines() -> list[str]:
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    except FileNotFoundError:
        raise RuntimeError("crontab is not installed on this machine") from None
    return r.stdout.splitlines() if r.returncode == 0 else []


def _write_crontab(lines: list[str]) -> None:
    r = subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
````

### FILE: `src/vero_monitor/server.py`

````python
"""Local status page: dashboard HTML, JSON API and a Server-Sent Events stream.
Binds to 127.0.0.1. Host and Origin are checked (no DNS rebinding, no cross-site 'check now')."""

from __future__ import annotations

import contextlib
import csv
import io
import json
import logging
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Optional, Type
from urllib.parse import parse_qs, urlparse

from . import __version__
from .config import Config
from .report import WEB, parse_hours, payload
from .runner import in_progress
from .scheduler import Loop
from .store import CSV_HEADER, Store

log = logging.getLogger("vero_monitor")
APP_ID = "vero-availability"


def make_handler(cfg: Config, store: Store, loop: Optional[Loop]) -> Type[BaseHTTPRequestHandler]:
    allowed_hosts = {f"127.0.0.1:{cfg.port}", f"localhost:{cfg.port}", f"{cfg.host}:{cfg.port}"}

    def running() -> bool:
        return bool(loop and loop.running) or in_progress(cfg)

    def state() -> Dict[str, Any]:
        return {
            "running": running(),
            "scheduler": "dashboard" if loop and loop.active else "external",
            "next_run": loop.expected_next() if loop else None,
        }

    class Handler(BaseHTTPRequestHandler):
        server_version = f"{APP_ID}/{__version__}"

        def log_message(self, format: str, *args: Any) -> None:
            log.debug("%s " + format, self.address_string(), *args)

        def _send(self, code: int, body: bytes, ctype: str, extra: Optional[Dict[str, str]] = None) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj: Any, code: int = 200) -> None:
            self._send(code, json.dumps(obj).encode(), "application/json")

        def _host_ok(self) -> bool:
            return cfg.host == "0.0.0.0" or (self.headers.get("Host") or "").lower() in allowed_hosts

        def _same_origin(self) -> bool:
            origin = self.headers.get("Origin")
            return origin is None or urlparse(origin).netloc.lower() == (self.headers.get("Host") or "").lower()

        def do_GET(self) -> None:
            try:
                if not self._host_ok():
                    return self._json({"error": "forbidden host"}, 403)
                u = urlparse(self.path)
                q = {k: v[0] for k, v in parse_qs(u.query).items()}
                hours = parse_hours(q.get("hours"))
                if u.path in ("/", "/index.html"):
                    self._send(200, (WEB / "dashboard.html").read_bytes(), "text/html; charset=utf-8")
                elif u.path == "/api/status":
                    s = state()
                    self._json(payload(cfg, store, hours, running=s["running"], scheduler=s["scheduler"], next_run=s["next_run"]))
                elif u.path == "/api/health":
                    self._json({"status": "up", "app": APP_ID, "version": __version__})
                elif u.path == "/api/export.csv":
                    buf = io.StringIO()
                    w = csv.writer(buf, lineterminator="\n")
                    w.writerow(CSV_HEADER)
                    w.writerows(store.csv_rows(time.time() - hours * 3600))
                    self._send(
                        200,
                        buf.getvalue().encode(),
                        "text/csv",
                        {"Content-Disposition": 'attachment; filename="vero_availability.csv"'},
                    )
                elif u.path == "/api/stream":
                    self._stream()
                else:
                    self._json({"error": "not found"}, 404)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass
            except Exception:
                log.exception("request failed: %s", self.path)
                with contextlib.suppress(OSError):
                    self._json({"error": "internal error, see data/monitor.log"}, 500)

        def do_POST(self) -> None:
            if not self._host_ok() or not self._same_origin():
                return self._json({"error": "forbidden"}, 403)
            if urlparse(self.path).path != "/api/check":
                return self._json({"error": "not found"}, 404)
            if loop is None:
                return self._json({"error": "unavailable"}, 503)
            if running():
                return self._json({"started": False, "running": True}, 409)
            started = loop.trigger("dashboard")
            self._json({"started": started, "running": True}, 202 if started else 409)

        def _stream(self) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            last = store.last_epoch()
            was: Optional[Dict[str, Any]] = None
            beat = time.time()
            while True:
                s = state()
                if s != was:
                    self._event("state", s)
                    was = s
                for r in store.runs(after_epoch=last, newest_first=False):
                    self._event("run", r)
                    last = max(last, r["epoch"])
                if time.time() - beat > 15:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    beat = time.time()
                time.sleep(1.5)

        def _event(self, name: str, data: Any) -> None:
            self.wfile.write(f"event: {name}\ndata: {json.dumps(data)}\n\n".encode())
            self.wfile.flush()

    return Handler


def already_running(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=2) as r:
            return bool(json.load(r).get("app") == APP_ID)
    except Exception:
        return False


def serve(cfg: Config, store: Store, with_scheduler: bool, open_browser: bool) -> int:
    url = f"http://127.0.0.1:{cfg.port}/"
    if already_running(cfg.port):
        print(f"Dashboard already running: {url}")
        if open_browser:
            webbrowser.open(url)
        return 0
    loop = Loop(cfg, store)
    try:
        httpd = ThreadingHTTPServer((cfg.host, cfg.port), make_handler(cfg, store, loop))
    except OSError as e:
        msg = f"cannot listen on {cfg.host}:{cfg.port} ({e}); set server.port in config/monitor.json"
        log.error(msg)
        print(msg)
        return 1
    httpd.daemon_threads = True
    if with_scheduler:
        loop.start()
    log.info("dashboard %s (scheduler: %s)", url, "dashboard" if with_scheduler else "external")
    print(f"Dashboard: {url}   (Ctrl+C to stop)")
    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()  # after the socket is bound
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        httpd.server_close()
    return 0
````

### FILE: `src/vero_monitor/store.py`

````python
"""SQLite persistence: <data_dir>/availability.db. One row per run, one row per check."""

from __future__ import annotations

import contextlib
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .domain import Point, RunResult, Status

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id       TEXT PRIMARY KEY,
    started_at   TEXT NOT NULL,
    epoch        REAL NOT NULL,
    trigger      TEXT NOT NULL,
    overall      TEXT NOT NULL,
    reason       TEXT,
    host         TEXT,
    tool_version TEXT
);
CREATE TABLE IF NOT EXISTS checks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id       TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    epoch        REAL NOT NULL,
    check_name   TEXT NOT NULL,
    status       TEXT NOT NULL,
    duration_ms  REAL,
    detail       TEXT,
    version      TEXT,
    provider_id  TEXT,
    model_id     TEXT
);
CREATE INDEX IF NOT EXISTS ix_runs_epoch ON runs(epoch);
CREATE INDEX IF NOT EXISTS ix_checks_run ON checks(run_id);
"""


def reason_of(run: RunResult) -> str:
    """The detail of the worst check: what the dashboard shows as the reason."""
    bad = [c for c in run.checks if c.status in (Status.DOWN, Status.DEGRADED)]
    bad.sort(key=lambda c: -c.status.rank)
    return f"{bad[0].check.value}: {bad[0].detail}" if bad else ""


class Store:
    def __init__(self, data_dir: Path):
        self.path = Path(data_dir) / "availability.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.execute("PRAGMA journal_mode=WAL")
            c.executescript(SCHEMA)

    @contextlib.contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        c = sqlite3.connect(str(self.path), timeout=30)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON")
        try:
            with c:
                yield c
        finally:
            c.close()

    def save(self, run: RunResult, host: str, tool_version: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO runs VALUES (?,?,?,?,?,?,?,?)",
                (run.run_id, run.started_at, run.epoch, run.trigger, run.overall.value, reason_of(run), host, tool_version),
            )
            c.executemany(
                "INSERT INTO checks(run_id, epoch, check_name, status, duration_ms, detail, version, provider_id, model_id)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                [
                    (
                        run.run_id,
                        run.epoch,
                        r.check.value,
                        r.status.value,
                        r.duration_ms,
                        r.detail,
                        r.version,
                        r.provider_id,
                        r.model_id,
                    )
                    for r in run.checks
                ],
            )

    def run_exists(self, run_id: str) -> bool:
        with self._conn() as c:
            return c.execute("SELECT 1 FROM runs WHERE run_id=?", (run_id,)).fetchone() is not None

    def prune(self, retention_days: int, now: Optional[float] = None) -> int:
        cutoff = (now or time.time()) - retention_days * 86400
        with self._conn() as c:
            return c.execute("DELETE FROM runs WHERE epoch < ?", (cutoff,)).rowcount

    def points(self, since: float) -> List[Point]:
        with self._conn() as c:
            rows = c.execute("SELECT epoch, overall, reason FROM runs WHERE epoch >= ? ORDER BY epoch", (since,))
            return [Point(r["epoch"], Status(r["overall"]), r["reason"] or "") for r in rows]

    def runs(
        self, since: float = 0, limit: Optional[int] = None, newest_first: bool = True, after_epoch: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        q = "SELECT * FROM runs WHERE epoch >= ?"
        args: List[Any] = [since]
        if after_epoch is not None:
            q += " AND epoch > ?"
            args.append(after_epoch)
        q += " ORDER BY epoch DESC" if newest_first else " ORDER BY epoch"
        if limit:
            q += " LIMIT ?"
            args.append(limit)
        with self._conn() as c:
            runs = [dict(r) for r in c.execute(q, args)]
            for r in runs:
                r["checks"] = [
                    dict(x)
                    for x in c.execute(
                        "SELECT check_name, status, duration_ms, detail, version, provider_id, model_id"
                        " FROM checks WHERE run_id=? ORDER BY id",
                        (r["run_id"],),
                    )
                ]
        return runs

    def latest_check(self, name: str) -> Optional[Dict[str, Any]]:
        with self._conn() as c:
            r = c.execute("SELECT * FROM checks WHERE check_name=? ORDER BY epoch DESC, id DESC LIMIT 1", (name,)).fetchone()
            return dict(r) if r else None

    def last_epoch(self) -> float:
        with self._conn() as c:
            return float(c.execute("SELECT COALESCE(MAX(epoch), 0) FROM runs").fetchone()[0])

    def count(self) -> int:
        with self._conn() as c:
            return int(c.execute("SELECT COUNT(*) FROM runs").fetchone()[0])

    def csv_rows(self, since: float = 0) -> List[List[Any]]:
        with self._conn() as c:
            q = (
                "SELECT r.run_id, r.started_at, r.trigger, r.overall, k.check_name, k.status, k.duration_ms,"
                " k.detail, k.version, k.provider_id, k.model_id FROM runs r JOIN checks k USING(run_id)"
                " WHERE r.epoch >= ? ORDER BY r.epoch, k.id"
            )
            return [list(r) for r in c.execute(q, (since,))]


CSV_HEADER = [
    "run_id",
    "started_at",
    "trigger",
    "overall",
    "check",
    "status",
    "duration_ms",
    "detail",
    "version",
    "provider_id",
    "model_id",
]
````

### FILE: `src/vero_monitor/web/dashboard.html`

````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vero Status</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Ccircle cx='8' cy='8' r='7' fill='%231f7a45'/%3E%3C/svg%3E">
<!--STATIC_DATA-->
<style>
:root{
  --ink:#1b2230; --mut:#5d6878; --line:#dde2ea; --paper:#ffffff; --soft:#f4f6f9; --card:#ffffff;
  --brand:#0a6aa1; --up:#1f7a45; --deg:#a8500b; --down:#9b1c2e; --unk:#b7bfcb;
  --up-bg:#e8f4ed; --deg-bg:#fbf0e6; --down-bg:#f8e7ea; --unk-bg:#f1f3f6;
  --sans:"IBM Plex Sans","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Consolas,"Courier New",monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ink:#e6eaf0; --mut:#9aa5b4; --line:#2c3441; --paper:#12161d; --soft:#1a2029; --card:#161b23;
    --brand:#4fa8dc; --up:#4cc38a; --deg:#e39a4b; --down:#f06b7f; --unk:#4a5363;
    --up-bg:#15291f; --deg-bg:#2e2214; --down-bg:#311a20; --unk-bg:#1d232c;
  }
}
:root[data-theme="dark"]{
  --ink:#e6eaf0; --mut:#9aa5b4; --line:#2c3441; --paper:#12161d; --soft:#1a2029; --card:#161b23;
  --brand:#4fa8dc; --up:#4cc38a; --deg:#e39a4b; --down:#f06b7f; --unk:#4a5363;
  --up-bg:#15291f; --deg-bg:#2e2214; --down-bg:#311a20; --unk-bg:#1d232c;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.5 var(--sans)}
.wrap{max-width:1180px;margin:0 auto;padding:22px 24px 48px}
header{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:flex-end;justify-content:space-between;
  padding-bottom:16px;border-bottom:1px solid var(--line)}
.kicker{font-size:12.5px;color:var(--mut)}
h1{font-size:24px;margin:2px 0 0;font-weight:700;letter-spacing:-.01em}
h2{font-size:15px;margin:0 0 2px}
.sub{font-size:12.5px;color:var(--mut);margin-bottom:10px}
.hright{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.pill{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;padding:4px 10px;border-radius:999px;
  border:1px solid var(--line);background:var(--soft);color:var(--mut)}
.dot{width:9px;height:9px;border-radius:50%;background:var(--unk);flex:none}
.pill.live .dot{background:var(--up);animation:pulse 2s infinite}
.pill.busy .dot{background:var(--brand);animation:pulse 1s infinite}
.pill.down .dot{background:var(--down)}
@keyframes pulse{50%{opacity:.35}}
@media (prefers-reduced-motion:reduce){.dot{animation:none!important}}
button,a.btn{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--card);color:var(--ink);
  border-radius:6px;padding:6px 12px;cursor:pointer;text-decoration:none;display:inline-block}
button.primary{background:var(--brand);border-color:var(--brand);color:#fff;font-weight:600}
button:disabled{opacity:.55;cursor:default}
button:focus-visible,a:focus-visible{outline:2px solid var(--brand);outline-offset:2px}
.hero{margin-top:18px;border-radius:10px;padding:20px 22px;display:flex;gap:18px;align-items:center;
  border:1px solid var(--line);background:var(--unk-bg)}
.hero .big{width:46px;height:46px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;
  color:#fff;font-weight:800;font-size:22px;background:var(--unk)}
.hero h2{font-size:22px;margin:0}
.hero .meta{color:var(--mut);font-size:13px;margin-top:2px}
.hero .why{margin-top:6px;font-size:13px}
.hero.s-up{background:var(--up-bg);border-color:color-mix(in srgb,var(--up) 35%,var(--line))} .hero.s-up .big{background:var(--up)}
.hero.s-degraded{background:var(--deg-bg);border-color:color-mix(in srgb,var(--deg) 35%,var(--line))} .hero.s-degraded .big{background:var(--deg)}
.hero.s-down{background:var(--down-bg);border-color:color-mix(in srgb,var(--down) 35%,var(--line))} .hero.s-down .big{background:var(--down)}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;min-width:0}
.comp .top{display:flex;align-items:center;gap:8px;font-weight:600}
.comp .st{margin-left:auto;font-size:12px;font-weight:600}
.comp .line{font-size:12.5px;color:var(--mut);margin-top:4px;overflow-wrap:anywhere}
.comp.off{opacity:.6}
.kpi .l{font-size:12px;color:var(--mut)}
.kpi .v{font-size:26px;font-weight:700;font-variant-numeric:tabular-nums}
.c-up{color:var(--up)} .c-degraded{color:var(--deg)} .c-down{color:var(--down)} .c-unknown{color:var(--mut)}
.bg-up{background:var(--up)} .bg-degraded{background:var(--deg)} .bg-down{background:var(--down)} .bg-unknown{background:var(--unk)}
.section{margin-top:14px}
.tl-head{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.seg button{border:0;border-radius:0;border-right:1px solid var(--line);padding:5px 11px}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--paper);font-weight:600}
.bars{display:flex;gap:2px;height:38px;margin:12px 0 4px;align-items:stretch}
.bars span{flex:1;border-radius:2px;min-width:1px}
.bars span:hover{outline:2px solid var(--ink);outline-offset:1px}
.axis{display:flex;justify-content:space-between;font-size:11.5px;color:var(--mut)}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--mut);margin-top:8px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;white-space:nowrap;vertical-align:top}
th{font-weight:600;color:var(--mut);font-size:12px}
td.n{text-align:right;font-variant-numeric:tabular-nums}
td.why{white-space:normal;min-width:220px;color:var(--mut)}
tr.new td{animation:flash 2.4s ease-out}
@keyframes flash{from{background:color-mix(in srgb,var(--brand) 18%,transparent)}to{background:transparent}}
.badge{display:inline-block;font-size:11.5px;font-weight:600;padding:1px 8px;border-radius:999px;border:1px solid currentColor}
.mini{display:inline-flex;gap:4px;align-items:center;margin-right:8px;font-size:12px;color:var(--mut)}
.mini .dot{width:8px;height:8px}
.empty{padding:22px 8px;text-align:center;color:var(--mut)}
footer{margin-top:22px;font-size:12px;color:var(--mut);display:flex;flex-wrap:wrap;gap:6px 18px}
footer code{font-family:var(--mono);font-size:11.5px}
.static-only{display:none}
body.static .live-only{display:none!important}
body.static .static-only{display:inline-flex}
@media (max-width:820px){.grid3{grid-template-columns:1fr}}
@media (max-width:560px){.wrap{padding:16px 16px 40px}.hero{padding:16px}.hero h2{font-size:19px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <div class="kicker">Quality AI Automation · ASPF-1578</div>
      <h1>Vero status</h1>
    </div>
    <div class="hright">
      <span class="pill live-only" id="live"><span class="dot"></span><span id="liveText">Connecting…</span></span>
      <span class="pill live-only"><span id="nextText">Next check: –</span></span>
      <span class="pill static-only"><span class="dot"></span><span id="staticText">Snapshot</span></span>
      <button class="primary live-only" id="runBtn" type="button">Check now</button>
      <a class="btn live-only" id="csvBtn" href="/api/export.csv">Export CSV</a>
      <button id="themeBtn" type="button" aria-label="Toggle light or dark theme">Theme</button>
    </div>
  </header>

  <section class="hero" id="hero" aria-live="polite">
    <div class="big" id="heroIcon">?</div>
    <div>
      <h2 id="heroTitle">Loading…</h2>
      <div class="meta" id="heroMeta"></div>
      <div class="why" id="heroWhy"></div>
    </div>
  </section>

  <section class="grid3" id="components" aria-label="Components"></section>
  <section class="grid3" id="kpis" aria-label="Availability"></section>

  <section class="card section">
    <div class="tl-head">
      <div><h2>Status over time</h2><div class="sub" id="tlSub">Each bar is the worst status in its time slot.</div></div>
      <div class="seg live-only" id="range" role="group" aria-label="Time range">
        <button type="button" data-h="1">1 h</button><button type="button" data-h="6">6 h</button>
        <button type="button" data-h="24">24 h</button><button type="button" data-h="168">7 d</button>
        <button type="button" data-h="720">30 d</button>
      </div>
    </div>
    <div class="bars" id="bars"></div>
    <div class="axis"><span id="axL"></span><span id="axR">now</span></div>
    <div class="legend">
      <span><i class="bg-up"></i>available</span><span><i class="bg-degraded"></i>degraded (slow, partial)</span>
      <span><i class="bg-down"></i>unavailable</span><span><i class="bg-unknown"></i>no check</span>
      <span id="counts"></span>
    </div>
  </section>

  <section class="card section">
    <h2>Incidents</h2>
    <div class="sub">Periods where Vero was not fully available, newest first.</div>
    <div class="tw"><table id="incidents"></table></div>
  </section>

  <section class="card section">
    <h2>Recent checks <span class="sub live-only">· live</span></h2>
    <div class="tw"><table id="recent"></table></div>
  </section>

  <footer id="foot"></footer>
</div>

<script>
(function(){
"use strict";
const STATIC = window.STATIC_DATA || null;
const $ = (id) => document.getElementById(id);
const S = {up:"available", degraded:"degraded", down:"unavailable", unknown:"no data"};
const TITLE = {up:"Vero is available", degraded:"Vero is degraded", down:"Vero is unavailable", unknown:"No check yet"};
const ICON = {up:"✓", degraded:"!", down:"×", unknown:"?"};
const COMP = {cli:["Vero CLI", "installed and starts (vero version)"],
              task:["Vero task", "end-to-end answer through the model"],
              chat:["Vero Chat", "MCP handshake (no model call)"]};
const state = {hours: 24, data: null, es: null, t: null, nextRun: null, running: false};
try { const h = +localStorage.getItem("vam.hours"); if ([1,6,24,168,720].includes(h)) state.hours = h; } catch(e){}
try { const t = localStorage.getItem("vam.theme"); if (t) document.documentElement.dataset.theme = t; } catch(e){}

const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const nowS = () => STATIC ? STATIC.now : Date.now()/1000;
function dur(s){ s = Math.max(0, Math.round(s)); if (s < 60) return s + " s"; if (s < 3600) return Math.round(s/60) + " min";
  if (s < 86400) { const h = Math.floor(s/3600), m = Math.round((s%3600)/60); return h + " h" + (m ? " " + m + " min" : ""); }
  const d = Math.floor(s/86400), h = Math.round((s%86400)/3600); return d + " d" + (h ? " " + h + " h" : ""); }
const ago = (e) => e ? dur(nowS() - e) + " ago" : "never";
const when = (e) => new Date(e*1000).toLocaleString(undefined,{month:"short",day:"2-digit",hour:"2-digit",minute:"2-digit"});
const pct = (v) => v == null ? "–" : (v >= 99.995 ? "100" : v.toFixed(v >= 99 ? 2 : 1)) + "%";
const pctClass = (v) => v == null ? "unknown" : v >= 99 ? "up" : v >= 95 ? "degraded" : "down";
const badge = (s) => `<span class="badge c-${esc(s)}">${esc(S[s] || s)}</span>`;
const secs = (ms) => ms == null ? "–" : (ms/1000).toFixed(ms < 10000 ? 1 : 0) + " s";

async function load(){
  if (STATIC) return render(STATIC);
  try { const r = await fetch("/api/status?hours=" + state.hours, {cache:"no-store"}); render(await r.json()); }
  catch(e){ setLive("down", "Server not reachable"); }
}
function reload(){ clearTimeout(state.t); state.t = setTimeout(load, 500); }

function render(d){
  state.data = d;
  document.querySelectorAll("#range button").forEach(b => b.setAttribute("aria-pressed", +b.dataset.h === state.hours));
  $("csvBtn").href = "/api/export.csv?hours=" + d.range_hours;
  const c = d.current, hero = $("hero");
  hero.className = "hero s-" + c.status;
  $("heroIcon").textContent = ICON[c.status];
  $("heroTitle").textContent = TITLE[c.status];
  const last = d.recent[0];
  $("heroMeta").textContent = c.since ? `since ${when(c.since)} (${dur(nowS() - c.since)}) · last check ${ago(last && last.epoch)}` : "Run a check to see the status.";
  $("heroWhy").textContent = (c.status !== "up" && last && last.reason) ? "Reason: " + last.reason : "";
  document.title = (c.status === "up" ? "✓ " : c.status === "unknown" ? "" : "⚠ ") + "Vero Status";

  $("components").innerHTML = ["cli","task","chat"].map(k => {
    const x = d.components[k] || {enabled:false}, s = x.enabled ? (x.status || "unknown") : "unknown";
    const facts = !x.enabled ? "not enabled" : [x.version, x.model_id && ("model " + x.model_id),
      x.duration_ms != null && ("took " + secs(x.duration_ms)), x.epoch && ("checked " + ago(x.epoch))].filter(Boolean).join(" · ");
    return `<div class="card comp${x.enabled ? "" : " off"}"><div class="top"><span class="dot bg-${s}"></span>${COMP[k][0]}
      <span class="st c-${s}">${x.enabled ? esc(S[s]) : "off"}</span></div>
      <div class="line">${COMP[k][1]}</div><div class="line">${esc(facts)}</div>
      ${x.enabled && x.detail ? `<div class="line c-${s}">${esc(x.detail)}</div>` : ""}</div>`;
  }).join("");

  $("kpis").innerHTML = [["Availability, last 24 h", d.availability["24h"]], ["Last 7 days", d.availability["7d"]],
    ["Last 30 days", d.availability["30d"]]].map(([l, v]) =>
    `<div class="card kpi"><div class="l">${l}</div><div class="v c-${pctClass(v)}">${pct(v)}</div></div>`).join("");

  const tl = d.timeline, slot = tl.length > 1 ? tl[1].t - tl[0].t : 0;
  $("bars").innerHTML = tl.map(b => `<span class="bg-${b.status}" title="${esc(when(b.t))} – ${esc(when(b.t + slot))}: ${esc(S[b.status])}${b.n ? ` (${b.n} check${b.n > 1 ? "s" : ""})` : ""}"></span>`).join("");
  $("axL").textContent = tl.length ? when(tl[0].t) : "";
  $("tlSub").textContent = `Each bar = ${dur(slot)}, coloured by the worst check in it.`;
  const n = d.counts; $("counts").textContent = `· ${n.up} available, ${n.degraded} degraded, ${n.down} unavailable`;

  $("incidents").innerHTML = d.incidents.length
    ? `<thead><tr><th>Started</th><th>Duration</th><th>Worst</th><th class="n">Checks</th><th>Reason</th></tr></thead><tbody>` +
      d.incidents.map(i => `<tr><td>${when(i.start)}</td><td>${dur(i.duration_s)}${i.end == null ? " · <b>ongoing</b>" : ""}</td>
        <td>${badge(i.worst)}</td><td class="n">${i.runs}</td><td class="why">${esc(i.reason)}</td></tr>`).join("") + "</tbody>"
    : `<tbody><tr><td class="empty">No incidents in this range.</td></tr></tbody>`;

  renderRecent(d.recent);
  footer(d);
  state.nextRun = d.state.next_run; setRunning(d.state.running); tick();
  if (STATIC) $("staticText").textContent = `Snapshot · ${d.range_hours >= 48 ? d.range_hours/24 + " d" : d.range_hours + " h"} · ${when(d.now)}`;
}

function row(r, isNew){
  const ck = (r.checks || []).map(c => `<span class="mini" title="${esc(c.check_name)}: ${esc(c.detail || S[c.status])}"><span class="dot bg-${esc(c.status)}"></span>${esc(c.check_name)}</span>`).join("");
  const task = (r.checks || []).find(c => c.check_name === "task");
  return `<tr${isNew ? ' class="new"' : ""}><td>${when(r.epoch)}</td><td>${badge(r.overall)}</td><td>${ck}</td>
    <td class="n">${task ? secs(task.duration_ms) : "–"}</td><td class="why">${esc(r.reason || "")}</td></tr>`;
}
function renderRecent(list){
  $("recent").innerHTML = `<thead><tr><th>Time</th><th>Result</th><th>Checks</th><th class="n">Task time</th><th>Reason</th></tr></thead><tbody>` +
    (list.length ? list.map(r => row(r, false)).join("") : `<tr><td colspan="5" class="empty">No checks yet. Click <b>Check now</b>.</td></tr>`) + "</tbody>";
}
function footer(d){
  const c = d.config;
  $("foot").innerHTML = [`Prompt <code>${esc(c.prompt)}</code>`, `Model <code>${esc(c.model)}</code>`,
    `Every ${c.interval_minutes} min (${d.state.scheduler === "dashboard" ? "dashboard timer" : "Task Scheduler"})`,
    `Task timeout ${c.task_timeout_s} s, slow above ${c.task_slow_s} s`, `vero-availability ${esc(d.tool_version)}`]
    .map(x => `<span>${x}</span>`).join("");
}

function setLive(cls, text){ $("live").className = "pill live-only " + cls; $("liveText").textContent = text; }
function setRunning(r){
  state.running = r; $("runBtn").disabled = !!r; $("runBtn").textContent = r ? "Checking…" : "Check now";
  if (state.es && state.es.readyState === 1) setLive(r ? "busy" : "live", r ? "Checking Vero…" : "Live");
}
function tick(){
  if (STATIC || !state.nextRun) { $("nextText").textContent = "Next check: –"; return; }
  const s = Math.max(0, Math.round(state.nextRun - Date.now()/1000));
  $("nextText").textContent = `Next check in ${Math.floor(s/60)}:${String(s%60).padStart(2,"0")}`;
}
function connect(){
  const es = new EventSource("/api/stream"); state.es = es;
  es.onopen = () => setRunning(state.running);
  es.onerror = () => setLive("down", "Reconnecting…");
  es.addEventListener("state", ev => { const s = JSON.parse(ev.data); state.nextRun = s.next_run; setRunning(s.running); tick(); });
  es.addEventListener("run", ev => {
    const r = JSON.parse(ev.data), tb = $("recent").tBodies[0];
    if (tb) { if (tb.querySelector(".empty")) tb.innerHTML = ""; tb.insertAdjacentHTML("afterbegin", row(r, true)); }
    reload();
  });
}

if (STATIC) { document.body.classList.add("static"); render(STATIC); }
else {
  document.querySelectorAll("#range button").forEach(b => b.addEventListener("click", () => {
    state.hours = +b.dataset.h; try { localStorage.setItem("vam.hours", state.hours); } catch(e){} load(); }));
  $("runBtn").addEventListener("click", async () => {
    setRunning(true);
    try { const r = await fetch("/api/check", {method:"POST"}); if (r.status >= 400 && r.status !== 409) setRunning(false); }
    catch(e){ setRunning(false); }
  });
  load().then(connect);
  setInterval(tick, 1000);
  setInterval(load, 60000);
}
$("themeBtn").addEventListener("click", () => {
  const cur = document.documentElement.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  const n = cur === "dark" ? "light" : "dark"; document.documentElement.dataset.theme = n;
  try { localStorage.setItem("vam.theme", n); } catch(e){}
});
})();
</script>
</body>
</html>
````

### FILE: `start_dashboard.bat`

````bat
@echo off
rem Opens the status page; starts it first if it is not running (keep this window open then).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py serve --open
pause
````

### FILE: `status.bat`

````bat
@echo off
rem Configuration, last result, status page and Task Scheduler state.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py status
pause
````

### FILE: `tests/__init__.py`

````python
"""Test package."""
````

### FILE: `tests/fixtures/.gitkeep`

````
# synthetic fixtures only
````

### FILE: `tests/fixtures/vero_task_stream.ndjson`

````
{"type":"task_started","taskId":"1790868292727"}
{"ts":1,"type":"say","say":"task","text":"Reply with exactly: OK","modelInfo":{"providerId":"bedrock","modelId":"us.anthropic.claude-haiku-4-5-20251001-v1:0","mode":"act"},"conversationHistoryIndex":-1}
{"ts":2,"type":"say","say":"api_req_started","text":"{\"request\":\"SYSTEM PROMPT secret-environment-block\"}","modelInfo":{"providerId":"bedrock","modelId":"us.anthropic.claude-haiku-4-5-20251001-v1:0","mode":"act"}}
{"ts":3,"type":"say","say":"reasoning","text":"thinking","partial":false}
{"ts":4,"type":"say","say":"text","text":"O","partial":true}
{"ts":5,"type":"say","say":"text","text":"OK","partial":false}
{"ts":6,"type":"say","say":"error","text":"[ERROR] You did not use a tool in your previous response!"}
{"ts":7,"type":"say","say":"completion_result","text":"OK","modelInfo":{"providerId":"bedrock","modelId":"us.anthropic.claude-haiku-4-5-20251001-v1:0","mode":"act"}}
````

### FILE: `tests/helpers.py`

````python
"""Shared test helpers. Tests never call the real Vero CLI or Vero Chat."""

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vero_monitor import config  # noqa: E402

FAKE = ROOT / "scripts" / "fake_vero.py"
FIXTURES = ROOT / "tests" / "fixtures"


def make_config(data_dir: Path, **over: Any) -> config.Config:
    """A valid config that runs the fake Vero CLI with the current Python."""
    raw: Dict[str, Any] = {
        "vero": {
            "command": sys.executable,
            "version_args": [str(FAKE), "version"],
            "task_args": [str(FAKE), "task", "--json", "-m", "{model}", "-t", "{timeout}", "-c", "{workdir}", "{prompt}"],
            "task_timeout_s": 5,
        },
        "thresholds_s": {"task_slow": 3},
        "schedule": {"interval_minutes": 2},
        "data_dir": str(data_dir),
    }
    return config.build(config.merge(raw, over), data_dir / "monitor.json")
````

### FILE: `tests/integration/__init__.py`

````python
"""Integration tests: fake Vero CLI, fake MCP server, real SQLite and HTTP."""
````

### FILE: `tests/integration/test_chat.py`

````python
"""Vero Chat check against a local fake MCP server."""

import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tests.helpers import make_config
from vero_monitor.checks.vero_chat import check_chat
from vero_monitor.domain import Status


class FakeMcp(BaseHTTPRequestHandler):
    mode = "sse"
    seen_auth = None

    def log_message(self, *a):
        pass

    def do_POST(self):
        FakeMcp.seen_auth = self.headers.get("Authorization")
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        assert body["method"] == "initialize"
        if self.mode == "401":
            self.send_response(401)
            self.end_headers()
            return
        msg = {"jsonrpc": "2.0", "id": 1, "result": {"serverInfo": {"name": "WChat MCP Server", "version": "4.0.3"}}}
        if self.mode == "error":
            msg = {"jsonrpc": "2.0", "id": 1, "error": {"code": -32600, "message": "bad request"}}
        data = (f"event: message\ndata: {json.dumps(msg)}\n\n" if self.mode != "html" else "<html>SSO</html>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class ChatCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), FakeMcp)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.srv.server_address[1]}/mcp"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = make_config(
            Path(self.tmp.name), checks={"chat": True}, chat={"url": self.url, "token_env": "VAM_TEST_TOKEN", "timeout_s": 5}
        )
        self.env = mock.patch.dict(os.environ, {"VAM_TEST_TOKEN": "tok-123"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def run_mode(self, mode):
        FakeMcp.mode = mode
        return check_chat(self.cfg)

    def test_handshake_up(self):
        r = self.run_mode("sse")
        self.assertEqual((r.status, r.version), (Status.UP, "WChat MCP Server 4.0.3"))
        self.assertEqual(FakeMcp.seen_auth, "Bearer tok-123")
        self.assertNotIn("tok-123", repr(r))

    def test_rejected_token(self):
        r = self.run_mode("401")
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("token rejected", r.detail)

    def test_mcp_error_and_non_mcp_reply(self):
        self.assertIn("bad request", self.run_mode("error").detail)
        self.assertIn("not an MCP", self.run_mode("html").detail)

    def test_missing_token_variable(self):
        os.environ.pop("VAM_TEST_TOKEN")
        r = check_chat(self.cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("VAM_TEST_TOKEN", r.detail)

    def test_unreachable(self):
        cfg = make_config(
            Path(self.tmp.name),
            checks={"chat": True},
            chat={"url": "http://127.0.0.1:9/mcp", "token_env": "VAM_TEST_TOKEN", "timeout_s": 2},
        )
        r = check_chat(cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("unreachable", r.detail)


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/integration/test_checks.py`

````python
"""The CLI checks against scripts/fake_vero.py in every failure mode."""

import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import make_config
from vero_monitor.checks import run_all
from vero_monitor.checks.vero_cli import check_cli, check_task
from vero_monitor.domain import Check, CheckResult, Status


class CliChecksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = make_config(Path(self.tmp.name))
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def mode(self, m, delay="0.05"):
        os.environ["FAKE_VERO_MODE"] = m
        os.environ["FAKE_VERO_DELAY"] = delay
        return check_task(self.cfg)

    def test_cli_up_with_version(self):
        r = check_cli(self.cfg)
        self.assertEqual((r.status, r.version), (Status.UP, "vero 2.3.3 (fake0000)"))

    def test_cli_missing(self):
        cfg = make_config(Path(self.tmp.name), vero={"command": "no-such-vero-xyz"})
        self.assertEqual(check_cli(cfg).status, Status.DOWN)
        self.assertIn("not found", check_task(cfg).detail)

    def test_task_up_reports_real_model(self):
        r = self.mode("ok")
        self.assertEqual(r.status, Status.UP, r.detail)
        self.assertEqual((r.provider_id, r.model_id), ("bedrock", self.cfg.vero.model))
        self.assertTrue((self.cfg.data_dir / "sandbox").is_dir())

    def test_task_slow_is_degraded(self):
        r = self.mode("ok", delay="3.2")  # threshold 3 s in make_config
        self.assertEqual(r.status, Status.DEGRADED)
        self.assertIn("slow", r.detail)

    def test_task_provider_down(self):
        r = self.mode("down")
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("provider unavailable", r.detail)

    def test_task_auth_error_secret_masked(self):
        r = self.mode("auth")
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("Unauthorized", r.detail)
        self.assertNotIn("abc123secret", r.detail)

    def test_no_completion_result_is_down(self):
        r = self.mode("nocompletion")
        self.assertEqual((r.status, r.detail), (Status.DOWN, "no completion_result"))

    def test_refusal_is_degraded_not_down(self):
        r = self.mode("refuse")
        self.assertEqual(r.status, Status.DEGRADED)
        self.assertIn("not with 'OK'", r.detail)

    def test_hang_is_killed_at_hard_limit(self):
        cfg = make_config(Path(self.tmp.name), vero={"task_timeout_s": 1})
        os.environ["FAKE_VERO_MODE"] = "hang"
        t0 = time.time()
        r = check_task(cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("no completion within 2 s", r.detail)
        self.assertLess(time.time() - t0, 6)

    def test_missing_json_flag_explained(self):
        cfg = make_config(Path(self.tmp.name), vero={"task_args": [self.cfg.vero.task_args[0], "task", "{prompt}"]})
        r = check_task(cfg)
        self.assertEqual(r.status, Status.DOWN)
        self.assertIn("--json", r.detail)


class RunAllTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_task_skipped_when_cli_down(self):
        cfg = make_config(Path(self.tmp.name), vero={"command": "no-such-vero-xyz"})
        res = run_all(cfg)
        self.assertEqual([(r.check, r.status) for r in res], [(Check.CLI, Status.DOWN), (Check.TASK, Status.DOWN)])
        self.assertIn("skipped", res[1].detail)

    def test_crashing_check_is_contained(self):
        cfg = make_config(Path(self.tmp.name))

        def boom(_):
            raise ValueError("bug")

        cli_up = lambda c: CheckResult(Check.CLI, Status.UP, 1.0)  # noqa: E731
        with mock.patch("vero_monitor.checks.check_task", boom), mock.patch(
            "vero_monitor.checks.check_cli", cli_up
        ), self.assertLogs("vero_monitor", "ERROR") as logs:
            res = run_all(cfg)
        self.assertIn("check task crashed", logs.output[0])
        self.assertEqual(res[-1].status, Status.DOWN)
        self.assertEqual(res[-1].detail, "monitor error: ValueError")


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/integration/test_runner_server.py`

````python
"""Run lifecycle (lock, store, manifest, privacy) and the HTTP status page."""

import json
import os
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tests.helpers import make_config
from vero_monitor.domain import Check, CheckResult, Status
from vero_monitor.report import payload, static_html
from vero_monitor.runner import RunLock, in_progress, run_once
from vero_monitor.scheduler import Loop
from vero_monitor.server import make_handler
from vero_monitor.store import Store


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = make_config(Path(self.tmp.name))
        self.store = Store(self.cfg.data_dir)
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_run_stores_and_writes_manifest(self):
        run = run_once(self.cfg, self.store, "manual")
        self.assertEqual(run.overall, Status.UP)
        self.assertRegex(run.run_id, r"^\d{8}-\d{4}-vero-availability$")
        m = json.loads(next((self.cfg.data_dir / "runs").rglob("*.json")).read_text())
        self.assertEqual(m["model"]["id"], self.cfg.vero.model)
        self.assertEqual([c["check"] for c in m["checks"]], ["cli", "task"])
        self.assertEqual(self.store.count(), 1)
        self.assertNotEqual(run_once(self.cfg, self.store, "manual").run_id, run.run_id)  # -2 suffix
        self.assertFalse(in_progress(self.cfg))

    def test_full_prompt_never_persisted(self):
        run_once(self.cfg, self.store, "manual")
        blobs = [p.read_bytes() for p in self.cfg.data_dir.rglob("*") if p.is_file()]
        self.assertFalse(any(b"FAKE-SECRET-api_req_started" in b for b in blobs))

    def test_lock_blocks_overlap_and_stale_lock_is_cleared(self):
        with RunLock(self.cfg.data_dir, 999) as held:
            self.assertTrue(held.held)
            self.assertTrue(in_progress(self.cfg))
            self.assertIsNone(run_once(self.cfg, self.store, "manual"))
        lock = self.cfg.data_dir / "run.lock"
        lock.write_text("1")
        old = time.time() - 99999
        os.utime(lock, (old, old))
        self.assertFalse(in_progress(self.cfg))
        self.assertIsNotNone(run_once(self.cfg, self.store, "manual"))

    def test_down_run_reason_and_prune(self):
        down = [CheckResult(Check.CLI, Status.UP, 1.0), CheckResult(Check.TASK, Status.DOWN, 5.0, "provider unavailable")]
        run_once(self.cfg, self.store, "manual", checker=lambda c: down)
        r = self.store.runs(limit=1)[0]
        self.assertEqual((r["overall"], r["reason"]), ("down", "task: provider unavailable"))
        self.assertEqual(len(r["checks"]), 2)
        self.assertEqual(self.store.prune(1, now=time.time() + 3 * 86400), 1)
        self.assertEqual(self.store.csv_rows(), [])  # checks removed with their run (cascade)

    def test_payload_and_static_report(self):
        run_once(self.cfg, self.store, "manual", checker=lambda c: [CheckResult(Check.TASK, Status.DOWN, 1.0, "</script><x>")])
        d = payload(self.cfg, self.store, 24)
        self.assertEqual(d["current"]["status"], "down")
        self.assertEqual(len(d["timeline"]), 96)
        self.assertEqual(d["availability"]["24h"], 0.0)
        self.assertEqual(d["incidents"][0]["end"], None)
        html = static_html(self.cfg, self.store, 24)
        blob = html.split("window.STATIC_DATA=", 1)[1].split(";</script>", 1)[0]
        self.assertNotIn("<", blob)
        self.assertEqual(json.loads(blob)["recent"][0]["reason"], "task: </script><x>")


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        port = free_port()
        self.cfg = make_config(Path(self.tmp.name), server={"host": "127.0.0.1", "port": port})
        self.store = Store(self.cfg.data_dir)
        self.loop = Loop(self.cfg, self.store)
        self.srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(self.cfg, self.store, self.loop))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{port}"
        self.env = mock.patch.dict(os.environ, {"FAKE_VERO_DELAY": "0.05", "FAKE_VERO_MODE": "ok"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()

    def status(self, path, method="GET", **headers):
        try:
            return urllib.request.urlopen(urllib.request.Request(self.base + path, method=method, headers=headers)).status
        except urllib.error.HTTPError as e:
            return e.code

    def get_json(self, path):
        with urllib.request.urlopen(self.base + path) as r:
            return json.load(r)

    def test_pages_and_api(self):
        with urllib.request.urlopen(self.base + "/") as r:
            self.assertIn(b"Vero status", r.read())
        d = self.get_json("/api/status?hours=6")
        self.assertEqual((d["range_hours"], d["current"]["status"]), (6, "unknown"))
        self.assertEqual(self.get_json("/api/status?hours=abc")["range_hours"], 24)
        self.assertEqual(self.get_json("/api/health")["app"], "vero-availability")
        self.assertEqual(self.status("/nope"), 404)

    def test_security_checks(self):
        self.assertEqual(self.status("/api/health", Host="evil.example"), 403)
        self.assertEqual(self.status("/api/check", "POST", Origin="http://evil.example"), 403)

    def test_check_now_then_csv(self):
        self.assertEqual(self.status("/api/check", "POST", Origin=self.base), 202)
        for _ in range(60):
            if self.store.count() == 1 and not self.loop.running:
                break
            time.sleep(0.1)
        self.assertEqual(self.store.count(), 1)
        with urllib.request.urlopen(self.base + "/api/export.csv") as r:
            self.assertEqual(r.read().decode().count("\n"), 3)  # header + cli + task


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/unit/__init__.py`

````python
"""Unit tests: pure logic, no processes, no network."""
````

### FILE: `tests/unit/test_config.py`

````python
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import tests.helpers  # noqa: F401
from vero_monitor import config
from vero_monitor.config import ConfigError


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, obj, bom=False):
        p = self.dir / "c.json"
        p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + json.dumps(obj).encode())
        return p

    def test_example_file_is_valid_and_equals_defaults(self):
        cfg = config.load(config.EXAMPLE_FILE)
        self.assertEqual(config.read_json(config.EXAMPLE_FILE), config.DEFAULTS)
        self.assertEqual((cfg.interval_minutes, cfg.vero.task_timeout_s, cfg.port), (15, 180, 8766))
        self.assertIn("--json", cfg.vero.task_args)
        self.assertNotIn("--yolo", cfg.vero.task_args)

    def test_notepad_bom(self):
        self.assertEqual(config.load(self.write({}, bom=True)).vero.command, "vero")

    def test_invalid_values(self):
        bad = [
            {"schedule": {"interval_minutes": "abc"}},
            {"schedule": {"interval_minutes": 0}},
            {"schedule": {"interval_minutes": 2000}},
            {"vero": {"task_args": ["task"]}},  # no {prompt}
            {"vero": {"task_args": "task --json"}},  # not a list
            {"vero": {"command": " "}},
            {"checks": {"cli": False, "task": False, "chat": False}},
            {"checks": {"task": "yes"}},
            {"schedule": {"interval_minutes": 3}},  # 180 s task cannot fit in 3 min
            {"retention_days": -1},
            {"vero": {"env": []}},
        ]
        for b in bad:
            with self.assertRaises(ConfigError, msg=b):
                config.load(self.write(b))

    def test_broken_json_and_hint(self):
        p = self.dir / "c.json"
        p.write_text('{"data_dir": "C:\\Tools\\x"}')
        with self.assertRaisesRegex(ConfigError, "Windows paths"):
            config.load(p)
        p.write_text("[1]")
        with self.assertRaisesRegex(ConfigError, "object"):
            config.load(p)

    def test_missing_file(self):
        with self.assertRaisesRegex(ConfigError, "not found"):
            config.load(self.dir / "nope.json")

    def test_data_dir_relative_and_env(self):
        self.assertEqual(config.load(self.write({})).data_dir, config.ROOT / "data")
        var = "%VAM_T%" if os.name == "nt" else "$VAM_T"
        with mock.patch.dict(os.environ, {"VAM_T": str(self.dir)}):
            self.assertEqual(config.load(self.write({"data_dir": f"{var}/d"})).data_dir, self.dir / "d")

    def test_public_view_has_no_secrets(self):
        cfg = config.load(self.write({"vero": {"env": {"AWS_SECRET": "s3cr3t"}}, "checks": {"chat": True}}))
        text = json.dumps(cfg.public())
        self.assertNotIn("s3cr3t", text)
        self.assertNotIn("token_env", text)


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/unit/test_domain.py`

````python
import unittest

import tests.helpers  # noqa: F401  (sets sys.path)
from vero_monitor.domain import (
    Check,
    CheckResult,
    Point,
    Status,
    availability_percent,
    current_since,
    incidents,
    overall_status,
    timeline,
    worst,
)

U, D, X, N = Status.UP, Status.DEGRADED, Status.DOWN, Status.UNKNOWN


def cr(check, status, detail=""):
    return CheckResult(check, status, 1.0, detail)


class WorstTest(unittest.TestCase):
    def test_order(self):
        self.assertIs(worst([]), N)
        self.assertIs(worst([U, D]), D)
        self.assertIs(worst([U, X, D]), X)
        self.assertIs(worst([N, U]), U)


class OverallStatusTest(unittest.TestCase):
    def test_empty_is_unknown(self):
        self.assertIs(overall_status([]), N)

    def test_all_up(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.TASK, U)]), U)

    def test_task_down_means_down(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.TASK, X)]), X)

    def test_task_slow_means_degraded(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.TASK, D)]), D)

    def test_secondary_down_only_degrades(self):
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.CHAT, X), cr(Check.TASK, U)]), D)

    def test_cli_is_primary_when_no_task(self):
        self.assertIs(overall_status([cr(Check.CLI, X), cr(Check.CHAT, U)]), X)
        self.assertIs(overall_status([cr(Check.CLI, U), cr(Check.CHAT, X)]), D)

    def test_chat_only(self):
        self.assertIs(overall_status([cr(Check.CHAT, X)]), X)


class AvailabilityTest(unittest.TestCase):
    def test_degraded_counts_as_available(self):
        self.assertEqual(availability_percent([U, D, X, U]), 75.0)

    def test_unknown_ignored_and_empty(self):
        self.assertIsNone(availability_percent([]))
        self.assertIsNone(availability_percent([N, N]))
        self.assertEqual(availability_percent([U, N]), 100.0)


class IncidentsTest(unittest.TestCase):
    def test_groups_consecutive_bad_runs(self):
        pts = [Point(0, U), Point(10, X, "task: timeout"), Point(20, D, "slow"), Point(30, U), Point(40, D, "slow"), Point(50, U)]
        inc = incidents(pts, min_degraded_runs=1)
        self.assertEqual(len(inc), 2)
        self.assertEqual((inc[0].start, inc[0].end, inc[0].worst, inc[0].runs), (10, 30, X, 2))
        self.assertEqual(inc[0].reason, "task: timeout")  # reason of the worst run
        self.assertEqual(inc[0].duration_s(now=99), 20)

    def test_single_slow_run_is_not_an_incident(self):
        pts = [Point(0, U), Point(10, D, "slow"), Point(20, U), Point(30, D), Point(40, D), Point(50, U)]
        inc = incidents(pts)
        self.assertEqual([(i.start, i.runs) for i in inc], [(30, 2)])
        self.assertEqual(len(incidents(pts, min_degraded_runs=1)), 2)

    def test_ongoing_incident(self):
        inc = incidents([Point(0, U), Point(10, X, "down")])
        self.assertIsNone(inc[0].end)
        self.assertEqual(inc[0].duration_s(now=70), 60)

    def test_unsorted_input_and_no_incident(self):
        self.assertEqual(incidents([Point(30, U), Point(10, U)]), [])
        self.assertEqual(len(incidents([Point(20, U), Point(10, X)])), 1)


class TimelineTest(unittest.TestCase):
    def test_worst_per_bin_and_empty_bins(self):
        pts = [Point(1, U), Point(2, X), Point(15, U), Point(29.9, D)]
        bins = timeline(pts, 0, 30, 3)
        self.assertEqual([(t, s, n) for t, s, n in bins], [(0, X, 2), (10, U, 1), (20, D, 1)])
        self.assertIs(timeline([], 0, 30, 3)[0][1], N)

    def test_outside_range_and_bad_args(self):
        self.assertEqual(timeline([Point(-1, X), Point(30, X)], 0, 30, 3)[0][2], 0)
        self.assertEqual(timeline([], 10, 10, 3), [])
        self.assertEqual(timeline([], 0, 10, 0), [])


class CurrentSinceTest(unittest.TestCase):
    def test_since_first_of_trailing_streak(self):
        self.assertEqual(current_since([Point(0, U), Point(10, X), Point(20, X)]), (X, 10))
        self.assertEqual(current_since([Point(20, U), Point(0, U)]), (U, 0))
        self.assertEqual(current_since([]), (N, None))


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/unit/test_parsers.py`

````python
import unittest
from pathlib import Path

from tests.helpers import FIXTURES, make_config
from vero_monitor.checks.vero_chat import parse_reply
from vero_monitor.checks.vero_cli import clean, hard_limit_s, parse_stream, task_command


class StreamParserTest(unittest.TestCase):
    def test_real_stream_from_integration_guide(self):
        s = parse_stream((FIXTURES / "vero_task_stream.ndjson").read_text().splitlines())
        self.assertEqual(s.task_id, "1790868292727")
        self.assertEqual(s.completion, "OK")
        self.assertEqual(s.provider_id, "bedrock")
        self.assertEqual(s.model_id, "us.anthropic.claude-haiku-4-5-20251001-v1:0")
        self.assertEqual(s.events, 8)

    def test_only_completion_result_is_the_answer(self):
        s = parse_stream(['{"type":"say","say":"text","text":"OK","partial":false}'])
        self.assertIsNone(s.completion)

    def test_partial_completion_ignored(self):
        s = parse_stream(['{"type":"say","say":"completion_result","text":"O","partial":true}'])
        self.assertIsNone(s.completion)

    def test_garbage_lines_ignored(self):
        s = parse_stream(["", "Vero banner", "{not json", "[1,2]", '"str"', '{"type":"task_started","taskId":7}'])
        self.assertEqual((s.task_id, s.events), ("7", 1))

    def test_error_event_captured_and_cleaned(self):
        s = parse_stream(['{"type":"error","message":"Unauthorized   Bearer abc.def"}'])
        self.assertEqual(s.error, "Unauthorized [masked]")


class CleanTest(unittest.TestCase):
    def test_masks_credentials_and_flattens(self):
        self.assertEqual(clean("a\n  b\tc"), "a b c")
        for secret in ("Bearer eyJabc", "token=abc123", "token: abc", "password=hunter2", "aws_secret_access_key=x"):
            self.assertNotIn(secret.split()[-1].split("=")[-1].split(":")[-1].strip(), clean(f"err {secret} end"))

    def test_length_limited(self):
        self.assertEqual(len(clean("x" * 1000)), 200)


class TaskCommandTest(unittest.TestCase):
    def test_placeholders_filled(self):
        cfg = make_config(
            Path("/tmp/x"),
            vero={
                "command": "vero",
                "task_args": ["task", "--json", "-m", "{model}", "-t", "{timeout}", "-c", "{workdir}", "{prompt}"],
                "task_timeout_s": 180,
            },
            schedule={"interval_minutes": 15},
        )
        args = task_command(cfg, "C:/vero.cmd", Path("/w"))
        self.assertEqual(
            args,
            ["C:/vero.cmd", "task", "--json", "-m", cfg.vero.model, "-t", "180", "-c", str(Path("/w")), "Reply with exactly: OK"],
        )
        self.assertNotIn("--yolo", args)  # never auto-approve (ADR-003)
        self.assertEqual(hard_limit_s(cfg), 210)


class McpReplyTest(unittest.TestCase):
    def test_plain_json(self):
        self.assertEqual(parse_reply('{"jsonrpc":"2.0","id":1,"result":{}}'), {"jsonrpc": "2.0", "id": 1, "result": {}})

    def test_sse(self):
        body = 'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{"serverInfo":{"name":"WChat MCP Server"}}}\n\n'
        self.assertEqual(parse_reply(body)["result"]["serverInfo"]["name"], "WChat MCP Server")

    def test_error_and_garbage(self):
        self.assertIn("error", parse_reply('data: {"jsonrpc":"2.0","id":1,"error":{"message":"bad"}}'))
        self.assertIsNone(parse_reply("<html>login page</html>"))
        self.assertIsNone(parse_reply('{"jsonrpc":"2.0"}'))


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/unit/test_scheduler.py`

````python
import unittest
import xml.etree.ElementTree as ET

import tests.helpers  # noqa: F401
from vero_monitor import scheduler

NS = "{http://schemas.microsoft.com/windows/2004/02/mit/task}"


def parse(xml):
    return ET.fromstring(xml.split("\n", 1)[1])


class TaskXmlTest(unittest.TestCase):
    def test_check_task_laptop_safe(self):
        root = parse(scheduler.probe_task_xml(15))
        s = root.find(f"{NS}Settings")
        for tag, val in (
            ("DisallowStartIfOnBatteries", "false"),
            ("StopIfGoingOnBatteries", "false"),
            ("StartWhenAvailable", "true"),
            ("MultipleInstancesPolicy", "IgnoreNew"),
            ("ExecutionTimeLimit", "PT1H"),
        ):
            self.assertEqual(s.find(NS + tag).text, val, tag)
        self.assertEqual(root.find(f".//{NS}Repetition/{NS}Interval").text, "PT15M")
        args = root.find(f".//{NS}Exec/{NS}Arguments").text
        self.assertIn("vam.py", args)
        self.assertIn("check --trigger task", args)
        self.assertEqual(root.find(f".//{NS}RunLevel").text, "LeastPrivilege")

    def test_dashboard_task(self):
        root = parse(scheduler.dashboard_task_xml())
        self.assertIsNotNone(root.find(f".//{NS}LogonTrigger"))
        self.assertEqual(root.find(f".//{NS}ExecutionTimeLimit").text, "PT0S")
        self.assertIn("serve --no-scheduler", root.find(f".//{NS}Exec/{NS}Arguments").text)

    def test_names_differ_from_the_old_latency_monitor(self):
        self.assertNotIn("Latency", scheduler.PROBE_TASK + scheduler.DASH_TASK)

    def test_cron_and_alignment(self):
        self.assertEqual(scheduler._cron_expr(15), "*/15 * * * *")
        self.assertEqual(scheduler._cron_expr(120), "0 */2 * * *")
        self.assertEqual(scheduler.next_aligned(900, 1000), 1800)
        self.assertEqual(scheduler.next_aligned(900, 1800), 2700)


if __name__ == "__main__":
    unittest.main()
````

### FILE: `uninstall.bat`

````bat
@echo off
rem Removes the scheduled tasks and the desktop shortcut. Data and config stay.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py uninstall
pause
````

### FILE: `vam.py`

````python
#!/usr/bin/env python3
"""Entry point. No install needed: python vam.py <command>."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from vero_monitor.cli import main

if __name__ == "__main__":
    sys.exit(main())
````

---

## Verify the rebuild

Save as `verify_rebuild.py` (outside the project folder) and run it as described in step 5.

````python
import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vero-availability-monitor")
md = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "REBUILD.md").read_text(encoding="utf-8")
manifest = json.loads(re.search(r"<!-- MANIFEST\n(.*?)\n-->", md, re.S).group(1))
bad = 0
for path, info in manifest["files"].items():
    p = root / path
    if not p.exists():
        print("MISSING ", path); bad += 1; continue
    text = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != info["sha256_lf"]:
        print("DIFFERENT", path); bad += 1
    elif info["crlf"] and b"\r\n" not in p.read_bytes():
        p.write_bytes(text.replace("\n", "\r\n").encode("utf-8")); print("fixed CRLF", path)
print("OK: all files match" if not bad else f"{bad} file(s) wrong: recreate them from the document")
sys.exit(1 if bad else 0)
````

<!-- MANIFEST
{
 "version": "3.0.0",
 "files": {
  ".ci/README.md": {
   "sha256_lf": "84f4caf43cc1c411273eeab9ba9ded9054a8595c6ef8a85b68bab0d1ee383076",
   "crlf": false,
   "bytes": 194
  },
  ".gitattributes": {
   "sha256_lf": "de5647982a8a835e7449c0a776bc039927e23530e9bdc1d588961500bb5af61f",
   "crlf": false,
   "bytes": 134
  },
  ".gitignore": {
   "sha256_lf": "7756a240e02140de687ed2f99bc4d70c8e1befd9764916064fb9e7eb4aa2d93c",
   "crlf": false,
   "bytes": 209
  },
  "AGENTS.md": {
   "sha256_lf": "44800f1ef26c843a15ceeeddf9569021a991c36318777ed97ab7e9454e57d8bb",
   "crlf": false,
   "bytes": 1423
  },
  "CHANGELOG.md": {
   "sha256_lf": "0cec48b50388071f2751a90f51a2b4a8eb7361e4f00512cc68c4e320851e8e3e",
   "crlf": false,
   "bytes": 1325
  },
  "CODEOWNERS": {
   "sha256_lf": "695a47f89d8c85232ee4946424a5f6a87f2fcea7a945bbc6abb6701981b09d44",
   "crlf": false,
   "bytes": 61
  },
  "CONTRIBUTING.md": {
   "sha256_lf": "0309ecb3676545058b6c326e9f4c90ba88b4e62f484b74c59b774d0c55f0fdef",
   "crlf": false,
   "bytes": 502
  },
  "README.md": {
   "sha256_lf": "bbdf950dc7b1985c130f6def9c6ca51e3d5afb5f617b399fd1efca49a12794ef",
   "crlf": false,
   "bytes": 1983
  },
  "START_HERE.txt": {
   "sha256_lf": "a6edd8fc74e409645f6c70c0c5b2393b75d4063c71da698deaae3394cbc0fe2f",
   "crlf": true,
   "bytes": 1386
  },
  "VERO_CONTEXT.md": {
   "sha256_lf": "e62427487f95e67c6894698b3244ffaa826825f59967b46caee15dadec5a9775",
   "crlf": false,
   "bytes": 9540
  },
  "check_now.bat": {
   "sha256_lf": "4bb4f1d8e7f19ffdc273ca2b4809be61f6d0644faba3bd4a1a7d8e5a81581748",
   "crlf": true,
   "bytes": 154
  },
  "config/monitor.example.json": {
   "sha256_lf": "9e78c6a7a86a94f21d5a62e20e7ec1e3479765a568b3aa554066a50a0f740c35",
   "crlf": false,
   "bytes": 878
  },
  "docs/ARCHITECTURE.md": {
   "sha256_lf": "44ff1006d66b37dee2156ac7c4425ae2bbd2ea18fcbe0de5f205a2d8797cbb6a",
   "crlf": false,
   "bytes": 2230
  },
  "docs/DESIGN_SYSTEM.md": {
   "sha256_lf": "fee93a3b440e1dab0f5ab8d7c4e4e1e7ea2090fdf1e5ea5b559f9b959f7c9b22",
   "crlf": false,
   "bytes": 733
  },
  "docs/PRD.md": {
   "sha256_lf": "884cfd889e035fe1a5d5979df28f26e34f5cb9b545130c102d121e3a87a4fc61",
   "crlf": false,
   "bytes": 1490
  },
  "docs/decisions/ADR-001_stdlib-only.md": {
   "sha256_lf": "0e8be0912e36d2a913c3185ba34e08f57bc39ac457bd6eba1648fe048f4a00e8",
   "crlf": false,
   "bytes": 388
  },
  "docs/decisions/ADR-002_availability-not-latency.md": {
   "sha256_lf": "e1eba8243b818ec04e5da7d10e81b054b02ca52f7dd7f8c05cd41afefa91c297",
   "crlf": false,
   "bytes": 570
  },
  "docs/decisions/ADR-003_no-yolo-sandbox.md": {
   "sha256_lf": "8ddb2cab993e4b50ed65cc98427a18348a82bdacc43d7b9bab09398aa76dce72",
   "crlf": false,
   "bytes": 623
  },
  "docs/decisions/ADR-004_vero-chat-handshake.md": {
   "sha256_lf": "d2afb7b0b6032cf142e87684d8a8b6946d091dc021d94cfaa8a51f4c772dde6a",
   "crlf": false,
   "bytes": 635
  },
  "pyproject.toml": {
   "sha256_lf": "536774c15d69d08ec17acd662efa7ace556ac35d713c8a9fa5d38dc4831e0ee5",
   "crlf": false,
   "bytes": 1218
  },
  "requirements.txt": {
   "sha256_lf": "97a344f15656255459c548b3281186ad0860a97ae2c8d962911507d6102ec837",
   "crlf": false,
   "bytes": 106
  },
  "scripts/_py.bat": {
   "sha256_lf": "ee03008dcfe04647b013bb12a8f75bfaabc1c2ebbce3395986b8829ffdd9cc96",
   "crlf": true,
   "bytes": 580
  },
  "scripts/build_rebuild_md.py": {
   "sha256_lf": "d2630ee8d7d70ea5e6b533de0df3eeeef1ac32d115e34c772f4536277000bac0",
   "crlf": false,
   "bytes": 6550
  },
  "scripts/fake_vero.py": {
   "sha256_lf": "8ac166e8e0e0b845a37161c46ed3192ded0a91a35beb10222bfeac86289a6fd7",
   "crlf": false,
   "bytes": 2865
  },
  "scripts/seed_demo_data.py": {
   "sha256_lf": "de8000130adac8ddad6337cd3c3105120af9247814f2238cb89f535f6afe53f5",
   "crlf": false,
   "bytes": 2302
  },
  "setup.bat": {
   "sha256_lf": "1676ff1a7460c049868868237db86fba6173e107ea78a2f321b56f40b3ae02f6",
   "crlf": true,
   "bytes": 957
  },
  "setup_demo.bat": {
   "sha256_lf": "4881f05e4c2bfe053ed4d0cc03fe585ef4544b549d7e43a9f1b9b28291de648c",
   "crlf": true,
   "bytes": 372
  },
  "src/vero_monitor/__init__.py": {
   "sha256_lf": "c77b5ab0da53e27487203d17afb38f8dc9ba0c68a7962759827afd5c9c27aee6",
   "crlf": false,
   "bytes": 145
  },
  "src/vero_monitor/__main__.py": {
   "sha256_lf": "13a1a5b340cdcfc1902b62be90e508c7c71886000d5bf087e7854aadf09fb35e",
   "crlf": false,
   "bytes": 52
  },
  "src/vero_monitor/checks/__init__.py": {
   "sha256_lf": "4e22f94dd92edc74066e117897f3a52506ed23460fdcc8b42192aeee28a3fc38",
   "crlf": false,
   "bytes": 1593
  },
  "src/vero_monitor/checks/process.py": {
   "sha256_lf": "bfeb6ac9be3fe90a93c0cb0d68f4b1d121aac015d5154b8b7626a021c509fd94",
   "crlf": false,
   "bytes": 3188
  },
  "src/vero_monitor/checks/vero_chat.py": {
   "sha256_lf": "f08bf1bf4287d3ccb0e20395517fdd5f49481f91c0bedbab4373e4af4e9e9209",
   "crlf": false,
   "bytes": 3463
  },
  "src/vero_monitor/checks/vero_cli.py": {
   "sha256_lf": "3ddceef9910b68e3f54311b3996aff4e53d8175c82761e855231ad712c35efef",
   "crlf": false,
   "bytes": 5375
  },
  "src/vero_monitor/cli.py": {
   "sha256_lf": "4c4986cdc26cc381eff0ac137e195eb8105c238a196b138f2b2dc4f5dc8d5b56",
   "crlf": false,
   "bytes": 13105
  },
  "src/vero_monitor/config.py": {
   "sha256_lf": "e7d56144b413831fe7acef7313ec9ef7890f4750bdbc9753b4f07c5c636d1aec",
   "crlf": false,
   "bytes": 7586
  },
  "src/vero_monitor/domain.py": {
   "sha256_lf": "a6baf2d88794a41ffa5a50cfcdf60a8c0fe0556afe8e8621a556bb6474b0a2cd",
   "crlf": false,
   "bytes": 5100
  },
  "src/vero_monitor/report.py": {
   "sha256_lf": "ecf99cc7db72004040d9d44f247243b701d26e431bb30af6d1734221cbf5cbef",
   "crlf": false,
   "bytes": 3403
  },
  "src/vero_monitor/runner.py": {
   "sha256_lf": "9c72b7358f12d5c068731c7560eac9efe744f95008c68e3175235a9b5ca27834",
   "crlf": false,
   "bytes": 4826
  },
  "src/vero_monitor/scheduler.py": {
   "sha256_lf": "758cf1aba70498ae6a42afc6e603f77839af12855ed453bf3e9cb05a3c462b0b",
   "crlf": false,
   "bytes": 10977
  },
  "src/vero_monitor/server.py": {
   "sha256_lf": "42a1833e37c8f670a622242e5b6d6d8ffb7c685a20b25ab8ee88328256b58da6",
   "crlf": false,
   "bytes": 7423
  },
  "src/vero_monitor/store.py": {
   "sha256_lf": "b144a73706a236cc8bc60e847995175e4fc644cd8495ff497110845747de4e0a",
   "crlf": false,
   "bytes": 5943
  },
  "src/vero_monitor/web/dashboard.html": {
   "sha256_lf": "d43abb27805424ff80a82f8b157d7d76edcf9c18c09db758502daa3f1723b679",
   "crlf": false,
   "bytes": 18415
  },
  "start_dashboard.bat": {
   "sha256_lf": "c9b963844055acd44896d5c42375bf0b84e41edb5190aa65cdfa576dd6fa6b9b",
   "crlf": true,
   "bytes": 199
  },
  "status.bat": {
   "sha256_lf": "6a754b5b8c1f74cd0842a9641d535ea25baf4dd5349a1819ce56703e3c33d65b",
   "crlf": true,
   "bytes": 169
  },
  "tests/__init__.py": {
   "sha256_lf": "7e9af23c4d8769e855436c950c52874ef9d5ac0c36f24531913b3ca965d6860f",
   "crlf": false,
   "bytes": 20
  },
  "tests/fixtures/.gitkeep": {
   "sha256_lf": "2be8225f3a9ad9e9ee49e2dbc7a20ef74b7d127b93047271e68eb3ba7d3992ec",
   "crlf": false,
   "bytes": 26
  },
  "tests/fixtures/vero_task_stream.ndjson": {
   "sha256_lf": "e4018110354d711892f0e577d030159c43140f0e405edc88af74ccd2569a220b",
   "crlf": false,
   "bytes": 937
  },
  "tests/helpers.py": {
   "sha256_lf": "0b35f2b3014752b801454367100e14ba0b2744ee9fdb9ad8a4c6d0957d6a28e2",
   "crlf": false,
   "bytes": 1003
  },
  "tests/integration/__init__.py": {
   "sha256_lf": "629eee0283bc7304250576c851f51e068a0625c70ada33c06f5abb2e3f8dedbc",
   "crlf": false,
   "bytes": 79
  },
  "tests/integration/test_chat.py": {
   "sha256_lf": "4462c0068b40fc9d56a3800129a92653e849006c84976a65ed6c5345964133d4",
   "crlf": false,
   "bytes": 3559
  },
  "tests/integration/test_checks.py": {
   "sha256_lf": "d033eb5c33fbbed346aa1700d1ac3aafc9eafc67c5d67b9d03a9d052809592d6",
   "crlf": false,
   "bytes": 4391
  },
  "tests/integration/test_runner_server.py": {
   "sha256_lf": "3bd30361d1bed25273da1911bf7a96321d22ddbf21b52a123bc44e63d41311b3",
   "crlf": false,
   "bytes": 6369
  },
  "tests/unit/__init__.py": {
   "sha256_lf": "34d8097b45b98a68acd466b69b9ba1cec7b2d93164ec960b913db0795e38c290",
   "crlf": false,
   "bytes": 56
  },
  "tests/unit/test_config.py": {
   "sha256_lf": "b089b300e44f15cafe6b466898610440389f4cc31a61eda5660877c56b1d2a91",
   "crlf": false,
   "bytes": 3057
  },
  "tests/unit/test_domain.py": {
   "sha256_lf": "9401a448b001527ce750da702d1db15a9c27ccea51a2a4523d0b4c1b6c0339c2",
   "crlf": false,
   "bytes": 4177
  },
  "tests/unit/test_parsers.py": {
   "sha256_lf": "83b0765d6362af1683ef5d3d6452e3707bea16cd03deb240b2036bee96e2fb3a",
   "crlf": false,
   "bytes": 3486
  },
  "tests/unit/test_scheduler.py": {
   "sha256_lf": "6d6460ec569ce5a126ab5a706932b6c7b197f61854b171360fe65deb2a15d959",
   "crlf": false,
   "bytes": 1904
  },
  "uninstall.bat": {
   "sha256_lf": "bce5f932e3942a7e39f3611867464061e55713a513f0526388368abed454e464",
   "crlf": true,
   "bytes": 182
  },
  "vam.py": {
   "sha256_lf": "25f30ade67d0e13c78622e8bc991228535d2535de206892795e9da55f7d5f8f1",
   "crlf": false,
   "bytes": 273
  }
 }
}
-->
