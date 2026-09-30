# Vero Latency Monitor 0.2.0: complete source for rebuild

**What this is.** The full source of the Vero Latency Monitor (Jira ASPF-1578), a local tool that measures
Vero CLI response latency and shows it on a dashboard. It is sent as a readable document because archives
and scripts cannot be attached. Nothing in it runs by itself. Read it before rebuilding.

- 50 files, all plain text, Python 3.8+ standard library only (no downloads, no pip).
- The HTML guide `VeroLatencyMonitor_Guide.html` is sent separately; put it in `docs/`.
- `VERO_CONTEXT.md` (included below) explains the architecture, contracts and rules.

---

## Instructions for the AI assistant (Vero CLI or other)

You are asked to recreate a project folder **exactly** from this document.

1. Create the folder `vero-latency-monitor/` in the location the user gives you (default: `C:\Tools\`).
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
   `py verify_rebuild.py C:\Tools\vero-latency-monitor VeroLatencyMonitor_0.2.0_REBUILD.md`.
   It checks every file against its SHA-256 (computed on LF line endings) and fixes CRLF where needed.
   If it reports `DIFFERENT` or `MISSING`, recreate those files again from this document.
6. Then run the tests: `py -m unittest discover -s tests -t .` inside the folder. Expected: `OK`.
7. Report the result to the user, then tell them to double-click `setup.bat` (see `START_HERE.txt`).

Do not run `setup.bat`, `install` or the real Vero CLI yourself unless the user asks.

---

## File list

| # | Path | Bytes | Line endings | SHA-256 (LF) |
|---|------|------:|:---:|---|
| 1 | `.ci/README.md` | 149 | LF | `c7331553b5e31c71…` |
| 2 | `.gitattributes` | 134 | LF | `de5647982a8a835e…` |
| 3 | `.gitignore` | 218 | LF | `416e67dcddbe8c7f…` |
| 4 | `AGENTS.md` | 1109 | LF | `fe9507d613dff833…` |
| 5 | `CHANGELOG.md` | 1742 | LF | `cc17fa2ce01954d3…` |
| 6 | `CODEOWNERS` | 61 | LF | `695a47f89d8c8523…` |
| 7 | `CONTRIBUTING.md` | 502 | LF | `0309ecb367654505…` |
| 8 | `README.md` | 2566 | LF | `c9c6ee5418e93c1f…` |
| 9 | `START_HERE.txt` | 1732 | CRLF | `d4840467fef66d01…` |
| 10 | `VERO_CONTEXT.md` | 19520 | LF | `ab219a39bfbef8fd…` |
| 11 | `config/monitor.example.json` | 531 | LF | `3da8d546ccc8f200…` |
| 12 | `docs/ARCHITECTURE.md` | 1655 | LF | `94de02081ddc3170…` |
| 13 | `docs/DESIGN_SYSTEM.md` | 737 | LF | `8877714e9d2a498f…` |
| 14 | `docs/PRD.md` | 1520 | LF | `e25beba6eb3b42fd…` |
| 15 | `docs/decisions/ADR-001_stdlib-only.md` | 567 | LF | `dd1b3761a9e13cb3…` |
| 16 | `make_report.bat` | 328 | CRLF | `b4948903d8df357a…` |
| 17 | `pyproject.toml` | 410 | LF | `46ba6fd177292043…` |
| 18 | `requirements.txt` | 110 | LF | `7d1cbdb0672e2583…` |
| 19 | `run_probe_now.bat` | 156 | CRLF | `712230cb7ef6bd56…` |
| 20 | `scripts/_py.bat` | 580 | CRLF | `ee03008dcfe04647…` |
| 21 | `scripts/build_installer.py` | 3501 | LF | `8bd7751d0c093b5a…` |
| 22 | `scripts/build_rebuild_md.py` | 6308 | LF | `46d59fd833a57471…` |
| 23 | `scripts/build_zip.py` | 1031 | LF | `10dba058802fa29c…` |
| 24 | `scripts/fake_vero.py` | 1055 | LF | `abe86f859e2c1697…` |
| 25 | `scripts/seed_demo_data.py` | 2598 | LF | `9ba19baee3e2acee…` |
| 26 | `setup.bat` | 1032 | CRLF | `1dffffc96cc36da3…` |
| 27 | `setup_demo.bat` | 521 | CRLF | `3d97a5149f25f325…` |
| 28 | `src/vero_latency/__init__.py` | 94 | LF | `e13d2e358f1452e1…` |
| 29 | `src/vero_latency/__main__.py` | 52 | LF | `13a1a5b340cdcfc1…` |
| 30 | `src/vero_latency/cli.py` | 13714 | LF | `c2e6528228831697…` |
| 31 | `src/vero_latency/config.py` | 5078 | LF | `9a9e23f6f10b102f…` |
| 32 | `src/vero_latency/probe.py` | 10214 | LF | `a7a9992aec478991…` |
| 33 | `src/vero_latency/scheduler.py` | 10813 | LF | `64ac03085dba2d4f…` |
| 34 | `src/vero_latency/server.py` | 9595 | LF | `eea3f864378c5acd…` |
| 35 | `src/vero_latency/stats.py` | 2902 | LF | `084ebd913cb29e25…` |
| 36 | `src/vero_latency/store.py` | 4736 | LF | `84da7e7712698362…` |
| 37 | `src/vero_latency/web/dashboard.html` | 24962 | LF | `35d3753a015a508d…` |
| 38 | `start_dashboard.bat` | 204 | CRLF | `a0ef7a00d2e9d904…` |
| 39 | `status.bat` | 170 | CRLF | `ea4c52c488de2e5d…` |
| 40 | `tests/__init__.py` | 20 | LF | `7e9af23c4d8769e8…` |
| 41 | `tests/conftest.py` | 701 | LF | `1e4df448187414b5…` |
| 42 | `tests/fixtures/.gitkeep` | 52 | LF | `71bb90b3532c3bcf…` |
| 43 | `tests/integration/__init__.py` | 20 | LF | `7e9af23c4d8769e8…` |
| 44 | `tests/integration/test_cycle.py` | 6580 | LF | `9643f197833bee81…` |
| 45 | `tests/unit/__init__.py` | 20 | LF | `7e9af23c4d8769e8…` |
| 46 | `tests/unit/test_config_scheduler.py` | 5060 | LF | `c899211b3e0e5031…` |
| 47 | `tests/unit/test_probe.py` | 2338 | LF | `67151bdcba1bf058…` |
| 48 | `tests/unit/test_stats.py` | 1774 | LF | `670305fcc5159ace…` |
| 49 | `uninstall.bat` | 222 | CRLF | `adabbc2092e35048…` |
| 50 | `vlm.py` | 286 | LF | `624649a3a8499918…` |

---

## Files

### FILE: `.ci/README.md`

````markdown
# CI

Planned plan: `QAI-vero-latency-monitor-PRGATE` (install, lint, unit tests, secret scan).
Command: `python -m unittest discover -s tests -t .`
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
!*.env.example
*.log
.idea/
.vscode/
dist/
build/
*.egg-info/
.pytest_cache/
runs/
output/
data/
reports/
config/monitor.json
*.docx
*.xlsx
*.xls
*.pdf
*.pptx
data-demo/
````

### FILE: `AGENTS.md`

````markdown
# Agents: vero-latency-monitor

## Role
Measures Vero CLI response latency. It is not an AI agent itself: it calls the Vero CLI with one fixed prompt and times the call.

## Rules
- The probe prompt stays minimal and neutral ("Reply with OK") so it is the cheapest call and within Vero guardrails.
- Never store the model answer. Store only status, timings, exit code, answer length and a truncated error.
- No secrets in `config/monitor.json` or in Git. Credentials stay in the Vero CLI's own login or in environment variables.
- Every probe belongs to a run with a run_id `<YYYYMMDD-HHMM>-vero-latency` and a JSON run manifest.
- Run outputs (`data/`, `data-demo/`, `reports/`, `dist/`) are never committed.

## Tools allowed
Python 3.8+ standard library only (ADR-001). The Vero CLI as configured.

## For coding agents
- Code lives in `src/vero_latency/`; the dashboard is one file, `src/vero_latency/web/dashboard.html`.
- Run `python -m unittest discover -s tests -t .` before every commit. Tests use `scripts/fake_vero.py`, never the real CLI.
- Commit and PR title: `ASPF-1578: <imperative summary>`.
````

### FILE: `CHANGELOG.md`

````markdown
# Changelog

## Unreleased

## 0.2.0
- Distribution: single-file installer `vero_latency_monitor_setup_<version>.py` (scripts/build_installer.py)
  for channels that block .zip; plain text, SHA-256 checked, never touches config or data.
- Distribution: `VeroLatencyMonitor_<version>_REBUILD.md` (scripts/build_rebuild_md.py), the whole source as one
  readable Markdown document with AI rebuild instructions, SHA-256 manifest and a verify script; for channels
  that accept no archives and no scripts. Empty files got a one-line comment so every file round-trips exactly.

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
# vero-latency-monitor

Purpose: measure how fast the Vero CLI answers. It runs the cheapest possible prompt on a timer, records every result and shows it on a live dashboard.
Owner: << OWNER >> (Quality AI Automation, GenAI Group 3)
Jira: ASPF-1578 (AES SW Process Framework)
Rules: see the SCMP (SCMP_QualityAIAutomation) and CONTRIBUTING.md.

Full guide: [docs/VeroLatencyMonitor_Guide.html](docs/VeroLatencyMonitor_Guide.html) · AI context for Vero CLI: [VERO_CONTEXT.md](VERO_CONTEXT.md)

## Install (Windows, about 5 minutes)

Needs Python 3.8+ and nothing else: no pip install, no internet, no admin rights.

1. Get the folder into e.g. `C:\Tools\vero-latency-monitor\`: `git clone`, or `py vero_latency_monitor_setup_<version>.py C:\Tools` (single-file installer, no zip needed), or unzip, or let an AI assistant rebuild it from `VeroLatencyMonitor_<version>_REBUILD.md`.
2. Optional: `setup_demo.bat` shows the dashboard with a fake CLI and sample data.
3. `setup.bat`: answer the questions (Vero command, cheapest model, timing), it tests the CLI, then Y installs background monitoring:
   - task `VeroLatencyMonitor`: probe every N minutes (also on battery, catches up after sleep)
   - task `VeroLatencyDashboard`: dashboard at logon, hidden
   - desktop shortcut "Vero Latency Dashboard" -> http://127.0.0.1:8765/
4. Check any time with `status.bat`. Remove with `uninstall.bat` (data is kept).

## Commands

```
python vlm.py configure                guided configuration
python vlm.py doctor                   test the Vero CLI (nothing stored)
python vlm.py install | uninstall      OS scheduler + dashboard at logon + shortcut
python vlm.py status                   config, last run, dashboard, tasks
python vlm.py open                     open the running dashboard
python vlm.py serve [--open]           dashboard in this window (+ timer if not installed)
python vlm.py probe                    one probe cycle now
python vlm.py export [--hours N]       CSV
python vlm.py report [--hours N]       self-contained HTML report
python vlm.py init --demo              demo config (fake CLI, data-demo/)
```

## Develop

```
python -m unittest discover -s tests -t .     # tests use scripts/fake_vero.py only
python scripts/build_zip.py                    # dist/vero-latency-monitor-<version>.zip
python scripts/build_installer.py              # dist/vero_latency_monitor_setup_<version>.py (one text file, no zip)
python scripts/build_rebuild_md.py             # dist/VeroLatencyMonitor_<version>_REBUILD.md (source as a document an AI rebuilds)
```
````

### FILE: `START_HERE.txt`

````text
VERO LATENCY MONITOR  (ASPF-1578)
=================================

Measures how fast the Vero CLI answers, on a timer, with a live dashboard.
Needs Python 3.8+ only. No admin rights, no internet, nothing to install with pip.

0. If you received vero_latency_monitor_setup_0.2.0.py (single-file installer):
      py vero_latency_monitor_setup_0.2.0.py C:\Tools
   It creates C:\Tools\vero-latency-monitor with everything below.
   If you received VeroLatencyMonitor_0.2.0_REBUILD.md instead: ask Vero CLI (or another AI
   assistant) to follow the instructions at the top of that file and rebuild the project in C:\Tools.

1. Put this folder somewhere local and fixed, e.g.  C:\Tools\vero-latency-monitor
   (not Downloads, not a OneDrive folder, not inside the zip preview)

2. (optional) Double-click  setup_demo.bat   -> dashboard with a fake CLI and sample data

3. Double-click  setup.bat
     - answer the questions (Vero command, cheapest model, timing; Enter = default)
     - it tests the Vero CLI once per model
     - answer Y to install background monitoring
   The dashboard opens. Later use the desktop shortcut "Vero Latency Dashboard"
   or http://127.0.0.1:8765/

Other files:
   start_dashboard.bat   open the dashboard (starts it if needed)
   run_probe_now.bat     one measurement now
   status.bat            what is configured and running
   make_report.bat       HTML report of the last 7 days, for email
   uninstall.bat         remove scheduled tasks and shortcut (data is kept)

Full guide: docs\VeroLatencyMonitor_Guide.html
For Vero CLI / AI agents: VERO_CONTEXT.md (whole project in one file)
Problems:   status.bat, then data\monitor.log, then the guide, section 13.
````

### FILE: `VERO_CONTEXT.md`

````markdown
# VERO_CONTEXT: vero-latency-monitor

> **For the AI reading this:** this file describes the whole project so you can answer questions about it or change it safely without opening every file first.
> - Treat it as the source of truth for structure, contracts and rules.
> - When you are asked to change code, read the named file before editing it, and keep the rules in section 9.
> - Answer only from this file and the repository. If something is marked `<< TO CONFIRM >>`, say so; do not guess.

Example use: `vero -p "Read VERO_CONTEXT.md, then explain how a timeout is detected"` <!-- adapt the syntax to your Vero CLI -->

---

## 1. What it is

A small, standalone tool that measures **how fast the Vero CLI answers**.

The Vero CLI is the client's AI command line tool; it offers several models behind pre-defined guardrails. The monitor treats it as a black box:

1. It starts the CLI the same way a user or an agentic workflow would.
2. It sends the cheapest possible prompt, `Reply with OK`.
3. It measures the time until the CLI exits.
4. It records the result and shows it on a live local dashboard.

| Item | Value |
|---|---|
| Jira story | ASPF-1578, "As a Quality Lead, I want to monitor latency in the VERO CLI responses." (AES SW Process Framework) |
| Acceptance criteria | 1. execute the cheapest prompt · 2. time-trigger setup · 3. record and dashboard the data · 4. automated |
| Version | 0.2.0 (`src/vero_latency/__init__.py`) |
| Team | Quality AI Automation, GenAI Group 3 (NXP). Governed by the SCMP of ASPF-1619. |
| Runtime | Python 3.8+ **standard library only**, no pip packages (ADR-001). Windows 10/11 first; Linux and macOS work too. |
| Network | Local only. Dashboard on `http://127.0.0.1:8765`. No internet needed. |

---

## 2. File map

```
vero-latency-monitor/
├── START_HERE.txt              plain-text install steps for the person who opens the zip
├── VERO_CONTEXT.md             this file
├── README.md, AGENTS.md, CONTRIBUTING.md, CODEOWNERS, CHANGELOG.md   (SCMP skeleton)
├── pyproject.toml, requirements.txt (empty: stdlib only), .gitignore, .gitattributes
├── vlm.py                      entry point: adds src/ to sys.path, calls vero_latency.cli.main()
├── setup.bat                   guided setup: configure -> doctor -> [Y] install -> open
├── setup_demo.bat              demo: fake CLI + 7 days of sample data in data-demo/
├── start_dashboard.bat         serve --open (only opens the browser if a dashboard already runs)
├── run_probe_now.bat, status.bat, make_report.bat, uninstall.bat
├── config/
│   ├── monitor.example.json    template (in Git)
│   └── monitor.json            local settings (NOT in Git, created by setup)
├── src/vero_latency/
│   ├── __init__.py             __version__, COMPONENT = "vero-latency"
│   ├── __main__.py             python -m vero_latency
│   ├── cli.py                  argparse commands (section 6)
│   ├── config.py               load / validate / defaults / public_view
│   ├── probe.py                build command, time one call, classify, lock, run_cycle, manifest
│   ├── store.py                SQLite: tables runs, probes
│   ├── stats.py                percentile, summarize, bucket_seconds, series
│   ├── scheduler.py            in-process Loop; Task Scheduler XML / cron install; desktop shortcut
│   ├── server.py               HTTP server: dashboard, JSON API, SSE stream, static report
│   └── web/dashboard.html      the whole dashboard: one file, vanilla JS + inline SVG, no CDN
├── scripts/
│   ├── _py.bat                 finds Python 3.8+ (py -3, then python) and sets %PY%
│   ├── fake_vero.py            stand-in Vero CLI for the demo and tests
│   ├── seed_demo_data.py       writes 7 days of demo probes (only into data-demo/)
│   ├── build_zip.py            dist/vero-latency-monitor-<version>.zip
│   ├── build_installer.py      dist/vero_latency_monitor_setup_<version>.py (single-file installer)
│   └── build_rebuild_md.py     dist/VeroLatencyMonitor_<version>_REBUILD.md (whole source as a Markdown document)
├── tests/                      unittest; unit/ and integration/; the fake CLI only, never the real one
├── docs/
│   ├── VeroLatencyMonitor_Guide.html   full human guide (setup, config, troubleshooting, review log)
│   ├── PRD.md, ARCHITECTURE.md, DESIGN_SYSTEM.md
│   └── decisions/ADR-001_stdlib-only.md
└── data/                       created at run time, NOT in Git
    ├── latency.db              SQLite
    ├── monitor.log             rotating log (1 MB x 4)
    ├── probe.lock              exists only while a run is in progress
    └── runs/<YYYY-MM>/<run_id>.json   run manifests
```

---

## 3. How it works (data flow)

```
Trigger ──> run_cycle() ──> for each model: Vero CLI call, timed ──> SQLite + manifest ──> dashboard
```

**Triggers.** Any of:
- the Task Scheduler task `VeroLatencyMonitor` (cron on Linux/macOS);
- the in-process `Loop` while a dashboard window runs;
- the "Run probe now" button;
- `vlm.py probe`.

**Run (`probe.run_cycle`).**
1. Take the lock file `data/probe.lock`. If another run holds it, return `None` (skipped). A lock older than `timeout_s × models + 120 s` is stale and gets replaced.
2. Create a `run_id` in the form `<YYYYMMDD-HHMM>-vero-latency`, adding `-2`, `-3` … within the same minute.
3. Record the CLI version, from `cli.version_command`.
4. For each model:
   - build the command (`build_command`);
   - time it (`time_command`): total wall-clock time and time to the first non-empty output byte;
   - classify the result (`classify`);
   - insert a row into `probes`.
5. Finish the run, prune rows older than `retention_days`, and write the JSON manifest.

**Dashboard.**
- `server.py` serves `web/dashboard.html`.
- The page fetches `/api/dashboard`, then opens `/api/stream` (Server-Sent Events).
- The stream checks SQLite every 1.5 s and pushes new probes and the run state.

**Grid.** Runs are aligned to the clock (`scheduler.next_aligned`): :00, :15, :30 … for 15 minutes. Task Scheduler's start time uses the same grid, so the dashboard countdown is correct in both modes.

---

## 4. Measurement rules

| Status | Condition (in `probe.classify`) |
|---|---|
| `ok` | exit code 0 and the output contains `expect` (case-insensitive; default `"OK"`; `""` accepts any output) |
| `unexpected` | exit code 0 but `expect` is missing (a banner, a guardrail refusal, a different answer) |
| `error` | non-zero exit code, or the process could not start (not found) |
| `timeout` | no exit within `cli.timeout_s`; the **whole process tree** is killed (`taskkill /T /F` on Windows, `killpg` on POSIX) |

- `total_ms` is wall-clock time from spawn to exit, which is what a user waits for. `first_byte_ms` is the time to the first non-empty stdout chunk.
- Latency statistics (avg, min, p50, p95, p99, max, first-byte p50) use **ok probes only**.
- Availability = ok / all probes × 100.
- Percentiles use linear interpolation between closest ranks (the numpy default).
- Dashboard bands: below `warn` is green "ok"; from `warn` to below `crit` is amber "slow"; at `crit` or above is red "very slow". Breach counts use the same bands.
- The model answer is **never stored**, only its length (`out_chars`). Errors are cut to 300 characters.

---

## 5. Data contracts

### 5.1 Config: `config/monitor.json` (defaults in `config.DEFAULTS`)

```json
{
  "cli": {
    "command": ["vero", "-p", "{prompt}", "--model", "{model}"],
    "prompt_via": "arg",
    "timeout_s": 60,
    "version_command": ["vero", "--version"],
    "env": {}
  },
  "prompt": "Reply with OK",
  "expect": "OK",
  "models": [{ "id": "<< CHEAPEST MODEL ID >>", "label": "cheap" }],
  "schedule": { "interval_minutes": 15, "run_in_dashboard": true },
  "thresholds_ms": { "warn": 5000, "crit": 15000 },
  "retention_days": 90,
  "server": { "host": "127.0.0.1", "port": 8765 },
  "data_dir": "data"
}
```

**Command template.**
- `{prompt}` and `{model}` are placeholders.
- With `prompt_via: "stdin"`, every argument containing `{prompt}` is dropped and the prompt is written to stdin.
- An empty model id drops the `{model}` argument and the flag before it.
- `command[0]` is resolved with `shutil.which`, so `vero` finds `vero.cmd` or `vero.exe`.

**Validation** (`config.validate`). Any failure raises `ConfigError` with a readable message:
- `command` is a non-empty list of strings;
- `prompt_via` is `arg` or `stdin`;
- `timeout_s` > 0;
- model labels are unique;
- `interval_minutes` is 1 to 1440;
- 0 < warn ≤ crit;
- `retention_days` ≥ 1.

**Reading and paths.**
- The file is read as `utf-8-sig`, so Notepad's BOM is accepted.
- `data_dir` expands environment variables and `~`; a relative path is relative to the tool folder.
- `VLM_CONFIG` (environment variable) or `--config` selects another file.

`public_view(cfg)` is the only config the dashboard sees. It **never** includes `cli.env`.

### 5.2 SQLite: `data/latency.db` (WAL mode)

```sql
runs(run_id TEXT PK, started_at TEXT, finished_at TEXT, trigger TEXT, host TEXT,
     tool_version TEXT, cli_version TEXT, prompt_sha256 TEXT)
probes(id INTEGER PK AUTOINCREMENT, run_id TEXT, ts TEXT /*ISO UTC*/, epoch REAL, model TEXT /*label*/,
       model_id TEXT, status TEXT, total_ms REAL, first_byte_ms REAL, exit_code INTEGER,
       out_chars INTEGER, error TEXT)
-- indexes: probes(epoch), probes(model, epoch)
```

`trigger` is one of `manual`, `task`, `schedule`, `dashboard` (`demo` for seeded data). Every connection is opened, committed and closed per call (`Store._conn`).

### 5.3 Run manifest: `data/runs/<YYYY-MM>/<run_id>.json`

Same shape as the automation-code manifest in the SCMP, so AI measurements can be reproduced:

```json
{ "run_id": "20261005-1430-vero-latency", "component": "vero-latency", "tool_version": "0.2.0",
  "trigger": "task", "host": "LAPTOP", "started_at": "…Z", "finished_at": "…Z",
  "cli": {"name": "vero", "version": "vero 2.3.1"}, "prompt_sha256": "…",
  "models": [{"label": "cheap", "id": "…"}],
  "results": [{"model": "cheap", "status": "ok", "total_ms": 1843.2, "first_byte_ms": 1790.4, "exit_code": 0, "error": null}],
  "totals": {"probes": 1, "ok": 1, "failed": 0}, "availability_percent": 100.0 }
```

### 5.4 HTTP API: `server.py`

The server binds to `127.0.0.1` only.

| Endpoint | Returns |
|---|---|
| `GET /` | `web/dashboard.html` |
| `GET /api/dashboard?hours=&model=` | JSON: `generated_at, tool_version, range_hours, config (public_view), state{running, scheduler: "dashboard"\|"external", next_run_epoch, last_run}, overall (summary), per_model[], series{bucket_s, models{label:[{t,n,fail,p50,p95,avg}]}}, failures[≤50], recent[15]`. `hours` ∈ {1, 6, 24, 168, 720}, anything else becomes 24. |
| `GET /api/stream` | SSE. `event: probe` carries a full probe row; `event: state` carries `{running, next_run_epoch}`; `: ping` every 15 s. |
| `POST /api/probe` | 202 started · 409 already running · 403 foreign origin · 503 no loop |
| `GET /api/export.csv?hours=&model=` | CSV with the columns of `probes` |
| `GET /api/health` | `{"status":"up","app":"vero-latency","version":…}` (used to detect a running dashboard) |

**Security checks.**
- The `Host` header must be `127.0.0.1:<port>` or `localhost:<port>` (blocks DNS rebinding).
- A POST with an `Origin` header from another host gets 403, so no other website can spend tokens.
- Handler errors are logged and answered as JSON 500.

**Static report.** `static_report()` injects `window.STATIC_DATA=<payload>` into the dashboard HTML with every `<` escaped as `<`. The page then runs in static mode: no stream, no buttons, and times relative to `generated_at`.

---

## 6. Commands (`python vlm.py <command>`)

| Command | Does | Exit code |
|---|---|---|
| `configure` | Interactive questions (command, models, interval, timeout, warn, crit); writes the config. A broken or demo config restarts from the example. | 0 / 1 |
| `init [--demo] [--force]` | Copies the example. `--demo` uses `scripts/fake_vero.py`, 2 fake models, a 1-minute interval and `data_dir: data-demo`. | 0 |
| `doctor` | Checks the executable, the CLI version, and one probe per model **without storing anything**. Prints `RESULT ready` or `NOT READY`. | 0 ready / 1 |
| `probe [--trigger T] [-q]` | One `run_cycle`; prints the manifest. | 0; 2 if a probe failed (**always 0** with `--trigger task`) |
| `serve [--open] [--port] [--host] [--no-scheduler]` | Dashboard. It runs the in-process Loop only if `schedule.run_in_dashboard` is true and `--no-scheduler` is not given. If a dashboard already answers `/api/health`, it only opens the browser. | 0 / 1 (port busy) |
| `install [--every N] [--no-dashboard]` | Windows: registers 2 tasks from XML and adds a desktop `.url` shortcut. Linux/macOS: 2 crontab lines tagged `# vero-latency-monitor`. Sets `run_in_dashboard=false`. | 0 / 1 |
| `uninstall` | Ends and removes the tasks (or cron lines) and the shortcut; sets `run_in_dashboard=true`. Data is kept. | 0 |
| `status` | Version, config, data, last run, whether a run is in progress, dashboard up, task state | 0 |
| `open [--wait S]` | Waits until `/api/health` answers, then opens the browser | 0 / 1 |
| `export` / `report` | CSV / self-contained HTML (`report` defaults to 168 h) | 0 |

Global options: `--config <file>`, `-v` (DEBUG logging, including each HTTP request).

### Windows tasks created by `install` (`scheduler.py`)

| Task | Action | Key settings |
|---|---|---|
| `VeroLatencyMonitor` | `pythonw.exe vlm.py probe --trigger task --quiet`, repeating every N minutes from an aligned start | `DisallowStartIfOnBatteries=false`, `StopIfGoingOnBatteries=false`, `StartWhenAvailable=true`, `MultipleInstancesPolicy=IgnoreNew`, `ExecutionTimeLimit=PT1H`, InteractiveToken, LeastPrivilege |
| `VeroLatencyDashboard` | `pythonw.exe vlm.py serve --no-scheduler` at logon | `ExecutionTimeLimit=PT0S` (no limit), `RestartOnFailure` 3 × 1 min |

- The XML is written as UTF-16 to a temporary file, then registered with `schtasks /Create /XML`.
- `pythonw` means no console window. Every subprocess uses `CREATE_NO_WINDOW`.
- Under `pythonw`, `sys.stdout` is `None`, so logging goes only to `monitor.log`, and crashes are logged there.

---

## 7. Dashboard (`src/vero_latency/web/dashboard.html`)

**Layout.**
- **Header:** live pill (green live, blue probing, red reconnecting), next-run countdown ("(Task Scheduler)" in external mode), Run probe now, Export CSV, Theme.
- **Controls:** range 1 h / 6 h / 24 h / 7 d / 30 d (remembered in localStorage); model filter.
- **6 tiles:** last probe · p50 (+ average, first byte) · p95 (+ p99, max) · availability · probes/failures · threshold breaches.
- **Chart:** one colour per model. p50 solid and p95 dotted per bucket; warn and crit dashed lines when on scale; red ticks for failures; hover tooltip. Lines break across gaps longer than 2.5 × max(bucket, interval), and points are clamped to the plot area.
- **Tables:** per model; recent 15 (live rows are added from SSE); failures (hidden when there are none).

**Design tokens.** Same as the SCMP: ok `#1f7a45`, warn `#a8500b`, crit `#9b1c2e`, brand `#0a6aa1`, with a dark mode. Everything user-supplied is escaped with `esc()` before it goes into HTML.

---

## 8. Build, test, run

```bash
python -m unittest discover -s tests -t .      # 35 tests; Python 3.8–3.13; uses scripts/fake_vero.py
python scripts/build_zip.py                      # dist/vero-latency-monitor-<ver>.zip, root folder "vero-latency-monitor"
python scripts/build_installer.py                # dist/vero_latency_monitor_setup_<ver>.py: one plain-text file that
                                                 #   recreates the folder (SHA-256 checked); for channels without zip
python vlm.py init --demo && python scripts/seed_demo_data.py && python vlm.py serve --open   # demo
```

**Fake CLI switches** (environment variables):

| Variable | Effect |
|---|---|
| `FAKE_VERO_DELAY=<s>` | Fixed delay |
| `FAKE_VERO_FAIL=1` | Always fails (exit 3) |
| `FAKE_VERO_FAIL=0` | Never fails |
| unset | Random: about 3% failures and 4% slow answers |

`build_rebuild_md.py` also leaves out the HTML guide, which is sent separately. The zip, the installer and the rebuild document exclude `data/`, `data-demo/`, `reports/`, `dist/`, `config/monitor.json`, caches and logs.

---

## 9. Rules (do not break)

1. **Standard library only.** Nothing to pip-install, no CDN or external scripts in the HTML. It must keep running on Python 3.8, so no `match`, and no `X | Y` outside annotations.
2. **Never store secrets or model answers.** `cli.env` must never reach the dashboard, reports or logs.
3. **The probe prompt stays minimal and neutral** (cheapest call, guardrail-friendly). Changing it changes `prompt_sha256`, and old data is no longer comparable.
4. **Every probe belongs to a run** with a run_id and a manifest. Keep the manifest fields stable; they are an SCMP contract.
5. **Local only.** Keep the bind on 127.0.0.1 and keep the Host and Origin checks.
6. **Never run two probe runs at once.** Always go through `run_cycle`, which takes `RunLock`.
7. **Tests use the fake CLI only**, never the real Vero CLI (tokens, guardrails, credentials).
8. **Git:** commit and PR titles are `ASPF-1578: <imperative summary>`. Never commit `data/`, `data-demo/`, `reports/`, `dist/` or `config/monitor.json`. Update `CHANGELOG.md`, and update the guide and this file when behaviour changes.
9. **Windows first.** `.bat` files keep CRLF line endings. Every new subprocess needs `creationflags=NO_WINDOW`, and a timeout must kill the whole process tree.

---

## 10. Common tasks: where to change what

| Task | Change |
|---|---|
| Support a different Vero syntax | Config only: `cli.command` / `prompt_via` (or `vlm.py configure`). No code change. |
| Add a new metric per probe | `probe.run_cycle` (the probe dict) → `store.SCHEMA` (new column; add an `ALTER TABLE` migration for existing databases) → `store.PROBE_COLS` → `stats.summarize` → `dashboard.html` → tests |
| Add a dashboard tile | `renderKpis()` in `dashboard.html`; the data comes from `stats.summarize` via `/api/dashboard` |
| Alerts (email or Teams) | Out of scope for now (PRD). The natural hook is the end of `run_cycle`, after the manifest is written. |
| Change the default thresholds or interval | `config.DEFAULTS` and `config/monitor.example.json` (keep both the same) |
| New command | `cli.build_parser()` + a `cmd_*` function + the `HANDLERS` map; add a `.bat` file if users need it |
| Release | Bump `__version__` and `pyproject.toml`, add a CHANGELOG entry, run the tests, run `build_zip.py`, tag `v<X.Y.Z>` on main through a PR |

---

## 11. Open items (`<< TO CONFIRM >>`)

- The exact Vero CLI one-shot syntax and model-listing command (`vero --help`). The default `vero -p {prompt} --model {model}` is an assumption.
- The cheapest model id.
- The warn and crit thresholds (5 s and 15 s are placeholders; the Quality Lead decides).
- The owner name, and where the code lives in Bitbucket project QAI (its own repository or a folder in automation-code).
- The Windows `.bat` files and the Task Scheduler XML are covered by tests off Windows but still need a first run on a real Windows laptop.
````

### FILE: `config/monitor.example.json`

````json
{
  "cli": {
    "command": ["vero", "-p", "{prompt}", "--model", "{model}"],
    "prompt_via": "arg",
    "timeout_s": 60,
    "version_command": ["vero", "--version"],
    "env": {}
  },
  "prompt": "Reply with OK",
  "expect": "OK",
  "models": [
    { "id": "<< CHEAPEST MODEL ID >>", "label": "cheap" }
  ],
  "schedule": { "interval_minutes": 15, "run_in_dashboard": true },
  "thresholds_ms": { "warn": 5000, "crit": 15000 },
  "retention_days": 90,
  "server": { "host": "127.0.0.1", "port": 8765 },
  "data_dir": "data"
}
````

### FILE: `docs/ARCHITECTURE.md`

````markdown
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
| `scheduler.py` | in-process loop; Task Scheduler XML tasks (probe + dashboard at logon) or cron; desktop shortcut |
| `server.py` | local HTTP server: dashboard, JSON API, SSE live stream |
| `web/dashboard.html` | single-file dashboard, no external libraries |

## Data flow
Trigger (task / loop / button) -> lock file `data/probe.lock` -> `run_cycle` -> Vero CLI per model -> `probes` rows + `data/runs/<YYYY-MM>/<run_id>.json` -> `/api/dashboard` and `/api/stream` -> dashboard.

## Interfaces
- CLI: `python vlm.py configure|init|doctor|install|uninstall|status|open|serve|probe|export|report`
- HTTP (127.0.0.1:8765, Host and Origin checked): `GET /`, `GET /api/dashboard?hours=&model=`, `GET /api/stream` (SSE), `POST /api/probe`, `GET /api/export.csv`, `GET /api/health`
- Run manifest: run_id, component, tool_version, trigger, host, started/finished, cli version, prompt_sha256, models, results, totals, availability_percent

## Dependencies
Python 3.8+ standard library. Vero CLI (version recorded per run). Model id per probe recorded.
````

### FILE: `docs/DESIGN_SYSTEM.md`

````markdown
# Design system: vero-latency-monitor

## Colours
Same tokens as the SCMP: pass/ok green `#1f7a45`, warn amber `#a8500b`, fail/crit red `#9b1c2e`, n.a. grey `#8a94a3`, brand `#0a6aa1`. Series colours in fixed order per model. Dark mode redefines every token.

## Typography
IBM Plex Sans / Segoe UI, tabular numbers for figures.

## Components
KPI tile, line chart (p50 solid, p95 dotted, threshold dashed lines, failure ticks), status badge (ok / slow / very slow / error / timeout / unexpected), per-model table, live feed, live pill.

## Rules
Latency colour is set by the thresholds in config (below warn = green, warn to crit = amber, at or above crit = red). Latency figures use successful probes; availability counts every probe.
````

### FILE: `docs/PRD.md`

````markdown
# PRD: vero-latency-monitor

## Problem
The Vero CLI (the client's AI CLI, several models behind pre-defined guardrails) is used in the quality-check workflows. Nobody measures how fast it answers, so slow or failing periods go unnoticed and cannot be proven.

## Goal
Measure Vero CLI latency continuously, at the lowest possible cost, and show it to the Quality Lead on a dashboard.

## Users
Quality Lead (owner of the figures), Quality AI Automation team (operates it), SW QA Engineer (reads reports).

## Requirements
| ID | Requirement | Jira |
|----|-------------|------|
| VLM-001 | Execute the cheapest prompt (fixed, minimal prompt; cheapest model configurable) | ASPF-1578 AC1 |
| VLM-002 | Support time-trigger setup (Windows Task Scheduler / cron, built-in scheduler) | ASPF-1578 AC2 |
| VLM-003 | Record every probe (SQLite, run manifest) and show it on a dashboard | ASPF-1578 AC3 |
| VLM-004 | Run without manual steps once set up (scheduled, retention pruning, logs) | ASPF-1578 AC4 |
| VLM-005 | Install on another laptop from a zip with one guided script, no internet, no admin rights | ASPF-1578 |
| VLM-008 | Keep measuring on a laptop: on battery, after sleep, dashboard available after logon | ASPF-1578 |
| VLM-006 | Live view of new probes without page reload | ASPF-1578 |
| VLM-007 | Export (CSV) and a self-contained HTML report for email | ASPF-1578 |

## Out of scope
Measuring answer quality; load or stress testing; alerting by email or Teams (possible later); central server deployment.
````

### FILE: `docs/decisions/ADR-001_stdlib-only.md`

````markdown
# ADR-001: Python standard library only

Status: accepted (ASPF-1578)

## Context
The tool is sent by email as a zip and installed on laptops without admin rights and often without access to PyPI or CDNs.

## Decision
Use only the Python 3.8+ standard library (sqlite3, http.server, subprocess, threading). The dashboard is one HTML file with inline JS and SVG, no external libraries.

## Consequences
Unzip and run; nothing to install or keep patched. Charts are hand-written SVG (simple line chart only). The HTTP server is for local use only (binds to 127.0.0.1).
````

### FILE: `make_report.bat`

````bat
@echo off
rem Writes a self-contained HTML report of the last 7 days into reports\ (can be emailed) and opens it.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py report --hours 168 --out reports\vero_latency_report.html || goto end
start "" "reports\vero_latency_report.html"
exit /b 0
:end
pause
````

### FILE: `pyproject.toml`

````toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "vero-latency-monitor"
version = "0.2.0"
description = "Monitor Vero CLI response latency (ASPF-1578)"
requires-python = ">=3.8"
dependencies = []

[project.scripts]
vlm = "vero_latency.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
vero_latency = ["web/*.html"]
````

### FILE: `requirements.txt`

````text
# No third-party dependencies: Python 3.8+ standard library only (see docs/decisions/ADR-001_stdlib-only.md).
````

### FILE: `run_probe_now.bat`

````bat
@echo off
rem Runs one probe cycle now and prints the run manifest.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py probe
pause
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

### FILE: `scripts/build_installer.py`

````python
#!/usr/bin/env python3
"""Build dist/vero_latency_monitor_setup_<version>.py: ONE plain-text Python file that
recreates the whole tool folder. For channels that do not accept .zip attachments.

The output contains every file as a readable string literal plus its SHA-256, so it can be
reviewed before running. Same file selection as build_zip.py (no data, no local config)."""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vero_latency import __version__  # noqa: E402

SKIP_DIRS = {"data", "data-demo", "reports", "dist", "__pycache__", ".pytest_cache", ".venv", "venv", ".git"}
SKIP_FILES = {"config/monitor.json"}

HEADER = '''#!/usr/bin/env python3
"""Vero Latency Monitor {version} (ASPF-1578): single-file installer.

Recreates the tool folder from the files embedded below (plain text, readable, SHA-256 checked).
Needs Python 3.8+ only. Nothing is downloaded, nothing is installed system-wide.

    py vero_latency_monitor_setup_{version}.py                 -> .\\vero-latency-monitor
    py vero_latency_monitor_setup_{version}.py C:\\Tools        -> C:\\Tools\\vero-latency-monitor
    py vero_latency_monitor_setup_{version}.py --list          -> show the files, write nothing

Existing config/monitor.json and data/ are never touched (they are not in this file),
so the same command also updates an existing install.
Then open the folder and double-click setup.bat (see START_HERE.txt).
"""
import hashlib
import sys
from pathlib import Path

VERSION = "{version}"
FOLDER = "vero-latency-monitor"

FILES = {{
'''

FOOTER = '''}


def main(argv):
    if "--list" in argv:
        for rel, (sha, text) in FILES.items():
            print(f"{len(text.encode('utf-8')):>9}  {rel}")
        print(f"{len(FILES)} files, version {VERSION}")
        return 0
    args = [a for a in argv if not a.startswith("-")]
    base = Path(args[0]) if args else Path.cwd()
    target = base / FOLDER
    for rel, (sha, text) in FILES.items():
        data = text.encode("utf-8")
        if hashlib.sha256(data).hexdigest() != sha:
            print(f"checksum mismatch for {rel}: this installer file was changed or damaged. Nothing written.")
            return 1
    for rel, (sha, text) in FILES.items():
        p = target / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    print(f"Vero Latency Monitor {VERSION}: {len(FILES)} files written to {target}")
    print("Next: open that folder and double-click setup.bat (or setup_demo.bat to see the demo).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''


def main() -> None:
    out = ROOT / "dist" / f"vero_latency_monitor_setup_{__version__}.py"
    out.parent.mkdir(exist_ok=True)
    parts = [HEADER.format(version=__version__)]
    n = 0
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if f.is_dir() or SKIP_DIRS & set(rel.parts) or rel.as_posix() in SKIP_FILES or f.suffix in (".pyc", ".log"):
            continue
        data = f.read_bytes()
        text = data.decode("utf-8")  # all project files are text
        parts.append(f"    {rel.as_posix()!r}: ({hashlib.sha256(data).hexdigest()!r},\n        {text!r}),\n")
        n += 1
    parts.append(FOOTER)
    out.write_text("".join(parts), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({n} files, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
````

### FILE: `scripts/build_rebuild_md.py`

`````python
#!/usr/bin/env python3
"""Build dist/VeroLatencyMonitor_<version>_REBUILD.md: the complete source as one Markdown document.

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
from vero_latency import __version__  # noqa: E402

SKIP_DIRS = {"data", "data-demo", "reports", "dist", "__pycache__", ".pytest_cache", ".venv", "venv", ".git"}
SKIP_FILES = {"config/monitor.json", "docs/VeroLatencyMonitor_Guide.html"}
CRLF_SUFFIXES = (".bat",)
CRLF_FILES = {"START_HERE.txt"}
LANG = {".py": "python", ".json": "json", ".md": "markdown", ".html": "html", ".bat": "bat",
        ".toml": "toml", ".txt": "text"}


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


VERIFY = r'''import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vero-latency-monitor")
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
'''


def main() -> None:
    items = list(files())
    manifest = {"version": __version__, "files": {
        p: {"sha256_lf": lf_sha(t), "crlf": p.endswith(CRLF_SUFFIXES) or p in CRLF_FILES,
            "bytes": len(t.encode("utf-8"))} for p, t in items}}
    out = ROOT / "dist" / f"VeroLatencyMonitor_{__version__}_REBUILD.md"
    out.parent.mkdir(exist_ok=True)
    w = []
    w.append(f"""# Vero Latency Monitor {__version__}: complete source for rebuild

**What this is.** The full source of the Vero Latency Monitor (Jira ASPF-1578), a local tool that measures
Vero CLI response latency and shows it on a dashboard. It is sent as a readable document because archives
and scripts cannot be attached. Nothing in it runs by itself. Read it before rebuilding.

- {len(items)} files, all plain text, Python 3.8+ standard library only (no downloads, no pip).
- The HTML guide `VeroLatencyMonitor_Guide.html` is sent separately; put it in `docs/`.
- `VERO_CONTEXT.md` (included below) explains the architecture, contracts and rules.

---

## Instructions for the AI assistant (Vero CLI or other)

You are asked to recreate a project folder **exactly** from this document.

1. Create the folder `vero-latency-monitor/` in the location the user gives you (default: `C:\\Tools\\`).
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
   `py verify_rebuild.py C:\\Tools\\vero-latency-monitor VeroLatencyMonitor_{__version__}_REBUILD.md`.
   It checks every file against its SHA-256 (computed on LF line endings) and fixes CRLF where needed.
   If it reports `DIFFERENT` or `MISSING`, recreate those files again from this document.
6. Then run the tests: `py -m unittest discover -s tests -t .` inside the folder. Expected: `OK`.
7. Report the result to the user, then tell them to double-click `setup.bat` (see `START_HERE.txt`).

Do not run `setup.bat`, `install` or the real Vero CLI yourself unless the user asks.

---

## File list

| # | Path | Bytes | Line endings | SHA-256 (LF) |
|---|------|------:|:---:|---|
""")
    for i, (p, t) in enumerate(items, 1):
        m = manifest["files"][p]
        w.append(f"| {i} | `{p}` | {m['bytes']} | {'CRLF' if m['crlf'] else 'LF'} | `{m['sha256_lf'][:16]}…` |\n")
    w.append("\n---\n\n## Files\n\n")
    for p, t in items:
        text = t.replace("\r\n", "\n")
        f = fence_for(text)
        lang = LANG.get(Path(p).suffix, "") if not p.endswith(("CODEOWNERS", ".gitignore", ".gitattributes")) else "text"
        body = text if text.endswith("\n") else text + "\n"
        w.append(f"### FILE: `{p}`\n\n{f}{lang}\n{body}{f}\n\n")
    w.append("---\n\n## Verify the rebuild\n\nSave as `verify_rebuild.py` (outside the project folder) and run it as described in step 5.\n\n")
    w.append(f"````python\n{VERIFY}````\n\n")
    w.append("<!-- MANIFEST\n" + json.dumps(manifest, indent=1) + "\n-->\n")
    out.write_text("".join(w), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({len(items)} files, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
`````

### FILE: `scripts/build_zip.py`

````python
#!/usr/bin/env python3
"""Build dist/vero-latency-monitor-<version>.zip (no data, no local config, no caches)."""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vero_latency import __version__  # noqa: E402

SKIP_DIRS = {"data", "data-demo", "reports", "dist", "__pycache__", ".pytest_cache", ".venv", "venv", ".git"}
SKIP_FILES = {"config/monitor.json"}

name = "vero-latency-monitor"  # stable folder name: scheduled tasks keep working after an update
out = ROOT / "dist" / f"{name}-{__version__}.zip"
out.parent.mkdir(exist_ok=True)
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if f.is_dir() or SKIP_DIRS & set(rel.parts) or rel.as_posix() in SKIP_FILES or f.suffix in (".pyc", ".log"):
            continue
        z.write(f, f"{name}/{rel.as_posix()}")
        n += 1
print(f"wrote {out} ({n} files, {out.stat().st_size // 1024} KB)")
````

### FILE: `scripts/fake_vero.py`

````python
#!/usr/bin/env python3
"""Stand-in for the Vero CLI (demo and tests). Answers 'OK' after a realistic delay.

Env: FAKE_VERO_FAIL=1 always fails, =0 never fails, FAKE_VERO_DELAY=<seconds> fixed delay."""
import argparse
import os
import random
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("-p", "--prompt")
p.add_argument("--model", default="fake-mini")
p.add_argument("--version", action="store_true")
a = p.parse_args()
if a.version:
    print("vero-fake 0.0.1")
    sys.exit(0)
prompt = a.prompt if a.prompt is not None else sys.stdin.read()
if os.environ.get("FAKE_VERO_DELAY"):
    delay = float(os.environ["FAKE_VERO_DELAY"])
else:
    base = 1.2 if a.model == "fake-mini" else 2.4
    delay = random.lognormvariate(0, 0.35) * base
    if random.random() < 0.04:
        delay *= 4  # occasional slow answer
time.sleep(delay)
fail = os.environ.get("FAKE_VERO_FAIL")
if fail == "1" or (fail is None and random.random() < 0.03):
    print("error: upstream model unavailable (fake)", file=sys.stderr)
    sys.exit(3)
print("OK")
````

### FILE: `scripts/seed_demo_data.py`

````python
#!/usr/bin/env python3
"""Fill data/latency.db with 7 days of synthetic probes so the dashboard can be shown
before a real Vero CLI is connected. Demo only: never run this against real data.

usage: python scripts/seed_demo_data.py [--days 7] [--interval 15]"""
import argparse
import datetime as dt
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vero_latency import config  # noqa: E402
from vero_latency.probe import iso  # noqa: E402
from vero_latency.store import Store  # noqa: E402

a = argparse.ArgumentParser()
a.add_argument("--days", type=int, default=7)
a.add_argument("--interval", type=int, default=15)
args = a.parse_args()

cfg = config.load()
if not Path(cfg["data_dir"]).name.startswith("data-demo"):
    sys.exit(f"refusing to seed demo data into {cfg['data_dir']}: run  vlm init --demo  first")
store = Store(cfg["data_dir"])
now = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0)
t = now - dt.timedelta(days=args.days)
n = 0
while t < now:
    run_id = f"{t:%Y%m%d-%H%M}-vero-latency-demo"
    if not store.run_exists(run_id):
        store.start_run({"run_id": run_id, "started_at": iso(t), "trigger": "demo", "host": "demo",
                         "tool_version": "demo", "cli_version": "vero-fake 0.0.1", "prompt_sha256": ""})
        busy = 1.0 + 0.6 * (8 <= t.hour <= 16)  # office hours are slower
        for i, m in enumerate(cfg["models"]):
            base = (1100 + 1300 * i) * busy
            ms = random.lognormvariate(0, 0.3) * base * (4 if random.random() < 0.02 else 1)
            status = "ok"
            err = None
            r = random.random()
            if r < 0.015:
                status, err, ms = "error", "exit 3: error: upstream model unavailable (demo)", ms * 0.3
            elif r < 0.02:
                status, err, ms = "timeout", "no answer within timeout", cfg["cli"]["timeout_s"] * 1000
            store.add_probe({"run_id": run_id, "ts": iso(t), "epoch": t.timestamp(), "model": m["label"],
                             "model_id": m["id"], "status": status, "total_ms": round(ms, 1),
                             "first_byte_ms": round(ms * 0.85, 1) if status == "ok" else None,
                             "exit_code": 0 if status == "ok" else (3 if status == "error" else None),
                             "out_chars": 3 if status == "ok" else 0, "error": err})
            n += 1
        store.finish_run(run_id, iso(t))
    t += dt.timedelta(minutes=args.interval)
print(f"seeded {n} demo probes into {store.path}")
````

### FILE: `setup.bat`

````bat
@echo off
rem Guided first-time setup: configure -> test -> install background monitoring.
setlocal
cd /d "%~dp0"
title Vero Latency Monitor - setup
call scripts\_py.bat || exit /b 1
echo.
echo  Vero Latency Monitor setup  (Python: %PY%)
echo  ------------------------------------------------------------
:configure
%PY% vlm.py configure
if errorlevel 1 goto again
echo.
echo  Testing the Vero CLI (one call per model, nothing stored)...
%PY% vlm.py doctor
if errorlevel 1 goto again
echo.
choice /C YN /M " Install background monitoring (probe on a timer + dashboard at every logon)"
if errorlevel 2 goto manual
%PY% vlm.py install
echo.
echo  Done. The dashboard opens now and from the desktop shortcut "Vero Latency Dashboard".
%PY% vlm.py open
goto end
:manual
echo.
echo  Not installed. Use start_dashboard.bat (it also probes while its window is open).
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
rem Demo with a fake Vero CLI and 7 days of sample data (kept in data-demo\, separate from real data).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py init --demo --force || goto end
%PY% scripts\seed_demo_data.py || goto end
set "FAKE_VERO_FAIL=0"
%PY% vlm.py doctor
set "FAKE_VERO_FAIL="
echo.
echo  Demo ready. The dashboard opens now; close this window to stop it.
echo  For the real setup later, run setup.bat (it leaves demo mode).
%PY% vlm.py serve --open
:end
pause
````

### FILE: `src/vero_latency/__init__.py`

````python
"""Vero CLI latency monitor (ASPF-1578)."""

__version__ = "0.2.0"
COMPONENT = "vero-latency"
````

### FILE: `src/vero_latency/__main__.py`

````python
import sys

from .cli import main

sys.exit(main())
````

### FILE: `src/vero_latency/cli.py`

````python
"""Command line: python vlm.py <command>. Run with -h for help."""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import logging.handlers
import os
import shlex
import shutil
import sys
import time
from pathlib import Path

from . import __version__, config, scheduler
from .config import ROOT, ConfigError
from .probe import build_command, classify, cli_version, run_cycle, run_in_progress, time_command
from .server import already_running, serve, static_report
from .store import Store

log = logging.getLogger("vero_latency")
FAKE = ROOT / "scripts" / "fake_vero.py"


def _setup_logging(data_dir: str, verbose: bool) -> None:
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [logging.handlers.RotatingFileHandler(
        Path(data_dir) / "monitor.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")]
    if sys.stdout is not None:  # None under pythonw (Task Scheduler)
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, handlers=handlers,
                        format="%(asctime)s %(levelname)s %(message)s", force=True)


def _ask(question: str, default: str) -> str:
    try:
        answer = input(f"{question} [{default}]: ").strip()
    except EOFError:
        answer = ""
    return answer or default


def _split(line: str) -> list[str]:
    parts = shlex.split(line, posix=os.name != "nt")
    return [p[1:-1] if len(p) >= 2 and p[0] == p[-1] == '"' else p for p in parts]


def _join(args: list[str]) -> str:
    return " ".join(f'"{a}"' if " " in a else a for a in args)


# commands ---------------------------------------------------------------------

def cmd_init(a) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    if target.exists() and not a.force:
        print(f"{target} already exists (use --force to overwrite, or run: vlm configure)")
        return 0
    cfg = config.read_json(config.EXAMPLE_FILE)
    if a.demo:
        cfg["cli"]["command"] = [sys.executable, str(FAKE), "-p", "{prompt}", "--model", "{model}"]
        cfg["cli"]["version_command"] = [sys.executable, str(FAKE), "--version"]
        cfg["models"] = [{"id": "fake-mini", "label": "fake-mini"}, {"id": "fake-std", "label": "fake-std"}]
        cfg["schedule"]["interval_minutes"] = 1
        cfg["data_dir"] = "data-demo"  # never mixed with real measurements
    config.write_json(target, cfg)
    print(f"wrote {target}" + ("  (demo: fake Vero CLI, data in data-demo/)" if a.demo else ""))
    return 0


def cmd_configure(a) -> int:
    target = Path(a.config) if a.config else config.CONFIG_FILE
    cur = config.read_json(config.EXAMPLE_FILE)
    if target.exists():
        try:
            cur = config.read_json(target)
        except ConfigError as e:
            print(f"current config is broken, starting from the defaults ({e})")
    if str(cur.get("data_dir", "")).startswith("data-demo"):
        cur = config.read_json(config.EXAMPLE_FILE)  # leaving demo mode
    cur = config._merge(config.DEFAULTS, cur)
    print("\nVero latency monitor: configuration. Press Enter to keep the value in [brackets].\n")
    print("1. How to run the Vero CLI once, non-interactively. Check with: vero --help")
    print("   Placeholders: {prompt} = the probe prompt, {model} = model id. Without {prompt} the prompt goes to stdin.")
    while True:
        cmd = _split(_ask("   Command", _join(cur["cli"]["command"])))
        found = shutil.which(cmd[0]) if cmd else None
        if cmd and found:
            print(f"   found: {found}")
            break
        print(f"   '{cmd[0] if cmd else ''}' was not found. Give the full path (run: where vero), or type it again to keep it.")
        if cmd and _ask("   Keep it anyway? (y/n)", "n").lower().startswith("y"):
            break
    cur["cli"]["command"] = cmd
    cur["cli"]["prompt_via"] = "arg" if any("{prompt}" in c for c in cmd) else "stdin"
    ver = cur["cli"].get("version_command") or []
    if ver and ver[0] in ("vero", "vero.exe", "vero.cmd"):
        cur["cli"]["version_command"] = [cmd[0]] + ver[1:]

    print("\n2. Model ids to probe, comma separated. Put the cheapest first. Empty = the CLI default model.")
    ids = [m["id"] for m in cur["models"] if "<<" not in m["id"]]
    raw = _ask("   Models", ",".join(ids) or "")
    ids = [x.strip() for x in raw.split(",")] if raw.strip() else [""]
    cur["models"] = [{"id": i, "label": i or "default"} for i in ids]

    print("\n3. Timing")
    try:
        cur["schedule"]["interval_minutes"] = int(_ask("   Probe every N minutes", str(cur["schedule"]["interval_minutes"])))
        cur["cli"]["timeout_s"] = float(_ask("   Timeout per call, seconds", f"{float(cur['cli']['timeout_s']):g}"))
        cur["thresholds_ms"]["warn"] = float(_ask("   Warn from, seconds", f"{cur['thresholds_ms']['warn'] / 1000:g}")) * 1000
        cur["thresholds_ms"]["crit"] = float(_ask("   Critical from, seconds", f"{cur['thresholds_ms']['crit'] / 1000:g}")) * 1000
        config.validate(config._merge(config.DEFAULTS, cur))
    except (ConfigError, KeyError, TypeError, ValueError) as e:
        print(f"\nnot saved: {e}")
        return 1
    config.write_json(target, cur)
    print(f"\nsaved {target}")
    return 0


def cmd_doctor(a, cfg) -> int:
    cli = cfg["cli"]
    ok = True
    print(f"config         {cfg['_path']}")
    print(f"data           {cfg['data_dir']}")
    exe = cli["command"][0]
    found = shutil.which(exe)
    print(f"executable     {exe} -> {found or 'NOT FOUND (use the full path, see: where vero)'}")
    ok &= bool(found)
    print(f"cli version    {cli_version(cfg)}")
    for m in cfg["models"]:
        args = build_command(cli["command"], cfg["prompt"], m["id"], cli["prompt_via"])
        stdin = cfg["prompt"] if cli["prompt_via"] == "stdin" else None
        res = time_command(args, stdin, cli["timeout_s"], cli.get("env"))
        status, err = classify(res, cfg.get("expect", ""))
        ms = f"{res['total_ms']:.0f} ms" if res["total_ms"] is not None else "-"
        print(f"probe {m['label']:<12} {status:<11}{ms:>9}   {err or res['stdout'].strip()[:60]!r}")
        print(f"               command: {_join(args)}")
        ok &= status == "ok"
    print("RESULT         " + ("ready" if ok else "NOT READY: fix the items above (guide, section Troubleshooting)"))
    return 0 if ok else 1


def cmd_probe(a, cfg) -> int:
    m = run_cycle(cfg, Store(cfg["data_dir"]), a.trigger)
    if m is None:
        print("another run is in progress; skipped")
        return 0
    if not a.quiet:
        import json
        print(json.dumps(m, indent=2))
    if a.trigger == "task":
        return 0  # failed probes are data, not a task failure (keeps Task Scheduler "Last Result" = 0)
    return 0 if m["totals"]["failed"] == 0 else 2


def cmd_serve(a, cfg) -> int:
    host = a.host or cfg["server"]["host"]
    port = a.port or cfg["server"]["port"]
    cfg["server"]["host"], cfg["server"]["port"] = host, port
    with_sched = bool(cfg["schedule"]["run_in_dashboard"]) and not a.no_scheduler
    return serve(cfg, Store(cfg["data_dir"]), host, port, with_sched, a.open)


def _set_run_in_dashboard(cfg: dict, value: bool) -> None:
    raw = config.read_json(Path(cfg["_path"]))
    raw.setdefault("schedule", {})["run_in_dashboard"] = value
    config.write_json(Path(cfg["_path"]), raw)


def cmd_install(a, cfg) -> int:
    every = int(a.every or cfg["schedule"]["interval_minutes"])
    if not 1 <= every <= 1440:
        print("--every must be between 1 and 1440 minutes")
        return 1
    url = f"http://127.0.0.1:{cfg['server']['port']}/"
    for line in scheduler.install(every, url, dashboard=not a.no_dashboard):
        print(line)
    _set_run_in_dashboard(cfg, False)
    print("config: schedule.run_in_dashboard = false (the OS scheduler runs the probes now)")
    print(f"open the dashboard: {url}")
    return 0


def cmd_uninstall(a, cfg) -> int:
    for line in scheduler.remove():
        print(line)
    _set_run_in_dashboard(cfg, True)
    print("config: schedule.run_in_dashboard = true. Data is kept in " + cfg["data_dir"])
    return 0


def cmd_open(a, cfg) -> int:
    """Wait for the background dashboard to answer, then open it in the browser."""
    import webbrowser
    port = cfg["server"]["port"]
    url = f"http://127.0.0.1:{port}/"
    deadline = time.time() + a.wait
    while not already_running("127.0.0.1", port):
        if time.time() > deadline:
            print(f"dashboard is not running at {url}: use start_dashboard.bat, or see data/monitor.log")
            return 1
        time.sleep(1)
    webbrowser.open(url)
    print(f"opened {url}")
    return 0


def cmd_status(a, cfg) -> int:
    store = Store(cfg["data_dir"])
    last = store.last_run()
    port = cfg["server"]["port"]
    print(f"version        {__version__}")
    print(f"config         {cfg['_path']}")
    print(f"data           {cfg['data_dir']}  ({store.max_probe_id()} probes recorded)")
    print(f"last run       {last['run_id'] + ' at ' + last['started_at'] if last else 'none yet'}")
    print(f"run now        {'yes' if run_in_progress(cfg) else 'no'}")
    print(f"dashboard      {'running at http://127.0.0.1:%d/' % port if already_running('127.0.0.1', port) else 'not running'}")
    print(f"scheduler      {'dashboard window' if cfg['schedule']['run_in_dashboard'] else 'OS (Task Scheduler / cron)'}"
          f", every {cfg['schedule']['interval_minutes']} min\n")
    print(scheduler.status())
    return 0


def cmd_export(a, cfg) -> int:
    data = Store(cfg["data_dir"]).to_csv(time.time() - a.hours * 3600 if a.hours else 0, a.model)
    out = Path(a.out or f"vero_latency_{dt.date.today():%Y%m%d}.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(data, encoding="utf-8")
    print(f"wrote {out} ({data.count(chr(10)) - 1} rows)")
    return 0


def cmd_report(a, cfg) -> int:
    out = Path(a.out or f"vero_latency_report_{dt.date.today():%Y%m%d}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(static_report(cfg, Store(cfg["data_dir"]), a.hours, a.model), encoding="utf-8")
    print(f"wrote {out} (last {a.hours:g} h, self-contained, can be emailed)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vlm", description="Vero CLI latency monitor (ASPF-1578)")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--config", help="path to monitor.json (default config/monitor.json, or env VLM_CONFIG)")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", metavar="command")
    sub.required = True

    s = sub.add_parser("init", help="create config/monitor.json from the example")
    s.add_argument("--demo", action="store_true", help="use the bundled fake Vero CLI (data in data-demo/)")
    s.add_argument("--force", action="store_true")
    sub.add_parser("configure", help="guided set-up of the Vero command, models and thresholds")
    sub.add_parser("doctor", help="check the Vero CLI connection with one test call per model (nothing stored)")

    s = sub.add_parser("probe", help="run one probe cycle now and store it")
    s.add_argument("--trigger", default="manual", choices=["manual", "task", "schedule", "dashboard"])
    s.add_argument("-q", "--quiet", action="store_true")

    s = sub.add_parser("serve", help="start the dashboard (with the built-in scheduler unless installed)")
    s.add_argument("--host")
    s.add_argument("--port", type=int)
    s.add_argument("--no-scheduler", action="store_true")
    s.add_argument("--open", action="store_true", help="open the browser")

    s = sub.add_parser("install", help="unattended mode: OS scheduler task + dashboard at logon + desktop shortcut")
    s.add_argument("--every", type=int, help="minutes (default: schedule.interval_minutes)")
    s.add_argument("--no-dashboard", action="store_true", help="only the probe task")
    sub.add_parser("uninstall", help="remove the tasks and the shortcut (data is kept)")
    sub.add_parser("status", help="show configuration, last run, dashboard and task state")
    s = sub.add_parser("open", help="open the running dashboard in the browser")
    s.add_argument("--wait", type=float, default=20, help="seconds to wait for it to start")

    for name, helptext in (("export", "write probes to CSV"), ("report", "write a self-contained HTML report")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("--hours", type=float, default=0 if name == "export" else 168)
        s.add_argument("--model")
        s.add_argument("--out")
    return p


HANDLERS = {"doctor": cmd_doctor, "probe": cmd_probe, "serve": cmd_serve, "install": cmd_install,
            "uninstall": cmd_uninstall, "status": cmd_status, "open": cmd_open, "export": cmd_export, "report": cmd_report}


def main(argv: list[str] | None = None) -> int:
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
    _setup_logging(cfg["data_dir"], a.verbose)
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

### FILE: `src/vero_latency/config.py`

````python
"""Load and validate config/monitor.json. Non-secret settings only."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "monitor.json"
EXAMPLE_FILE = CONFIG_DIR / "monitor.example.json"

DEFAULTS = {
    "cli": {
        "command": ["vero", "-p", "{prompt}", "--model", "{model}"],
        "prompt_via": "arg",
        "timeout_s": 60,
        "version_command": ["vero", "--version"],
        "env": {},
    },
    "prompt": "Reply with OK",
    "expect": "OK",
    "models": [{"id": "", "label": "default"}],
    "schedule": {"interval_minutes": 15, "run_in_dashboard": True},
    "thresholds_ms": {"warn": 5000, "crit": 15000},
    "retention_days": 90,
    "server": {"host": "127.0.0.1", "port": 8765},
    "data_dir": "data",
}


class ConfigError(Exception):
    pass


def _merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def read_json(path: Path) -> dict:
    # utf-8-sig: Notepad on Windows may save "UTF-8 with BOM"
    text = Path(path).read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        hint = ""
        if "escape" in str(e).lower():
            hint = " (Windows paths: write C:\\\\Tools\\\\x or C:/Tools/x)"
        raise ConfigError(f"{path}: invalid JSON: {e}{hint}") from e


def write_json(path: Path, data: dict) -> None:
    clean = {k: v for k, v in data.items() if not k.startswith("_")}
    Path(path).write_text(json.dumps(clean, indent=2) + "\n", encoding="utf-8")


def load(path: Path | str | None = None) -> dict:
    path = Path(path or os.environ.get("VLM_CONFIG") or CONFIG_FILE)
    if not path.exists():
        raise ConfigError(f"config not found: {path} (run setup.bat or: python vlm.py configure)")
    raw = read_json(path)
    if not isinstance(raw, dict):
        raise ConfigError(f"{path}: top level must be a JSON object")
    cfg = _merge(DEFAULTS, raw)
    try:
        validate(cfg)
    except (KeyError, TypeError, ValueError) as e:
        raise ConfigError(f"{path}: wrong value or type near {e}") from e
    data_dir = Path(os.path.expandvars(os.path.expanduser(str(cfg["data_dir"]))))
    cfg["data_dir"] = str(data_dir if data_dir.is_absolute() else ROOT / data_dir)
    cfg["_path"] = str(path)
    return cfg


def validate(cfg: dict) -> None:
    cli = cfg["cli"]
    if not isinstance(cli["command"], list) or not cli["command"] or not all(isinstance(a, str) for a in cli["command"]):
        raise ConfigError("cli.command must be a non-empty list of strings")
    if cli["prompt_via"] not in ("arg", "stdin"):
        raise ConfigError("cli.prompt_via must be 'arg' or 'stdin'")
    if cli["prompt_via"] == "arg" and not any("{prompt}" in a for a in cli["command"]):
        raise ConfigError("cli.command needs a {prompt} placeholder when prompt_via is 'arg'")
    cli["timeout_s"] = float(cli["timeout_s"])
    if cli["timeout_s"] <= 0:
        raise ConfigError("cli.timeout_s must be > 0")
    if not isinstance(cli.get("env") or {}, dict):
        raise ConfigError("cli.env must be an object")
    if not isinstance(cfg["models"], list) or not cfg["models"]:
        raise ConfigError("models must list at least one entry")
    labels = set()
    for m in cfg["models"]:
        if not isinstance(m, dict) or "id" not in m:
            raise ConfigError("every model needs an 'id' (use \"\" for the CLI default)")
        m["id"] = str(m["id"])
        m["label"] = str(m.get("label") or m["id"] or "default")
        if m["label"] in labels:
            raise ConfigError(f"duplicate model label {m['label']!r}")
        labels.add(m["label"])
    s = cfg["schedule"]
    s["interval_minutes"] = int(s["interval_minutes"])
    if not 1 <= s["interval_minutes"] <= 1440:
        raise ConfigError("schedule.interval_minutes must be between 1 and 1440")
    t = cfg["thresholds_ms"]
    t["warn"], t["crit"] = float(t["warn"]), float(t["crit"])
    if not 0 < t["warn"] <= t["crit"]:
        raise ConfigError("thresholds_ms: need 0 < warn <= crit")
    cfg["retention_days"] = int(cfg["retention_days"])
    if cfg["retention_days"] < 1:
        raise ConfigError("retention_days must be >= 1")
    cfg["server"]["port"] = int(cfg["server"]["port"])


def public_view(cfg: dict) -> dict:
    """What the dashboard may show. Never includes cli.env values."""
    return {
        "models": [m["label"] for m in cfg["models"]],
        "prompt": cfg["prompt"],
        "interval_minutes": cfg["schedule"]["interval_minutes"],
        "run_in_dashboard": cfg["schedule"]["run_in_dashboard"],
        "thresholds_ms": cfg["thresholds_ms"],
        "timeout_s": cfg["cli"]["timeout_s"],
        "retention_days": cfg["retention_days"],
    }
````

### FILE: `src/vero_latency/probe.py`

````python
"""Run the cheapest prompt through the Vero CLI and time it.

One *run* = one probe per configured model. Each run gets a run_id
(<YYYYMMDD-HHMM>-vero-latency, SCMP naming) and a JSON run manifest.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import os
import platform
import shutil
import signal
import subprocess
import threading
import time
from pathlib import Path

from . import COMPONENT, __version__
from .store import Store

log = logging.getLogger("vero_latency")

IS_WINDOWS = os.name == "nt"
NO_WINDOW = 0x08000000 if IS_WINDOWS else 0  # CREATE_NO_WINDOW: no console flash from Task Scheduler
ERROR_MAX = 300


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso(t: dt.datetime) -> str:
    return t.isoformat(timespec="seconds").replace("+00:00", "Z")


def build_command(template: list[str], prompt: str, model_id: str, prompt_via: str) -> list[str]:
    """Fill {prompt}/{model}. An empty model drops the {model} arg and the flag before it."""
    args: list[str] = []
    for a in template:
        if "{model}" in a and not model_id:
            if a == "{model}" and args and args[-1].startswith("-"):
                args.pop()
            continue
        if "{prompt}" in a and prompt_via == "stdin":
            continue
        args.append(a.replace("{prompt}", prompt).replace("{model}", model_id))
    exe = shutil.which(args[0])  # resolves vero.cmd / vero.exe on Windows
    if exe:
        args[0] = exe
    return args


def _kill_tree(proc: subprocess.Popen) -> None:
    """Kill the CLI and everything it started (e.g. vero.cmd -> node), so no pipe stays open."""
    try:
        if IS_WINDOWS:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                           capture_output=True, creationflags=NO_WINDOW)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    except OSError:
        pass
    try:
        proc.kill()
    except OSError:
        pass


def time_command(args: list[str], stdin_text: str | None, timeout_s: float,
                 env_extra: dict | None = None) -> dict:
    """Run one command. Returns total_ms, first_byte_ms, exit_code, stdout, stderr, timed_out."""
    env = dict(os.environ, **{k: str(v) for k, v in (env_extra or {}).items()})
    t0 = time.perf_counter()
    try:
        proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=env, creationflags=NO_WINDOW,
            start_new_session=not IS_WINDOWS,  # own process group, killable as a whole
        )
    except OSError as e:
        return {"total_ms": None, "first_byte_ms": None, "exit_code": None,
                "stdout": "", "stderr": f"cannot start {args[0]!r}: {e}", "timed_out": False}

    first = {}
    out_chunks: list[bytes] = []
    err_chunks: list[bytes] = []

    def read_out():
        while True:
            chunk = proc.stdout.read1(4096)
            if not chunk:
                break
            if "t" not in first and chunk.strip():
                first["t"] = time.perf_counter()
            out_chunks.append(chunk)

    def read_err():
        err_chunks.append(proc.stderr.read())

    threads = [threading.Thread(target=read_out, daemon=True),
               threading.Thread(target=read_err, daemon=True)]
    for th in threads:
        th.start()
    if stdin_text is not None:
        try:
            proc.stdin.write(stdin_text.encode("utf-8"))
            proc.stdin.close()
        except OSError:
            pass
    timed_out = False
    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_tree(proc)
        proc.wait()
    t1 = time.perf_counter()
    for th in threads:
        th.join(timeout=5)
    return {
        "total_ms": (t1 - t0) * 1000,
        "first_byte_ms": (first["t"] - t0) * 1000 if "t" in first else None,
        "exit_code": proc.returncode,
        "stdout": b"".join(out_chunks).decode("utf-8", "replace"),
        "stderr": b"".join(err_chunks).decode("utf-8", "replace"),
        "timed_out": timed_out,
    }


def classify(res: dict, expect: str) -> tuple[str, str | None]:
    if res["timed_out"]:
        return "timeout", "no answer within timeout"
    if res["total_ms"] is None:
        return "error", res["stderr"][:ERROR_MAX]
    if res["exit_code"] != 0:
        msg = (res["stderr"].strip() or res["stdout"].strip())[:ERROR_MAX]
        return "error", f"exit {res['exit_code']}: {msg}"
    if expect and expect.lower() not in res["stdout"].lower():
        return "unexpected", f"answer did not contain {expect!r} ({len(res['stdout'])} chars)"
    return "ok", None


def cli_version(cfg: dict) -> str:
    cmd = cfg["cli"].get("version_command") or []
    if not cmd:
        return "n/a"
    res = time_command(build_command(cmd, "", "", "arg"), None, 15, cfg["cli"].get("env"))
    text = (res["stdout"] or res["stderr"]).strip().splitlines()
    return text[0][:80] if res["exit_code"] == 0 and text else "unknown"


def new_run_id(store: Store, now: dt.datetime) -> str:
    base = f"{now:%Y%m%d-%H%M}-{COMPONENT}"
    run_id, n = base, 2
    while store.run_exists(run_id):
        run_id, n = f"{base}-{n}", n + 1
    return run_id


def lock_stale_after(cfg: dict) -> float:
    return cfg["cli"]["timeout_s"] * len(cfg["models"]) + 120


def run_in_progress(cfg: dict) -> bool:
    """True while any process (dashboard or Task Scheduler) holds a fresh probe lock."""
    try:
        age = time.time() - (Path(cfg["data_dir"]) / "probe.lock").stat().st_mtime
    except FileNotFoundError:
        return False
    return age < lock_stale_after(cfg)


class RunLock:
    """File lock so a Task Scheduler run and a dashboard run never overlap."""

    def __init__(self, data_dir: str, stale_s: float):
        self.path = Path(data_dir) / "probe.lock"
        self.stale_s = stale_s
        self.held = False

    def __enter__(self):
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                self.held = True
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > self.stale_s:
                        self.path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                return self
        return self

    def __exit__(self, *exc):
        if self.held:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


def run_cycle(cfg: dict, store: Store, trigger: str = "manual") -> dict | None:
    """Probe every model once. Returns the run manifest, or None if another run holds the lock."""
    cli = cfg["cli"]
    with RunLock(cfg["data_dir"], lock_stale_after(cfg)) as lock:
        if not lock.held:
            log.info("another run is in progress; skipped")
            return None
        started = utc_now()
        run = {
            "run_id": new_run_id(store, started),
            "started_at": iso(started),
            "trigger": trigger,
            "host": platform.node(),
            "tool_version": __version__,
            "cli_version": cli_version(cfg),
            "prompt_sha256": hashlib.sha256(cfg["prompt"].encode("utf-8")).hexdigest(),
        }
        store.start_run(run)
        results = []
        for m in cfg["models"]:
            args = build_command(cli["command"], cfg["prompt"], m["id"], cli["prompt_via"])
            stdin = cfg["prompt"] if cli["prompt_via"] == "stdin" else None
            when = utc_now()
            res = time_command(args, stdin, cli["timeout_s"], cli.get("env"))
            status, error = classify(res, cfg.get("expect", ""))
            probe = {
                "run_id": run["run_id"],
                "ts": iso(when),
                "epoch": when.timestamp(),
                "model": m["label"],
                "model_id": m["id"],
                "status": status,
                "total_ms": round(res["total_ms"], 1) if res["total_ms"] is not None else None,
                "first_byte_ms": round(res["first_byte_ms"], 1) if res["first_byte_ms"] is not None else None,
                "exit_code": res["exit_code"],
                "out_chars": len(res["stdout"]),
                "error": error,
            }
            probe["id"] = store.add_probe(probe)
            results.append(probe)
            log.info("%s %-12s %-10s %s ms", run["run_id"], m["label"], status, probe["total_ms"])
        finished = utc_now()
        store.finish_run(run["run_id"], iso(finished))
        store.prune(int(cfg["retention_days"]))
        manifest = write_manifest(cfg, run, iso(finished), results)
        return manifest


def write_manifest(cfg: dict, run: dict, finished_at: str, results: list[dict]) -> dict:
    ok = sum(1 for r in results if r["status"] == "ok")
    manifest = {
        "run_id": run["run_id"],
        "component": COMPONENT,
        "tool_version": run["tool_version"],
        "trigger": run["trigger"],
        "host": run["host"],
        "started_at": run["started_at"],
        "finished_at": finished_at,
        "cli": {"name": "vero", "version": run["cli_version"]},
        "prompt_sha256": run["prompt_sha256"],
        "models": [{"label": m["label"], "id": m["id"]} for m in cfg["models"]],
        "results": [{k: r[k] for k in ("model", "status", "total_ms", "first_byte_ms", "exit_code", "error")}
                    for r in results],
        "totals": {"probes": len(results), "ok": ok, "failed": len(results) - ok},
        "availability_percent": round(ok / len(results) * 100, 2) if results else None,
    }
    d = Path(cfg["data_dir"]) / "runs" / run["started_at"][:7]
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{run['run_id']}.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
````

### FILE: `src/vero_latency/scheduler.py`

````python
"""Time triggers.

- Loop: in-process scheduler used while the dashboard runs in "dashboard" mode.
- install()/remove()/status(): the OS scheduler for unattended use.
  Windows: two Task Scheduler tasks, registered from XML so laptop-safe settings apply
  (runs on battery, catches up after sleep, never two at once):
    VeroLatencyMonitor   every N minutes: pythonw vlm.py probe --trigger task
    VeroLatencyDashboard at logon:        pythonw vlm.py serve --no-scheduler (hidden, background)
  Linux/macOS: two crontab lines (probe every N minutes, dashboard @reboot).
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

from .config import ROOT
from .probe import NO_WINDOW, run_cycle
from .store import Store

log = logging.getLogger("vero_latency")

PROBE_TASK = "VeroLatencyMonitor"
DASH_TASK = "VeroLatencyDashboard"
CRON_MARK = "# vero-latency-monitor"
SHORTCUT = "Vero Latency Dashboard.url"


def next_aligned(interval_s: int, now: float | None = None) -> float:
    """Next wall-clock boundary (:00, :15, ...). Task Scheduler and the Loop use the same grid."""
    now = time.time() if now is None else now
    return (now // interval_s + 1) * interval_s


class Loop:
    """Runs a probe cycle every interval while the dashboard is open."""

    def __init__(self, cfg: dict, store: Store):
        self.cfg, self.store = cfg, store
        self.interval = int(cfg["schedule"]["interval_minutes"]) * 60
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

        def work():
            self.running = True
            try:
                run_cycle(self.cfg, self.store, source)
            except Exception:
                log.exception("probe cycle failed")
            finally:
                self.running = False
                self._busy.release()

        threading.Thread(target=work, daemon=True).start()
        return True

    def start(self) -> None:
        self.active = True

        def loop():
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
    return [_python(True), str(ROOT / "vlm.py"), "probe", "--trigger", "task", "--quiet"]


def dashboard_command() -> list[str]:
    return [_python(True), str(ROOT / "vlm.py"), "serve", "--no-scheduler"]


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
  <Principals><Principal id="Author"><UserId>{user}</UserId><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
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
    trig = (f"<TimeTrigger><Repetition><Interval>PT{interval_minutes}M</Interval>"
            f"<StopAtDurationEnd>false</StopAtDurationEnd></Repetition>"
            f"<StartBoundary>{start}</StartBoundary><Enabled>true</Enabled></TimeTrigger>")
    return _task_xml("Vero CLI latency probe (ASPF-1578)", trig, probe_command(), "PT1H")


def dashboard_task_xml() -> str:
    trig = f"<LogonTrigger><Enabled>true</Enabled><UserId>{escape(_win_user())}</UserId></LogonTrigger>"
    return _task_xml("Vero CLI latency dashboard, http://127.0.0.1 (ASPF-1578)", trig, dashboard_command(), "PT0S")


def _schtasks(*args: str, check: bool = True) -> subprocess.CompletedProcess:
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
    if os.name == "nt":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
            return Path(os.path.expandvars(winreg.QueryValueEx(key, "Desktop")[0]))
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
        out.append(f"task '{PROBE_TASK}': probe every {interval_minutes} min (also on battery, catches up after sleep)")
        if dashboard:
            _register(DASH_TASK, dashboard_task_xml())
            _schtasks("/Run", "/TN", DASH_TASK, check=False)
            out.append(f"task '{DASH_TASK}': dashboard starts hidden at every logon (started now)")
    else:
        lines = [l for l in _crontab_lines() if CRON_MARK not in l]
        lines.append(f"{_cron_expr(interval_minutes)} {' '.join(_sh(c) for c in probe_command())} {CRON_MARK}")
        if dashboard:
            lines.append(f"@reboot {' '.join(_sh(c) for c in dashboard_command())} >/dev/null 2>&1 {CRON_MARK}")
            subprocess.Popen(dashboard_command(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        _write_crontab(lines)
        out.append(f"cron: probe every {interval_minutes} min" + (", dashboard @reboot (started now)" if dashboard else ""))
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
        _write_crontab([l for l in _crontab_lines() if CRON_MARK not in l])
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
        mine = [l for l in _crontab_lines() if CRON_MARK in l]
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
        raise RuntimeError("crontab is not installed on this machine")
    return r.stdout.splitlines() if r.returncode == 0 else []


def _write_crontab(lines: list[str]) -> None:
    r = subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
````

### FILE: `src/vero_latency/server.py`

````python
"""Local web server: dashboard page, JSON API and a live Server-Sent Events stream."""
from __future__ import annotations

import datetime as dt
import json
import logging
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import __version__, stats
from .config import public_view
from .probe import run_in_progress
from .scheduler import Loop
from .store import Store

log = logging.getLogger("vero_latency")
WEB = Path(__file__).parent / "web"
RANGES = (1, 6, 24, 168, 720)


def parse_hours(value: str | None, default: float = 24) -> float:
    try:
        h = float(value) if value is not None else default
    except ValueError:
        return default
    return h if h in RANGES else default


def dashboard_payload(cfg: dict, store: Store, hours: float, model: str | None,
                      loop: Loop | None = None) -> dict:
    since = time.time() - hours * 3600
    rows = store.probes(since, model)
    warn, crit = cfg["thresholds_ms"]["warn"], cfg["thresholds_ms"]["crit"]
    labels = [m["label"] for m in cfg["models"]]
    seen = sorted({r["model"] for r in rows} - set(labels))
    per_model = []
    for label in labels + seen:
        if model and label != model:
            continue
        s = stats.summarize([r for r in rows if r["model"] == label], warn, crit)
        s["model"] = label
        per_model.append(s)
    bucket = stats.bucket_seconds(hours)
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "tool_version": __version__,
        "range_hours": hours,
        "model": model,
        "config": public_view(cfg),
        "state": {
            "running": bool(loop and loop.running) or run_in_progress(cfg),
            "scheduler": "dashboard" if loop and loop.active else "external",
            "next_run_epoch": loop.expected_next() if loop else None,
            "last_run": store.last_run(),
        },
        "overall": stats.summarize(rows, warn, crit),
        "per_model": per_model,
        "series": {"bucket_s": bucket, "models": stats.series(rows, bucket)},
        "failures": [{k: r[k] for k in ("ts", "epoch", "model", "status", "error")}
                     for r in rows if r["status"] != "ok"][-50:],
        "recent": store.probes(since, model, limit=15, newest_first=True),
    }


def static_report(cfg: dict, store: Store, hours: float, model: str | None) -> str:
    payload = dashboard_payload(cfg, store, hours, model)
    html = (WEB / "dashboard.html").read_text(encoding="utf-8")
    blob = json.dumps(payload).replace("<", "\\u003c")  # nothing in the data can open or close a tag
    return html.replace("<!--STATIC_DATA-->", f"<script>window.STATIC_DATA={blob};</script>", 1)


def make_handler(cfg: dict, store: Store, loop: Loop | None):
    port = cfg["server"]["port"]
    bind = cfg["server"]["host"]
    allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}", f"{bind}:{port}"}

    class Handler(BaseHTTPRequestHandler):
        server_version = f"vero-latency/{__version__}"

        def log_message(self, fmt, *args):
            log.debug("%s " + fmt, self.address_string(), *args)

        def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj, code: int = 200):
            self._send(code, json.dumps(obj).encode(), "application/json")

        def _host_ok(self) -> bool:
            # blocks DNS rebinding: only requests addressed to this local server
            if bind == "0.0.0.0":
                return True
            return (self.headers.get("Host") or "").lower() in allowed_hosts

        def _same_origin(self) -> bool:
            # blocks other web pages from POSTing (a probe costs tokens)
            origin = self.headers.get("Origin")
            if origin is None:
                return True
            return urlparse(origin).netloc.lower() == (self.headers.get("Host") or "").lower()

        def do_GET(self):
            try:
                if not self._host_ok():
                    return self._json({"error": "forbidden host"}, 403)
                u = urlparse(self.path)
                q = {k: v[0] for k, v in parse_qs(u.query).items()}
                hours = parse_hours(q.get("hours"))
                model = q.get("model") or None
                if u.path in ("/", "/index.html"):
                    self._send(200, (WEB / "dashboard.html").read_bytes(), "text/html; charset=utf-8")
                elif u.path == "/api/dashboard":
                    self._json(dashboard_payload(cfg, store, hours, model, loop))
                elif u.path == "/api/health":
                    self._json({"status": "up", "app": "vero-latency", "version": __version__})
                elif u.path == "/api/export.csv":
                    name = f"vero_latency_{dt.date.today():%Y%m%d}.csv"
                    self._send(200, store.to_csv(time.time() - hours * 3600, model).encode(), "text/csv",
                               {"Content-Disposition": f'attachment; filename="{name}"'})
                elif u.path == "/api/stream":
                    self._stream()
                else:
                    self._json({"error": "not found"}, 404)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass
            except Exception:
                log.exception("request failed: %s", self.path)
                try:
                    self._json({"error": "internal error, see data/monitor.log"}, 500)
                except OSError:
                    pass

        def do_POST(self):
            if not self._host_ok() or not self._same_origin():
                return self._json({"error": "forbidden"}, 403)
            if urlparse(self.path).path != "/api/probe":
                return self._json({"error": "not found"}, 404)
            if loop is None:
                return self._json({"error": "scheduler unavailable"}, 503)
            if run_in_progress(cfg):
                return self._json({"started": False, "running": True}, 409)
            started = loop.trigger("dashboard")
            self._json({"started": started, "running": True}, 202 if started else 409)

        def _stream(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            last_id = store.max_probe_id()
            was = None
            beat = time.time()
            while True:
                running = bool(loop and loop.running) or run_in_progress(cfg)
                nxt = loop.expected_next() if loop else None
                if (running, nxt) != was:
                    self._event("state", {"running": running, "next_run_epoch": nxt})
                    was = (running, nxt)
                for p in store.probes(after_id=last_id):
                    self._event("probe", p)
                    last_id = max(last_id, p["id"])
                if time.time() - beat > 15:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    beat = time.time()
                time.sleep(1.5)

        def _event(self, name: str, data: dict):
            self.wfile.write(f"event: {name}\ndata: {json.dumps(data)}\n\n".encode())
            self.wfile.flush()

    return Handler


def already_running(host: str, port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://{host}:{port}/api/health", timeout=2) as r:
            return json.load(r).get("app") == "vero-latency"
    except Exception:
        return False


def serve(cfg: dict, store: Store, host: str, port: int, with_scheduler: bool, open_browser: bool) -> int:
    local = "127.0.0.1" if host == "0.0.0.0" else host
    url = f"http://{local}:{port}/"
    if already_running(local, port):
        print(f"Dashboard already running: {url}")
        if open_browser:
            webbrowser.open(url)
        return 0
    loop = Loop(cfg, store)
    try:
        httpd = ThreadingHTTPServer((host, port), make_handler(cfg, store, loop))
    except OSError as e:
        msg = f"cannot listen on {host}:{port} ({e}). Another program uses the port: change server.port in config/monitor.json"
        log.error(msg)
        print(msg)
        return 1
    httpd.daemon_threads = True
    if with_scheduler:
        loop.start()
    log.info("dashboard %s (scheduler: %s)", url, "dashboard" if with_scheduler else "external")
    print(f"Dashboard: {url}   (Ctrl+C to stop)")
    print("Scheduler: " + (f"every {cfg['schedule']['interval_minutes']} min (in this window)"
                           if with_scheduler else "external (Task Scheduler / cron)"))
    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()  # only after the socket is bound
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        httpd.server_close()
    return 0
````

### FILE: `src/vero_latency/stats.py`

````python
"""Latency statistics and time buckets for the dashboard."""
from __future__ import annotations

import math

BUCKET_STEPS = [60, 300, 900, 1800, 3600, 7200, 21600, 43200, 86400]


def percentile(values: list[float], pct: float) -> float | None:
    """Linear interpolation between closest ranks (same as numpy default)."""
    if not values:
        return None
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * pct / 100.0
    lo, hi = math.floor(k), math.ceil(k)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def _r(x):
    return None if x is None else round(x, 1)


def summarize(probes: list[dict], warn_ms: float, crit_ms: float) -> dict:
    """Availability counts every probe; latency figures use successful probes only."""
    total = len(probes)
    ok = [p for p in probes if p["status"] == "ok"]
    lat = [p["total_ms"] for p in ok]
    fb = [p["first_byte_ms"] for p in ok if p.get("first_byte_ms") is not None]
    last = probes[-1] if probes else None
    return {
        "probes": total,
        "ok": len(ok),
        "failed": total - len(ok),
        "availability_percent": round(len(ok) / total * 100, 2) if total else None,
        "avg_ms": _r(sum(lat) / len(lat)) if lat else None,
        "min_ms": _r(min(lat)) if lat else None,
        "p50_ms": _r(percentile(lat, 50)),
        "p95_ms": _r(percentile(lat, 95)),
        "p99_ms": _r(percentile(lat, 99)),
        "max_ms": _r(max(lat)) if lat else None,
        "first_byte_p50_ms": _r(percentile(fb, 50)),
        "warn_breaches": sum(1 for x in lat if warn_ms <= x < crit_ms),
        "crit_breaches": sum(1 for x in lat if x >= crit_ms),
        "last": {k: last[k] for k in ("ts", "status", "total_ms", "model")} if last else None,
    }


def bucket_seconds(range_hours: float, target_points: int = 200) -> int:
    raw = range_hours * 3600 / target_points
    for step in BUCKET_STEPS:
        if step >= raw:
            return step
    return BUCKET_STEPS[-1]


def series(probes: list[dict], bucket_s: int) -> dict:
    """Per model: list of buckets {t, n, fail, p50, p95, avg} ordered by time."""
    grouped: dict[str, dict[int, list[dict]]] = {}
    for p in probes:
        b = int(p["epoch"] // bucket_s * bucket_s)
        grouped.setdefault(p["model"], {}).setdefault(b, []).append(p)
    out = {}
    for model, buckets in grouped.items():
        rows = []
        for t in sorted(buckets):
            items = buckets[t]
            lat = [p["total_ms"] for p in items if p["status"] == "ok"]
            rows.append({
                "t": t,
                "n": len(items),
                "fail": sum(1 for p in items if p["status"] != "ok"),
                "p50": _r(percentile(lat, 50)),
                "p95": _r(percentile(lat, 95)),
                "avg": _r(sum(lat) / len(lat)) if lat else None,
            })
        out[model] = rows
    return out
````

### FILE: `src/vero_latency/store.py`

````python
"""SQLite storage for probe results. One file: <data_dir>/latency.db."""
from __future__ import annotations

import contextlib
import csv
import io
import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id        TEXT PRIMARY KEY,
    started_at    TEXT NOT NULL,
    finished_at   TEXT,
    trigger       TEXT NOT NULL,
    host          TEXT,
    tool_version  TEXT,
    cli_version   TEXT,
    prompt_sha256 TEXT
);
CREATE TABLE IF NOT EXISTS probes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        TEXT NOT NULL REFERENCES runs(run_id),
    ts            TEXT NOT NULL,
    epoch         REAL NOT NULL,
    model         TEXT NOT NULL,
    model_id      TEXT,
    status        TEXT NOT NULL,
    total_ms      REAL,
    first_byte_ms REAL,
    exit_code     INTEGER,
    out_chars     INTEGER,
    error         TEXT
);
CREATE INDEX IF NOT EXISTS ix_probes_epoch ON probes(epoch);
CREATE INDEX IF NOT EXISTS ix_probes_model ON probes(model, epoch);
"""

PROBE_COLS = ["id", "run_id", "ts", "epoch", "model", "model_id", "status",
              "total_ms", "first_byte_ms", "exit_code", "out_chars", "error"]


class Store:
    def __init__(self, data_dir: str | Path):
        self.path = Path(data_dir) / "latency.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.execute("PRAGMA journal_mode=WAL")
            c.executescript(SCHEMA)

    @contextlib.contextmanager
    def _conn(self):
        """Commit on success, roll back on error, always close (no leaked file handles on Windows)."""
        c = sqlite3.connect(self.path, timeout=30)
        c.row_factory = sqlite3.Row
        try:
            with c:
                yield c
        finally:
            c.close()

    # writes -------------------------------------------------------------
    def run_exists(self, run_id: str) -> bool:
        with self._conn() as c:
            return c.execute("SELECT 1 FROM runs WHERE run_id=?", (run_id,)).fetchone() is not None

    def start_run(self, run: dict) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO runs(run_id, started_at, trigger, host, tool_version, cli_version, prompt_sha256)"
                " VALUES(:run_id, :started_at, :trigger, :host, :tool_version, :cli_version, :prompt_sha256)",
                run,
            )

    def finish_run(self, run_id: str, finished_at: str) -> None:
        with self._conn() as c:
            c.execute("UPDATE runs SET finished_at=? WHERE run_id=?", (finished_at, run_id))

    def add_probe(self, p: dict) -> int:
        cols = [k for k in PROBE_COLS if k != "id"]
        with self._conn() as c:
            cur = c.execute(
                f"INSERT INTO probes({', '.join(cols)}) VALUES({', '.join(':' + k for k in cols)})",
                {k: p.get(k) for k in cols},
            )
            return cur.lastrowid

    def prune(self, retention_days: int) -> int:
        cutoff = time.time() - retention_days * 86400
        with self._conn() as c:
            n = c.execute("DELETE FROM probes WHERE epoch < ?", (cutoff,)).rowcount
            c.execute("DELETE FROM runs WHERE finished_at IS NOT NULL"
                      " AND run_id NOT IN (SELECT DISTINCT run_id FROM probes)")
            return n

    # reads --------------------------------------------------------------
    def probes(self, since_epoch: float = 0, model: str | None = None,
               after_id: int = 0, limit: int | None = None, newest_first: bool = False) -> list[dict]:
        q = "SELECT * FROM probes WHERE epoch >= ? AND id > ?"
        args: list = [since_epoch, after_id]
        if model:
            q += " AND model = ?"
            args.append(model)
        q += " ORDER BY epoch DESC, id DESC" if newest_first else " ORDER BY epoch, id"
        if limit:
            q += " LIMIT ?"
            args.append(limit)
        with self._conn() as c:
            return [dict(r) for r in c.execute(q, args)]

    def last_run(self) -> dict | None:
        with self._conn() as c:
            r = c.execute("SELECT * FROM runs ORDER BY started_at DESC LIMIT 1").fetchone()
            return dict(r) if r else None

    def max_probe_id(self) -> int:
        with self._conn() as c:
            return c.execute("SELECT COALESCE(MAX(id), 0) FROM probes").fetchone()[0]

    def to_csv(self, since_epoch: float = 0, model: str | None = None) -> str:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(PROBE_COLS)
        for r in self.probes(since_epoch, model):
            w.writerow([r[k] for k in PROBE_COLS])
        return buf.getvalue()
````

### FILE: `src/vero_latency/web/dashboard.html`

````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vero Latency Monitor</title>
<!--STATIC_DATA-->
<style>
:root{
  --ink:#1b2230; --mut:#5d6878; --line:#dde2ea; --paper:#ffffff; --soft:#f4f6f9; --card:#ffffff;
  --brand:#0a6aa1;
  --ok:#1f7a45; --warn:#a8500b; --crit:#9b1c2e; --na:#8a94a3;
  --s1:#0a6aa1; --s2:#0d8a6a; --s3:#7a3fb8; --s4:#a8660f; --s5:#2f5fd0; --s6:#b0306a;
  --sans:"IBM Plex Sans","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Consolas,"Courier New",monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ink:#e6eaf0; --mut:#9aa5b4; --line:#2c3441; --paper:#12161d; --soft:#1a2029; --card:#161b23;
    --brand:#4fa8dc; --ok:#4cc38a; --warn:#e39a4b; --crit:#f06b7f; --na:#6f7a89;
    --s1:#4fa8dc; --s2:#3fbf98; --s3:#b48be6; --s4:#e0a54a; --s5:#7f9df0; --s6:#e577a8;
  }
}
:root[data-theme="dark"]{
  --ink:#e6eaf0; --mut:#9aa5b4; --line:#2c3441; --paper:#12161d; --soft:#1a2029; --card:#161b23;
  --brand:#4fa8dc; --ok:#4cc38a; --warn:#e39a4b; --crit:#f06b7f; --na:#6f7a89;
  --s1:#4fa8dc; --s2:#3fbf98; --s3:#b48be6; --s4:#e0a54a; --s5:#7f9df0; --s6:#e577a8;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.5 var(--sans)}
.wrap{max-width:1280px;margin:0 auto;padding:22px 24px 48px}
header{display:flex;flex-wrap:wrap;gap:14px 24px;align-items:flex-end;justify-content:space-between;
  padding-bottom:16px;border-bottom:1px solid var(--line)}
.kicker{font-size:12.5px;color:var(--mut);letter-spacing:.02em}
h1{font-size:24px;margin:2px 0 0;font-weight:700;letter-spacing:-.01em}
.hright{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.pill{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;padding:4px 10px;border-radius:999px;
  border:1px solid var(--line);background:var(--soft);color:var(--mut)}
.dot{width:8px;height:8px;border-radius:50%;background:var(--na)}
.pill.live .dot{background:var(--ok);animation:pulse 2s infinite}
.pill.busy .dot{background:var(--brand);animation:pulse 1s infinite}
.pill.down .dot{background:var(--crit)}
@keyframes pulse{50%{opacity:.35}}
@media (prefers-reduced-motion:reduce){.pill .dot{animation:none!important}}
button,select,a.btn{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--card);color:var(--ink);
  border-radius:6px;padding:6px 12px;cursor:pointer;text-decoration:none;display:inline-block}
button.primary{background:var(--brand);border-color:var(--brand);color:#fff;font-weight:600}
button:disabled{opacity:.55;cursor:default}
button:focus-visible,select:focus-visible,a:focus-visible{outline:2px solid var(--brand);outline-offset:2px}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:16px 0 2px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.seg button{border:0;border-radius:0;border-right:1px solid var(--line);padding:6px 12px;background:var(--card)}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--paper);font-weight:600}
.spacer{flex:1}
.muted{color:var(--mut)}
.kpis{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-top:16px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;min-width:0}
.kpi .l{font-size:12px;color:var(--mut)}
.kpi .v{font-size:24px;font-weight:700;font-variant-numeric:tabular-nums;margin-top:2px;white-space:nowrap}
.kpi .s{font-size:12px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.v.ok{color:var(--ok)} .v.warn{color:var(--warn)} .v.crit{color:var(--crit)}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin-top:14px;min-width:0}
.card h2{font-size:15px;margin:0 0 2px}
.card .sub{font-size:12.5px;color:var(--mut);margin-bottom:8px}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--mut);margin:4px 0 6px}
.legend i{display:inline-block;width:14px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px}
#chart{position:relative}
#chart svg{display:block;width:100%;height:300px}
#chart text{font:11px var(--sans);fill:var(--mut)}
.tip{position:absolute;pointer-events:none;background:var(--card);border:1px solid var(--line);border-radius:6px;
  padding:7px 10px;font-size:12px;box-shadow:0 4px 14px rgba(0,0,0,.12);display:none;min-width:160px;z-index:2}
.tip b{display:block;margin-bottom:3px}
.tip .r{display:flex;gap:8px;justify-content:space-between;font-variant-numeric:tabular-nums}
.grid2{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:14px}
.grid2 .card{margin-top:14px}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;white-space:nowrap}
th{font-weight:600;color:var(--mut);font-size:12px}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
tr.new td{animation:flash 2.4s ease-out}
@keyframes flash{from{background:color-mix(in srgb,var(--brand) 18%,transparent)}to{background:transparent}}
.badge{display:inline-block;font-size:11.5px;font-weight:600;padding:1px 8px;border-radius:999px;
  border:1px solid currentColor;line-height:1.5}
.b-ok{color:var(--ok)} .b-warn,.b-unexpected{color:var(--warn)} .b-crit,.b-error,.b-timeout{color:var(--crit)}
.swatch{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.empty{padding:30px 10px;text-align:center;color:var(--mut)}
.err{color:var(--crit);font-size:12px;white-space:normal;max-width:420px}
footer{margin-top:22px;font-size:12px;color:var(--mut);display:flex;flex-wrap:wrap;gap:6px 20px}
footer code{font-family:var(--mono);font-size:11.5px}
.static-only{display:none}
body.static .live-only{display:none!important}
body.static .static-only{display:inline-flex}
@media (max-width:1050px){.kpis{grid-template-columns:repeat(3,minmax(0,1fr))}.grid2{grid-template-columns:1fr}}
@media (max-width:560px){.wrap{padding:16px 16px 40px}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}
  .kpi .v{font-size:20px}#chart svg{height:240px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <div class="kicker">Quality AI Automation · ASPF-1578 · Vero CLI</div>
      <h1>Vero CLI latency</h1>
    </div>
    <div class="hright">
      <span class="pill live-only" id="live"><span class="dot"></span><span id="liveText">Connecting…</span></span>
      <span class="pill live-only" id="next"><span id="nextText">Next run: –</span></span>
      <span class="pill static-only" id="staticPill"><span class="dot"></span><span id="staticText">Static report</span></span>
      <button class="primary live-only" id="runBtn" type="button">Run probe now</button>
      <a class="btn live-only" id="csvBtn" href="#">Export CSV</a>
      <button id="themeBtn" type="button" aria-label="Toggle light or dark theme">Theme</button>
    </div>
  </header>

  <div class="controls live-only">
    <div class="seg" id="range" role="group" aria-label="Time range">
      <button type="button" data-h="1">1 h</button><button type="button" data-h="6">6 h</button>
      <button type="button" data-h="24">24 h</button><button type="button" data-h="168">7 d</button>
      <button type="button" data-h="720">30 d</button>
    </div>
    <label class="muted">Model
      <select id="model"><option value="">All models</option></select></label>
    <span class="spacer"></span>
    <span class="muted" id="updated"></span>
  </div>

  <section class="kpis" id="kpis" aria-label="Key figures"></section>

  <section class="card">
    <h2>Latency over time</h2>
    <div class="sub" id="chartSub">Successful probes, total wall-clock time of one Vero CLI call.</div>
    <div class="legend" id="legend"></div>
    <div id="chart"><div class="tip" id="tip"></div></div>
  </section>

  <div class="grid2">
    <section class="card">
      <h2>Per model</h2>
      <div class="sub">Latency figures use successful probes; availability counts every probe.</div>
      <div class="tw"><table id="models"></table></div>
    </section>
    <section class="card">
      <h2>Recent probes <span class="muted live-only" style="font-weight:400;font-size:12px">· live</span></h2>
      <div class="sub">Newest first. Hover a status for the error message.</div>
      <div class="tw"><table id="recent"></table></div>
    </section>
  </div>

  <section class="card" id="failCard">
    <h2>Failures</h2>
    <div class="sub">Errors, timeouts and unexpected answers in the selected range (latest 50).</div>
    <div class="tw"><table id="failures"></table></div>
  </section>

  <footer id="foot"></footer>
</div>

<script>
(function(){
"use strict";
const STATIC = window.STATIC_DATA || null;
const $ = (id) => document.getElementById(id);
const SERIES = ["--s1","--s2","--s3","--s4","--s5","--s6"];
const state = { hours: 24, model: "", data: null, es: null, reloadT: null };
try { const h = +localStorage.getItem("vlm.hours"); if ([1,6,24,168,720].includes(h)) state.hours = h; } catch(e){}
try { const t = localStorage.getItem("vlm.theme"); if (t) document.documentElement.dataset.theme = t; } catch(e){}

const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function fmtMs(v){ if (v == null) return "–"; return v < 1000 ? Math.round(v) + " ms" : (v/1000).toFixed(v < 10000 ? 2 : 1) + " s"; }
function fmtPct(v){ return v == null ? "–" : (v >= 99.95 ? "100" : v.toFixed(1)) + "%"; }
function band(v){ if (v == null || !state.data) return ""; const t = state.data.config.thresholds_ms;
  return v >= t.crit ? "crit" : v >= t.warn ? "warn" : "ok"; }
function fmtTime(ts){ const d = new Date(ts); return d.toLocaleString(undefined,{month:"short",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit"}); }
function nowMs(){ return STATIC ? new Date(STATIC.generated_at).getTime() : Date.now(); }
function ago(ts){ const s = Math.max(0, Math.round((nowMs() - new Date(ts))/1000));
  if (s < 60) return s + " s ago"; if (s < 3600) return Math.round(s/60) + " min ago";
  if (s < 86400) return Math.round(s/3600) + " h ago"; return Math.round(s/86400) + " d ago"; }
function colorOf(model){ const ms = state.data ? state.data.config.models : [];
  let i = ms.indexOf(model); if (i < 0) i = ms.length + [...model].reduce((a,c)=>a+c.charCodeAt(0),0);
  return css(SERIES[i % SERIES.length]); }
function statusBadge(p){
  let cls = p.status, label = p.status;
  if (p.status === "ok") { const b = band(p.total_ms); cls = b; label = b === "ok" ? "ok" : b === "warn" ? "slow" : "very slow"; }
  return `<span class="badge b-${cls}" title="${esc(p.error || "")}">${esc(label)}</span>`;
}

// data ------------------------------------------------------------------
async function load(){
  if (STATIC) { render(STATIC); return; }
  const q = `hours=${state.hours}&model=${encodeURIComponent(state.model)}`;
  $("csvBtn").href = "/api/export.csv?" + q;
  try {
    const r = await fetch("/api/dashboard?" + q, {cache:"no-store"});
    render(await r.json());
  } catch(e){ setLive("down", "Server not reachable"); }
}
function scheduleReload(){ clearTimeout(state.reloadT); state.reloadT = setTimeout(load, 700); }

// render ----------------------------------------------------------------
function render(d){
  state.data = d;
  const sel = $("model");
  if (sel.options.length === 1) d.config.models.forEach(m => sel.add(new Option(m, m)));
  document.querySelectorAll("#range button").forEach(b => b.setAttribute("aria-pressed", +b.dataset.h === state.hours));
  $("updated").textContent = "Updated " + new Date(d.generated_at).toLocaleTimeString();
  renderKpis(d); renderChart(d); renderModels(d); renderRecent(d.recent); renderFailures(d.failures); renderFoot(d);
  setRunning(d.state.running); state.nextRun = d.state.next_run_epoch; tickNext();
  if (STATIC) { $("staticText").textContent = `Static report · last ${rangeLabel(d.range_hours)} · generated ${fmtTime(d.generated_at)}`; }
}
function rangeLabel(h){ return h >= 48 ? (h/24) + " d" : h + " h"; }

function renderKpis(d){
  const o = d.overall, t = d.config.thresholds_ms, L = o.last;
  const tiles = [
    ["Last probe", L ? fmtMs(L.total_ms) : "–", L ? (L.status === "ok" ? band(L.total_ms) : "crit") : "",
      L ? `${L.model} · ${L.status} · ${ago(L.ts)}` : "no probes yet"],
    ["Median (p50)", fmtMs(o.p50_ms), band(o.p50_ms), `avg ${fmtMs(o.avg_ms)} · 1st byte ${fmtMs(o.first_byte_p50_ms)}`],
    ["p95", fmtMs(o.p95_ms), band(o.p95_ms), `p99 ${fmtMs(o.p99_ms)} · max ${fmtMs(o.max_ms)}`],
    ["Availability", fmtPct(o.availability_percent),
      o.availability_percent == null ? "" : o.availability_percent >= 99 ? "ok" : o.availability_percent >= 95 ? "warn" : "crit",
      `${o.ok} ok of ${o.probes}`],
    ["Probes", String(o.probes), "", `${o.failed} failed · last ${rangeLabel(d.range_hours)}`],
    ["Threshold breaches", String(o.warn_breaches + o.crit_breaches), o.crit_breaches ? "crit" : o.warn_breaches ? "warn" : (o.probes ? "ok" : ""),
      `≥ ${fmtMs(t.warn)}: ${o.warn_breaches} · ≥ ${fmtMs(t.crit)}: ${o.crit_breaches}`],
  ];
  $("kpis").innerHTML = tiles.map(([l,v,c,s]) =>
    `<div class="kpi"><div class="l">${l}</div><div class="v ${c}">${esc(v)}</div><div class="s" title="${esc(s)}">${esc(s)}</div></div>`).join("");
}

function niceMax(v){ if (v <= 0) return 1000; const p = Math.pow(10, Math.floor(Math.log10(v))); const n = v / p;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * p; }

function renderChart(d){
  const box = $("chart"), tip = $("tip");
  box.querySelectorAll("svg,.empty").forEach(n => n.remove());
  const models = Object.keys(d.series.models);
  const th = d.config.thresholds_ms;
  $("legend").innerHTML = models.map(m => `<span><i style="background:${colorOf(m)}"></i>${esc(m)}</span>`).join("")
    + (models.length ? `<span>solid p50 · dotted p95 per ${fmtBucket(d.series.bucket_s)}</span><span><i style="background:${css("--crit")};height:8px;width:3px"></i>failure</span>` : "");
  if (!models.length) { box.insertAdjacentHTML("afterbegin", `<div class="empty">No probes in this range yet. ${STATIC ? "" : "Click <b>Run probe now</b> or wait for the schedule."}</div>`); return; }

  const W = Math.max(320, box.clientWidth), H = W < 560 ? 240 : 300;
  const m = {l: 58, r: 14, t: 12, b: 30};
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const end = new Date(d.generated_at).getTime()/1000, start = end - d.range_hours*3600;
  let vmax = 0;
  models.forEach(k => d.series.models[k].forEach(b => { vmax = Math.max(vmax, b.p95 || 0, b.p50 || 0); }));
  const ymax = niceMax(vmax * 1.12);
  const x = (t) => m.l + (Math.min(Math.max(t, start), end) - start) / (end - start) * iw;
  const y = (v) => m.t + ih - v / ymax * ih;
  const gap = Math.max(d.series.bucket_s, d.config.interval_minutes*60) * 2.5;
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Latency over time per model">`;
  for (let i = 0; i <= 4; i++) { const v = ymax * i / 4, yy = y(v);
    s += `<line x1="${m.l}" x2="${W-m.r}" y1="${yy}" y2="${yy}" stroke="${css("--line")}" stroke-width="1"/>`;
    s += `<text x="${m.l-8}" y="${yy+4}" text-anchor="end">${fmtMs(v)}</text>`; }
  xTicks(start, end, d.range_hours).forEach(t => { const xx = x(t);
    s += `<line x1="${xx}" x2="${xx}" y1="${m.t+ih}" y2="${m.t+ih+4}" stroke="${css("--mut")}"/>`;
    s += `<text x="${xx}" y="${H-8}" text-anchor="middle">${fmtTick(t, d.range_hours)}</text>`; });
  [["warn", th.warn], ["crit", th.crit]].forEach(([k, v]) => { if (v <= ymax) { const yy = y(v);
    s += `<line x1="${m.l}" x2="${W-m.r}" y1="${yy}" y2="${yy}" stroke="${css("--"+k)}" stroke-dasharray="6 4" stroke-width="1.2"/>`;
    s += `<text x="${W-m.r-4}" y="${yy-4}" text-anchor="end" style="fill:${css("--"+k)}">${k} ${fmtMs(v)}</text>`; } });
  models.forEach(k => {
    const col = colorOf(k), rows = d.series.models[k];
    ["p95","p50"].forEach(f => {
      let path = "", prev = null;
      rows.forEach(b => { if (b[f] == null) { prev = null; return; }
        const cmd = (prev === null || b.t - prev > gap) ? "M" : "L";
        path += `${cmd}${x(b.t + d.series.bucket_s/2).toFixed(1)},${y(b[f]).toFixed(1)}`; prev = b.t; });
      if (path) s += `<path d="${path}" fill="none" stroke="${col}" stroke-width="${f === "p50" ? 2 : 1.2}" ${f === "p95" ? 'stroke-dasharray="2 3" opacity=".75"' : ""} stroke-linejoin="round" stroke-linecap="round"/>`;
    });
    if (rows.length <= 80) rows.forEach(b => { if (b.p50 != null)
      s += `<circle cx="${x(b.t + d.series.bucket_s/2).toFixed(1)}" cy="${y(b.p50).toFixed(1)}" r="2.6" fill="${col}"/>`; });
  });
  d.failures.forEach(f => { if (f.epoch >= start) { const xx = x(f.epoch);
    s += `<rect x="${(xx-1.5).toFixed(1)}" y="${m.t+ih-10}" width="3" height="10" fill="${css("--crit")}"><title>${esc(f.model)} ${esc(f.status)} ${fmtTime(f.ts)}</title></rect>`; } });
  s += `<line id="hair" x1="0" x2="0" y1="${m.t}" y2="${m.t+ih}" stroke="${css("--mut")}" stroke-width="1" visibility="hidden"/>`;
  s += `<rect id="hit" x="${m.l}" y="${m.t}" width="${iw}" height="${ih}" fill="transparent"/></svg>`;
  box.insertAdjacentHTML("afterbegin", s);

  const svg = box.querySelector("svg"), hair = svg.querySelector("#hair");
  const times = [...new Set(models.flatMap(k => d.series.models[k].map(b => b.t)))].sort((a,b)=>a-b);
  svg.querySelector("#hit").addEventListener("mousemove", ev => {
    const r = svg.getBoundingClientRect(), px = (ev.clientX - r.left) * W / r.width;
    const t = start + (px - m.l) / iw * (end - start) - d.series.bucket_s/2;
    let best = times[0]; times.forEach(tt => { if (Math.abs(tt - t) < Math.abs(best - t)) best = tt; });
    const xx = x(best + d.series.bucket_s/2);
    hair.setAttribute("x1", xx); hair.setAttribute("x2", xx); hair.setAttribute("visibility", "visible");
    let h = `<b>${fmtTime(best*1000)}</b>`;
    models.forEach(k => { const b = d.series.models[k].find(z => z.t === best); if (!b) return;
      h += `<div class="r"><span><span class="swatch" style="background:${colorOf(k)}"></span>${esc(k)}</span><span>${fmtMs(b.p50)}</span></div>`;
      h += `<div class="r muted"><span>p95 · n · fail</span><span>${fmtMs(b.p95)} · ${b.n} · ${b.fail}</span></div>`; });
    tip.innerHTML = h; tip.style.display = "block";
    const left = xx * r.width / W; tip.style.left = Math.min(left + 12, r.width - tip.offsetWidth - 4) + "px"; tip.style.top = "10px";
  });
  svg.querySelector("#hit").addEventListener("mouseleave", () => { tip.style.display = "none"; hair.setAttribute("visibility","hidden"); });
}
function fmtBucket(s){ return s < 3600 ? (s/60) + " min" : s < 86400 ? (s/3600) + " h" : (s/86400) + " d"; }
function xTicks(start, end, h){
  const step = h <= 1 ? 600 : h <= 6 ? 3600 : h <= 24 ? 4*3600 : h <= 168 ? 86400 : 5*86400;
  const off = new Date().getTimezoneOffset()*60, out = [];
  for (let t = Math.ceil((start - off) / step) * step + off; t <= end; t += step) out.push(t);
  return out;
}
function fmtTick(t, h){ const d = new Date(t*1000);
  return h <= 24 ? d.toLocaleTimeString(undefined,{hour:"2-digit",minute:"2-digit"}) : d.toLocaleDateString(undefined,{day:"2-digit",month:"short"}); }

function renderModels(d){
  const rows = d.per_model;
  $("models").innerHTML = `<thead><tr><th>Model</th><th class="n">Probes</th><th class="n">Avail.</th><th class="n">p50</th><th class="n">p95</th><th class="n">Max</th><th class="n">1st byte p50</th><th>Last</th></tr></thead><tbody>`
    + (rows.length ? rows.map(r => `<tr><td><span class="swatch" style="background:${colorOf(r.model)}"></span>${esc(r.model)}</td>
      <td class="n">${r.probes}</td><td class="n">${fmtPct(r.availability_percent)}</td>
      <td class="n">${fmtMs(r.p50_ms)}</td><td class="n">${fmtMs(r.p95_ms)}</td><td class="n">${fmtMs(r.max_ms)}</td>
      <td class="n">${fmtMs(r.first_byte_p50_ms)}</td><td>${r.last ? ago(r.last.ts) : "–"}</td></tr>`).join("")
      : `<tr><td colspan="8" class="empty">No data</td></tr>`) + "</tbody>";
}
function recentRow(p, isNew){
  return `<tr${isNew ? ' class="new"' : ""}><td>${fmtTime(p.ts)}</td><td><span class="swatch" style="background:${colorOf(p.model)}"></span>${esc(p.model)}</td>
    <td>${statusBadge(p)}</td><td class="n">${fmtMs(p.total_ms)}</td><td class="n">${fmtMs(p.first_byte_ms)}</td></tr>`;
}
function renderRecent(list){
  $("recent").innerHTML = `<thead><tr><th>Time</th><th>Model</th><th>Status</th><th class="n">Total</th><th class="n">1st byte</th></tr></thead><tbody>`
    + (list.length ? list.slice(0, 15).map(p => recentRow(p, false)).join("") : `<tr><td colspan="5" class="empty">No probes yet</td></tr>`) + "</tbody>";
}
function renderFailures(list){
  $("failCard").style.display = list.length ? "" : "none";
  $("failures").innerHTML = `<thead><tr><th>Time</th><th>Model</th><th>Status</th><th>Message</th></tr></thead><tbody>`
    + list.slice().reverse().map(f => `<tr><td>${fmtTime(f.ts)}</td><td>${esc(f.model)}</td><td>${statusBadge(f)}</td><td class="err">${esc(f.error)}</td></tr>`).join("") + "</tbody>";
}
function renderFoot(d){
  const c = d.config, lr = d.state.last_run;
  $("foot").innerHTML = [
    `Prompt <code>${esc(c.prompt)}</code>`,
    `Interval ${c.interval_minutes} min (${d.state.scheduler === "dashboard" ? "dashboard scheduler" : "Task Scheduler / cron"})`,
    `Timeout ${c.timeout_s} s`, `Warn ${fmtMs(c.thresholds_ms.warn)} · crit ${fmtMs(c.thresholds_ms.crit)}`,
    `Retention ${c.retention_days} d`,
    lr ? `Last run <code>${esc(lr.run_id)}</code> · Vero ${esc(lr.cli_version || "?")}` : "",
    `vero-latency ${esc(d.tool_version)}`].filter(Boolean).map(x => `<span>${x}</span>`).join("");
}

// live ------------------------------------------------------------------
function setLive(cls, text){ const p = $("live"); p.className = "pill live-only " + cls; $("liveText").textContent = text; }
function setRunning(r){ state.running = r; $("runBtn").disabled = !!r; $("runBtn").textContent = r ? "Probing…" : "Run probe now";
  if (state.es && state.es.readyState === 1) setLive(r ? "busy" : "live", r ? "Probing Vero CLI…" : "Live"); }
function tickNext(){
  if (STATIC || !state.data) return;
  const n = state.nextRun;
  if (!n) { $("nextText").textContent = "Next run: –"; return; }
  const s = Math.max(0, Math.round(n - Date.now()/1000));
  const who = state.data.state.scheduler === "external" ? " (Task Scheduler)" : "";
  $("nextText").textContent = `Next run in ${Math.floor(s/60)}:${String(s%60).padStart(2,"0")}${who}`;
}
function connect(){
  const es = new EventSource("/api/stream"); state.es = es;
  es.onopen = () => setLive(state.running ? "busy" : "live", state.running ? "Probing Vero CLI…" : "Live");
  es.onerror = () => setLive("down", "Reconnecting…");
  es.addEventListener("state", ev => { const s = JSON.parse(ev.data); state.nextRun = s.next_run_epoch; setRunning(s.running); tickNext(); });
  es.addEventListener("probe", ev => {
    const p = JSON.parse(ev.data);
    if (state.model && p.model !== state.model) return;
    const tb = $("recent").tBodies[0];
    if (tb) { if (tb.querySelector(".empty")) tb.innerHTML = ""; tb.insertAdjacentHTML("afterbegin", recentRow(p, true));
      while (tb.rows.length > 15) tb.deleteRow(-1); }
    scheduleReload();
  });
}

// wiring ----------------------------------------------------------------
if (STATIC) { document.body.classList.add("static"); load(); }
else {
  document.querySelectorAll("#range button").forEach(b => b.addEventListener("click", () => {
    state.hours = +b.dataset.h; try { localStorage.setItem("vlm.hours", state.hours); } catch(e){} load(); }));
  $("model").addEventListener("change", e => { state.model = e.target.value; load(); });
  $("runBtn").addEventListener("click", async () => {
    setRunning(true);
    try { const r = await fetch("/api/probe", {method:"POST"}); if (r.status >= 400 && r.status !== 409) setRunning(false); }
    catch(e){ setRunning(false); }
  });
  load().then(connect);  // first paint from data, then open the live stream
  setInterval(tickNext, 1000);
  setInterval(load, 60000);
}
$("themeBtn").addEventListener("click", () => {
  const cur = document.documentElement.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  const nxt = cur === "dark" ? "light" : "dark"; document.documentElement.dataset.theme = nxt;
  try { localStorage.setItem("vlm.theme", nxt); } catch(e){}
  if (state.data) render(state.data);
});
let rz; addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(() => state.data && renderChart(state.data), 150); });
})();
</script>
</body>
</html>
````

### FILE: `start_dashboard.bat`

````bat
@echo off
rem Opens the dashboard; starts it first if it is not running. Keep this window open in that case.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py serve --open
pause
````

### FILE: `status.bat`

````bat
@echo off
rem Shows configuration, last run, dashboard and Task Scheduler state.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py status
pause
````

### FILE: `tests/__init__.py`

````python
"""Test package."""
````

### FILE: `tests/conftest.py`

````python
"""Shared test helpers (works with unittest and pytest)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
FAKE = ROOT / "scripts" / "fake_vero.py"


def demo_config(data_dir, **over):
    from vero_latency import config
    cfg = config._merge(config.DEFAULTS, {
        "cli": {"command": [sys.executable, str(FAKE), "-p", "{prompt}", "--model", "{model}"],
                "version_command": [sys.executable, str(FAKE), "--version"], "timeout_s": 10},
        "models": [{"id": "fake-mini", "label": "mini"}],
        "data_dir": str(data_dir),
    })
    cfg = config._merge(cfg, over)
    config.validate(cfg)
    return cfg
````

### FILE: `tests/fixtures/.gitkeep`

````
# keeps the folder in Git (synthetic fixtures only)
````

### FILE: `tests/integration/__init__.py`

````python
"""Test package."""
````

### FILE: `tests/integration/test_cycle.py`

````python
"""End to end with the bundled fake Vero CLI: probe, store, manifest, dashboard payload, HTTP."""
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

import tests.conftest as h
from vero_latency.probe import run_cycle, time_command
from vero_latency.scheduler import Loop
from vero_latency.server import make_handler, static_report
from vero_latency.store import Store


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class CycleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["FAKE_VERO_DELAY"] = "0.05"
        os.environ["FAKE_VERO_FAIL"] = "0"

    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("FAKE_VERO_DELAY", None)
        os.environ.pop("FAKE_VERO_FAIL", None)

    def test_cycle_records_probe_and_manifest(self):
        cfg = h.demo_config(self.tmp.name, models=[{"id": "fake-mini", "label": "mini"},
                                                   {"id": "fake-std", "label": "std"}])
        store = Store(cfg["data_dir"])
        m = run_cycle(cfg, store, "manual")
        self.assertEqual(m["totals"], {"probes": 2, "ok": 2, "failed": 0})
        self.assertEqual(m["cli"]["version"], "vero-fake 0.0.1")
        self.assertRegex(m["run_id"], r"^\d{8}-\d{4}-vero-latency$")
        self.assertEqual(len(list(Path(cfg["data_dir"], "runs").rglob("*.json"))), 1)
        rows = store.probes()
        self.assertEqual(len(rows), 2)
        self.assertGreaterEqual(rows[0]["total_ms"], 50)
        self.assertIsNotNone(rows[0]["first_byte_ms"])
        m2 = run_cycle(cfg, store, "manual")
        self.assertNotEqual(m["run_id"], m2["run_id"])  # same minute -> suffix
        self.assertFalse(Path(cfg["data_dir"], "probe.lock").exists())

    def test_failure_and_timeout_recorded(self):
        os.environ["FAKE_VERO_FAIL"] = "1"
        cfg = h.demo_config(self.tmp.name)
        m = run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        self.assertEqual(m["results"][0]["status"], "error")
        os.environ["FAKE_VERO_FAIL"] = "0"
        os.environ["FAKE_VERO_DELAY"] = "5"
        cfg = h.demo_config(self.tmp.name, cli={"timeout_s": 0.5})
        m = run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        self.assertEqual(m["results"][0]["status"], "timeout")
        self.assertLess(m["results"][0]["total_ms"], 4000)

    @unittest.skipIf(os.name == "nt", "POSIX process groups")
    def test_timeout_kills_whole_tree_quickly(self):
        # regression: a grandchild kept the pipe open, the probe stalled ~10 s and left an orphan
        marker = f"sleep {37 + os.getpid() % 50}.5"
        t0 = time.time()
        r = time_command(["sh", "-c", f"{marker}; echo OK"], None, 0.5)
        self.assertTrue(r["timed_out"])
        self.assertLess(time.time() - t0, 3)
        time.sleep(0.2)
        alive = os.popen(f"pgrep -f '[s]{marker[1:]}'").read().strip()
        self.assertEqual(alive, "")

    def test_missing_executable(self):
        cfg = h.demo_config(self.tmp.name, cli={"command": ["no-such-vero-cli", "{prompt}"], "version_command": []})
        m = run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        self.assertEqual(m["results"][0]["status"], "error")

    def test_static_report_cannot_break_out_of_script(self):
        cfg = h.demo_config(self.tmp.name, models=[{"id": "fake-mini", "label": "</script><!--x"}])
        run_cycle(cfg, Store(cfg["data_dir"]), "manual")
        html = static_report(cfg, Store(cfg["data_dir"]), 24, None)
        blob = html.split("window.STATIC_DATA=", 1)[1].split(";</script>", 1)[0]
        self.assertNotIn("<", blob)
        self.assertEqual(json.loads(blob)["per_model"][0]["model"], "</script><!--x")


class HttpTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["FAKE_VERO_DELAY"] = "0.05"
        os.environ["FAKE_VERO_FAIL"] = "0"
        port = free_port()
        self.cfg = h.demo_config(self.tmp.name, server={"host": "127.0.0.1", "port": port})
        self.store = Store(self.cfg["data_dir"])
        run_cycle(self.cfg, self.store, "manual")
        self.loop = Loop(self.cfg, self.store)
        self.srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(self.cfg, self.store, self.loop))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{port}"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()
        os.environ.pop("FAKE_VERO_DELAY", None)
        os.environ.pop("FAKE_VERO_FAIL", None)

    def get(self, path, **headers):
        return urllib.request.urlopen(urllib.request.Request(self.base + path, headers=headers))

    def status(self, path, method="GET", **headers):
        try:
            return urllib.request.urlopen(urllib.request.Request(self.base + path, method=method, headers=headers)).status
        except urllib.error.HTTPError as e:
            return e.code

    def test_endpoints(self):
        with self.get("/api/dashboard?hours=1") as r:
            d = json.load(r)
        self.assertEqual(d["per_model"][0]["model"], "mini")
        self.assertEqual(d["state"]["scheduler"], "external")
        self.assertNotIn("env", json.dumps(d["config"]))
        with self.get("/api/export.csv") as r:
            self.assertEqual(r.read().decode().count("\n"), 2)
        with self.get("/") as r:
            self.assertIn(b"Vero CLI latency", r.read())
        with self.get("/api/health") as r:
            self.assertEqual(json.load(r)["app"], "vero-latency")

    def test_bad_hours_does_not_crash(self):
        with self.get("/api/dashboard?hours=abc") as r:
            self.assertEqual(json.load(r)["range_hours"], 24)

    def test_foreign_host_and_origin_rejected(self):
        self.assertEqual(self.status("/api/health", Host="evil.example"), 403)
        self.assertEqual(self.status("/api/probe", "POST", Origin="http://evil.example"), 403)

    def test_probe_now(self):
        self.assertEqual(self.status("/api/probe", "POST", Origin=self.base), 202)
        for _ in range(50):
            if not self.loop.running and len(self.store.probes()) == 2:
                break
            time.sleep(0.1)
        self.assertEqual(len(self.store.probes()), 2)


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/unit/__init__.py`

````python
"""Test package."""
````

### FILE: `tests/unit/test_config_scheduler.py`

````python
import json
import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import mock

import tests.conftest  # noqa: F401
from vero_latency import cli, config, scheduler

NS = "{http://schemas.microsoft.com/windows/2004/02/mit/task}"


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

    def test_notepad_bom_accepted(self):
        cfg = config.load(self.write({"models": [{"id": "m"}]}, bom=True))
        self.assertEqual(cfg["models"][0]["label"], "m")

    def test_bad_types_are_config_errors(self):
        for bad in ({"schedule": {"interval_minutes": "abc"}}, {"thresholds_ms": {"warn": 9, "crit": 1}},
                    {"models": []}, {"cli": {"command": "vero -p x"}}, {"models": [{"id": "a"}, {"id": "a"}]}):
            with self.assertRaises(config.ConfigError, msg=bad):
                config.load(self.write(bad))

    def test_windows_path_hint(self):
        p = self.dir / "c.json"
        p.write_text('{"data_dir": "C:\\Tools\\x"}')
        with self.assertRaisesRegex(config.ConfigError, "Windows paths"):
            config.load(p)

    def test_example_is_valid(self):
        cfg = config.load(config.EXAMPLE_FILE)
        self.assertEqual(cfg["schedule"]["interval_minutes"], 15)

    def test_data_dir_env_expansion(self):
        with mock.patch.dict(os.environ, {"VLM_TEST_DIR": str(self.dir)}):
            cfg = config.load(self.write({"data_dir": "$VLM_TEST_DIR/d" if os.name != "nt" else "%VLM_TEST_DIR%/d"}))
        self.assertEqual(Path(cfg["data_dir"]), self.dir / "d")

    def test_configure_wizard(self):
        target = self.dir / "monitor.json"
        answers = iter([f'"{sys.executable}" -p {{prompt}} --model {{model}}', "cheap-1, big-2", "5", "30", "4", "12"])
        with mock.patch("builtins.input", lambda *_: next(answers)), mock.patch("builtins.print"):
            rc = cli.main(["--config", str(target), "configure"])
        self.assertEqual(rc, 0)
        cfg = config.load(target)
        self.assertEqual(cfg["cli"]["command"][0], sys.executable)
        self.assertEqual([m["id"] for m in cfg["models"]], ["cheap-1", "big-2"])
        self.assertEqual(cfg["schedule"]["interval_minutes"], 5)
        self.assertEqual(cfg["thresholds_ms"], {"warn": 4000.0, "crit": 12000.0})

    def test_configure_recovers_from_broken_config(self):
        target = self.dir / "monitor.json"
        target.write_text("{ broken")
        answers = iter([f'"{sys.executable}" -p {{prompt}}', "", "15", "60", "5", "15"])
        with mock.patch("builtins.input", lambda *_: next(answers)), mock.patch("builtins.print"):
            self.assertEqual(cli.main(["--config", str(target), "configure"]), 0)
        self.assertEqual(config.load(target)["models"][0]["id"], "")

    def test_demo_uses_separate_data_dir(self):
        target = self.dir / "monitor.json"
        with mock.patch("builtins.print"):
            cli.main(["--config", str(target), "init", "--demo"])
        self.assertTrue(config.load(target)["data_dir"].endswith("data-demo"))


class TaskXmlTest(unittest.TestCase):
    def test_probe_task_is_laptop_safe(self):
        root = ET.fromstring(scheduler.probe_task_xml(15).split("\n", 1)[1])
        s = root.find(f"{NS}Settings")
        self.assertEqual(s.find(f"{NS}DisallowStartIfOnBatteries").text, "false")
        self.assertEqual(s.find(f"{NS}StopIfGoingOnBatteries").text, "false")
        self.assertEqual(s.find(f"{NS}StartWhenAvailable").text, "true")
        self.assertEqual(s.find(f"{NS}MultipleInstancesPolicy").text, "IgnoreNew")
        self.assertEqual(root.find(f".//{NS}Repetition/{NS}Interval").text, "PT15M")
        args = root.find(f".//{NS}Exec/{NS}Arguments").text
        self.assertIn("vlm.py", args)
        self.assertIn("--trigger task", args)
        self.assertTrue(root.find(f".//{NS}StartBoundary").text.endswith((":00:00", ":15:00", ":30:00", ":45:00")))

    def test_dashboard_task_runs_forever_at_logon(self):
        root = ET.fromstring(scheduler.dashboard_task_xml().split("\n", 1)[1])
        self.assertIsNotNone(root.find(f".//{NS}LogonTrigger"))
        self.assertEqual(root.find(f".//{NS}ExecutionTimeLimit").text, "PT0S")
        self.assertIn("--no-scheduler", root.find(f".//{NS}Exec/{NS}Arguments").text)

    def test_cron_expr(self):
        self.assertEqual(scheduler._cron_expr(15), "*/15 * * * *")
        self.assertEqual(scheduler._cron_expr(120), "0 */2 * * *")
        self.assertEqual(scheduler._cron_expr(1440), "0 0 * * *")

    def test_next_aligned(self):
        self.assertEqual(scheduler.next_aligned(900, 1000), 1800)
        self.assertEqual(scheduler.next_aligned(900, 1800), 2700)


if __name__ == "__main__":
    unittest.main()
````

### FILE: `tests/unit/test_probe.py`

````python
import unittest

import tests.conftest  # noqa: F401
from vero_latency.probe import build_command, classify


def res(**kw):
    base = {"total_ms": 10.0, "first_byte_ms": 5.0, "exit_code": 0, "stdout": "OK\n", "stderr": "", "timed_out": False}
    base.update(kw)
    return base


class BuildCommandTest(unittest.TestCase):
    T = ["nonexistent-vero", "-p", "{prompt}", "--model", "{model}"]

    def test_fills_placeholders(self):
        self.assertEqual(build_command(self.T, "hi", "m1", "arg"), ["nonexistent-vero", "-p", "hi", "--model", "m1"])

    def test_empty_model_drops_flag(self):
        self.assertEqual(build_command(self.T, "hi", "", "arg"), ["nonexistent-vero", "-p", "hi"])

    def test_stdin_mode_drops_prompt_arg(self):
        self.assertEqual(build_command(["v", "{prompt}"], "hi", "", "stdin"), ["v"])


class ClassifyTest(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(classify(res(), "ok"), ("ok", None))

    def test_timeout(self):
        self.assertEqual(classify(res(timed_out=True), "OK")[0], "timeout")

    def test_nonzero_exit(self):
        st, msg = classify(res(exit_code=2, stderr="guardrail blocked"), "OK")
        self.assertEqual(st, "error")
        self.assertIn("guardrail blocked", msg)

    def test_unexpected_answer(self):
        self.assertEqual(classify(res(stdout="I cannot help"), "OK")[0], "unexpected")

    def test_not_started(self):
        self.assertEqual(classify(res(total_ms=None, exit_code=None, stderr="cannot start"), "OK")[0], "error")


if __name__ == "__main__":
    unittest.main()


class LockTest(unittest.TestCase):
    def test_stale_lock_is_ignored_and_cleared(self):
        import os
        import tempfile
        import time
        from pathlib import Path

        from vero_latency.probe import RunLock, run_in_progress
        with tempfile.TemporaryDirectory() as d:
            cfg = {"data_dir": d, "cli": {"timeout_s": 1}, "models": [{}]}
            lock = Path(d) / "probe.lock"
            lock.write_text("123")
            self.assertTrue(run_in_progress(cfg))
            old = time.time() - 3600
            os.utime(lock, (old, old))
            self.assertFalse(run_in_progress(cfg))
            with RunLock(d, 121) as held:
                self.assertTrue(held.held)
            self.assertFalse(lock.exists())
````

### FILE: `tests/unit/test_stats.py`

````python
import unittest

import tests.conftest  # noqa: F401
from vero_latency import stats


def p(ms, status="ok", epoch=0, model="m"):
    return {"total_ms": ms, "first_byte_ms": ms, "status": status, "epoch": epoch, "model": model, "ts": "t"}


class StatsTest(unittest.TestCase):
    def test_percentile(self):
        self.assertIsNone(stats.percentile([], 50))
        self.assertEqual(stats.percentile([5], 95), 5)
        self.assertEqual(stats.percentile([1, 2, 3, 4], 50), 2.5)
        self.assertAlmostEqual(stats.percentile(list(range(1, 101)), 95), 95.05)

    def test_summary_counts_failures_in_availability_only(self):
        s = stats.summarize([p(100), p(200), p(9000, "timeout"), p(6000)], warn_ms=5000, crit_ms=8000)
        self.assertEqual((s["probes"], s["ok"], s["failed"]), (4, 3, 1))
        self.assertEqual(s["availability_percent"], 75.0)
        self.assertEqual(s["max_ms"], 6000)
        self.assertEqual((s["warn_breaches"], s["crit_breaches"]), (1, 0))

    def test_empty_summary(self):
        s = stats.summarize([], 1, 2)
        self.assertIsNone(s["availability_percent"])
        self.assertIsNone(s["last"])

    def test_bucket_seconds(self):
        self.assertEqual(stats.bucket_seconds(1), 60)
        self.assertEqual(stats.bucket_seconds(24), 900)
        self.assertEqual(stats.bucket_seconds(720), 21600)

    def test_series_groups_by_bucket(self):
        rows = [p(100, epoch=10), p(300, epoch=50), p(0, "error", epoch=70), p(500, epoch=130)]
        out = stats.series(rows, 60)["m"]
        self.assertEqual([b["t"] for b in out], [0, 60, 120])
        self.assertEqual(out[0]["p50"], 200)
        self.assertEqual(out[1]["fail"], 1)
        self.assertIsNone(out[1]["p50"])


if __name__ == "__main__":
    unittest.main()
````

### FILE: `uninstall.bat`

````bat
@echo off
rem Removes the scheduled tasks and the desktop shortcut. Data and config stay; delete the folder to remove everything.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py uninstall
pause
````

### FILE: `vlm.py`

````python
#!/usr/bin/env python3
"""Entry point. No install needed: python vlm.py <command>."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from vero_latency.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
````

---

## Verify the rebuild

Save as `verify_rebuild.py` (outside the project folder) and run it as described in step 5.

````python
import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vero-latency-monitor")
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
 "version": "0.2.0",
 "files": {
  ".ci/README.md": {
   "sha256_lf": "c7331553b5e31c7198b20ed5a6e793f4c4f9fdc0e460c989cf04c43a0c62f45a",
   "crlf": false,
   "bytes": 149
  },
  ".gitattributes": {
   "sha256_lf": "de5647982a8a835e7449c0a776bc039927e23530e9bdc1d588961500bb5af61f",
   "crlf": false,
   "bytes": 134
  },
  ".gitignore": {
   "sha256_lf": "416e67dcddbe8c7f873d514dda8bae8559764d65288640068c43983c00eb2535",
   "crlf": false,
   "bytes": 218
  },
  "AGENTS.md": {
   "sha256_lf": "fe9507d613dff8334d80a6f6ae1c24fc70b2aada4d02baf9c70a121b30231a55",
   "crlf": false,
   "bytes": 1109
  },
  "CHANGELOG.md": {
   "sha256_lf": "cc17fa2ce01954d334e55764c7cd9dbcb47d39cd27640701630279a89a9778c6",
   "crlf": false,
   "bytes": 1742
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
   "sha256_lf": "c9c6ee5418e93c1f33ce6146282f148a3586405614d3bc4a161ee340fc038fad",
   "crlf": false,
   "bytes": 2566
  },
  "START_HERE.txt": {
   "sha256_lf": "d4840467fef66d01f6985d587a82a5b00007ea0b2fde0ec01ef4b91fcc0cbfc2",
   "crlf": true,
   "bytes": 1732
  },
  "VERO_CONTEXT.md": {
   "sha256_lf": "ab219a39bfbef8fdb9b5803f09e4c3fb2e7521c443bdb32dabfa651fe18e1962",
   "crlf": false,
   "bytes": 19520
  },
  "config/monitor.example.json": {
   "sha256_lf": "3da8d546ccc8f200d1f72a9c47fbd2a0f38f5c56b6faba7161a6bf25a1673fa8",
   "crlf": false,
   "bytes": 531
  },
  "docs/ARCHITECTURE.md": {
   "sha256_lf": "94de02081ddc31707ca49571350e8642fbe2eb4f13210eb61eee8afc88d6bf5f",
   "crlf": false,
   "bytes": 1655
  },
  "docs/DESIGN_SYSTEM.md": {
   "sha256_lf": "8877714e9d2a498f8a2848be56bd28d9e5432df063498adb5168c08c25ca29b4",
   "crlf": false,
   "bytes": 737
  },
  "docs/PRD.md": {
   "sha256_lf": "e25beba6eb3b42fd4a5c5b8bb40f42098ebd5a99c4a84c36b0fcebd72e914f18",
   "crlf": false,
   "bytes": 1520
  },
  "docs/decisions/ADR-001_stdlib-only.md": {
   "sha256_lf": "dd1b3761a9e13cb31ffd57e8446a01e2b5bcd69ac92068059810f2d4848342f8",
   "crlf": false,
   "bytes": 567
  },
  "make_report.bat": {
   "sha256_lf": "b4948903d8df357a7bdfb4b5c0932b71cbace69e6315d6d1e1461e9d805f944e",
   "crlf": true,
   "bytes": 328
  },
  "pyproject.toml": {
   "sha256_lf": "46ba6fd1772920433f7a2c748c35596b9b75ce439649a57260e404b9567aff3d",
   "crlf": false,
   "bytes": 410
  },
  "requirements.txt": {
   "sha256_lf": "7d1cbdb0672e2583fb06e0f1f89042b6a7bae2621786f0bf75b863179d6a8839",
   "crlf": false,
   "bytes": 110
  },
  "run_probe_now.bat": {
   "sha256_lf": "712230cb7ef6bd562cbe28a2e83bda944298892ac0e5b96a43d2af344ec8a68f",
   "crlf": true,
   "bytes": 156
  },
  "scripts/_py.bat": {
   "sha256_lf": "ee03008dcfe04647b013bb12a8f75bfaabc1c2ebbce3395986b8829ffdd9cc96",
   "crlf": true,
   "bytes": 580
  },
  "scripts/build_installer.py": {
   "sha256_lf": "8bd7751d0c093b5a07492b34d02ef72fff8a51e164d8d2ead86b6e7439645a30",
   "crlf": false,
   "bytes": 3501
  },
  "scripts/build_rebuild_md.py": {
   "sha256_lf": "46d59fd833a57471fae31277065b55f9b96c1b87cb2707ae3fdb03859d76e4c7",
   "crlf": false,
   "bytes": 6308
  },
  "scripts/build_zip.py": {
   "sha256_lf": "10dba058802fa29c78249cfef8fca32f4cb98720805d4771c398ef6a63514c1b",
   "crlf": false,
   "bytes": 1031
  },
  "scripts/fake_vero.py": {
   "sha256_lf": "abe86f859e2c169757cf0d301bd702aa6a555b7a528f0771d2985a60de700c41",
   "crlf": false,
   "bytes": 1055
  },
  "scripts/seed_demo_data.py": {
   "sha256_lf": "9ba19baee3e2aceea6784bbfe97b9e376ae2d26622fe36e1c77ddc8722dc4beb",
   "crlf": false,
   "bytes": 2598
  },
  "setup.bat": {
   "sha256_lf": "1dffffc96cc36da35578b948f99ebce33f98a01904e14f12383dd37586ebc90a",
   "crlf": true,
   "bytes": 1032
  },
  "setup_demo.bat": {
   "sha256_lf": "3d97a5149f25f325d2691f9a9d818b98ac95aff21bfa0dbd08ad54d08d80971b",
   "crlf": true,
   "bytes": 521
  },
  "src/vero_latency/__init__.py": {
   "sha256_lf": "e13d2e358f1452e19492ff42c06ef9edaf7b63aca0c253529201406b6ee7ff03",
   "crlf": false,
   "bytes": 94
  },
  "src/vero_latency/__main__.py": {
   "sha256_lf": "13a1a5b340cdcfc1902b62be90e508c7c71886000d5bf087e7854aadf09fb35e",
   "crlf": false,
   "bytes": 52
  },
  "src/vero_latency/cli.py": {
   "sha256_lf": "c2e6528228831697d292bef2c458d54f3c3a659f52275a1b5bacb364516d95b4",
   "crlf": false,
   "bytes": 13714
  },
  "src/vero_latency/config.py": {
   "sha256_lf": "9a9e23f6f10b102f3b3e4ae4c74509b5cd6b14f39517f8c7657d90a2efb6af1d",
   "crlf": false,
   "bytes": 5078
  },
  "src/vero_latency/probe.py": {
   "sha256_lf": "a7a9992aec478991c031b9ae2417dc27705c3fae5f1f307506226e7c6cde797a",
   "crlf": false,
   "bytes": 10214
  },
  "src/vero_latency/scheduler.py": {
   "sha256_lf": "64ac03085dba2d4ff8c01f8611a62017872109fec61d32de14a04206ed719654",
   "crlf": false,
   "bytes": 10813
  },
  "src/vero_latency/server.py": {
   "sha256_lf": "eea3f864378c5acd2d56e18f3a25260f0c12955dcfa6bb389ca497db5ba9b265",
   "crlf": false,
   "bytes": 9595
  },
  "src/vero_latency/stats.py": {
   "sha256_lf": "084ebd913cb29e25739e187c41e7432b5856c22931fb55e1e5c798765948b6cd",
   "crlf": false,
   "bytes": 2902
  },
  "src/vero_latency/store.py": {
   "sha256_lf": "84da7e7712698362c1e8faeda0a444b2fe7219ff5166135ff1f1355443dba2c5",
   "crlf": false,
   "bytes": 4736
  },
  "src/vero_latency/web/dashboard.html": {
   "sha256_lf": "35d3753a015a508d7506cc2b982f7e3006ad7490aa16f2abd50b51094534eecc",
   "crlf": false,
   "bytes": 24962
  },
  "start_dashboard.bat": {
   "sha256_lf": "a0ef7a00d2e9d9040eb727f31a84826a8ce3bf0169a16d8aa69660c823a5f25d",
   "crlf": true,
   "bytes": 204
  },
  "status.bat": {
   "sha256_lf": "ea4c52c488de2e5d07fb2b013fd62b416d03891d0f4335b385d4091c2c4e6505",
   "crlf": true,
   "bytes": 170
  },
  "tests/__init__.py": {
   "sha256_lf": "7e9af23c4d8769e855436c950c52874ef9d5ac0c36f24531913b3ca965d6860f",
   "crlf": false,
   "bytes": 20
  },
  "tests/conftest.py": {
   "sha256_lf": "1e4df448187414b5cbbb2484f9d48ac2103a5e048bd83da5209ee0243eb22686",
   "crlf": false,
   "bytes": 701
  },
  "tests/fixtures/.gitkeep": {
   "sha256_lf": "71bb90b3532c3bcf92a2a5729e984b4767f5925858cdec163808765b2ee51dad",
   "crlf": false,
   "bytes": 52
  },
  "tests/integration/__init__.py": {
   "sha256_lf": "7e9af23c4d8769e855436c950c52874ef9d5ac0c36f24531913b3ca965d6860f",
   "crlf": false,
   "bytes": 20
  },
  "tests/integration/test_cycle.py": {
   "sha256_lf": "9643f197833bee8196e3032ffd79fe9e7e8e79916e5c49a18ad3da3bc6ab513d",
   "crlf": false,
   "bytes": 6580
  },
  "tests/unit/__init__.py": {
   "sha256_lf": "7e9af23c4d8769e855436c950c52874ef9d5ac0c36f24531913b3ca965d6860f",
   "crlf": false,
   "bytes": 20
  },
  "tests/unit/test_config_scheduler.py": {
   "sha256_lf": "c899211b3e0e5031a9e774c3cd9e34878ddb8edba0b6078deaa41e2468b7cadc",
   "crlf": false,
   "bytes": 5060
  },
  "tests/unit/test_probe.py": {
   "sha256_lf": "67151bdcba1bf058cbb676107cd78c087097c344ff125c589db12966a9067dc9",
   "crlf": false,
   "bytes": 2338
  },
  "tests/unit/test_stats.py": {
   "sha256_lf": "670305fcc5159ace5d41ba40d35fbe24b09d8c46e207f65aab4a690cea1f24a3",
   "crlf": false,
   "bytes": 1774
  },
  "uninstall.bat": {
   "sha256_lf": "adabbc2092e350484ce5a0bea099d2404579d3d778d0ab1f5f4b80e891e27958",
   "crlf": true,
   "bytes": 222
  },
  "vlm.py": {
   "sha256_lf": "624649a3a849991833bcd3545da3ba07627bc9ddc039f6bb08a2a3f2f2ccee32",
   "crlf": false,
   "bytes": 286
  }
 }
}
-->
