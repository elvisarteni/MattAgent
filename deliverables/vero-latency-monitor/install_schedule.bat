@echo off
rem Creates the Windows Task Scheduler task "VeroLatencyMonitor" (interval from config).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py schedule install %*
%PY% vlm.py schedule status
pause
