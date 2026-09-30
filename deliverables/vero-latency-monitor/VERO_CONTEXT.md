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
│   └── build_installer.py      dist/vero_latency_monitor_setup_<version>.py (single-file installer)
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

The zip and the installer exclude `data/`, `data-demo/`, `reports/`, `dist/`, `config/monitor.json`, caches and logs.

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
