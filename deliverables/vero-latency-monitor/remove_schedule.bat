@echo off
rem Deletes the Windows Task Scheduler task "VeroLatencyMonitor".
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py schedule remove
pause
