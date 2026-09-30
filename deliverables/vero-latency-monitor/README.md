# vero-latency-monitor

Purpose: measure how fast the Vero CLI answers. It runs the cheapest possible prompt on a timer, records every result and shows it on a live dashboard.
Owner: << OWNER >> (Quality AI Automation, GenAI Group 3)
Jira: ASPF-1578 (AES SW Process Framework)
Rules: see the SCMP (SCMP_QualityAIAutomation) and CONTRIBUTING.md.

Full guide: [docs/VeroLatencyMonitor_Guide.html](docs/VeroLatencyMonitor_Guide.html) · AI context for Vero CLI: [VERO_CONTEXT.md](VERO_CONTEXT.md)

## Install (Windows, about 5 minutes)

Needs Python 3.8+ and nothing else: no pip install, no internet, no admin rights.

1. Get the folder into e.g. `C:\Tools\vero-latency-monitor\`: `git clone`, or `py vero_latency_monitor_setup_<version>.py C:\Tools` (single-file installer, no zip needed), or unzip.
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
```
