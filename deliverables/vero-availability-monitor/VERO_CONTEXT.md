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
