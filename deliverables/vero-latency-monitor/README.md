# vero-latency-monitor

Purpose: measure how fast the Vero CLI answers. It runs the cheapest possible prompt on a timer, records every result and shows it on a live dashboard.
Owner: << OWNER >> (Quality AI Automation, GenAI Group 3)
Jira: ASPF-1578 (AES SW Process Framework)
Rules: see the SCMP (SCMP_QualityAIAutomation), CONTRIBUTING.md.

Full guide: [docs/VeroLatencyMonitor_Guide.html](docs/VeroLatencyMonitor_Guide.html)

## Quick start (Windows)

1. Unzip anywhere, e.g. `C:\Tools\vero-latency-monitor`. You need Python 3.8+ and nothing else: no pip install, no internet.
2. `setup.bat demo` to try it with a fake CLI, or `setup.bat` to connect the real Vero CLI.
3. `start_dashboard.bat` opens http://127.0.0.1:8765
4. Optional: `install_schedule.bat` for unattended runs through Windows Task Scheduler.

## Commands

```
python vlm.py init [--demo]            create config/monitor.json
python vlm.py doctor                   test the Vero CLI connection (nothing stored)
python vlm.py probe                    one probe cycle now
python vlm.py serve [--open]           dashboard + live stream + built-in scheduler
python vlm.py schedule install|remove|status
python vlm.py export [--hours N]       CSV
python vlm.py report [--hours N]       self-contained HTML report
```

## Tests

```
python -m unittest discover -s tests -t .
```
