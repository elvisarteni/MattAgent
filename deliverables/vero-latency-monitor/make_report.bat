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
