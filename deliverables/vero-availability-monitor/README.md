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
