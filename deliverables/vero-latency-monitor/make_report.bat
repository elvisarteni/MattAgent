@echo off
rem Writes a self-contained HTML report of the last 7 days into reports\ (can be emailed).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
if not exist reports mkdir reports
%PY% vlm.py report --hours 168 --out reports\vero_latency_report.html
start "" reports\vero_latency_report.html
