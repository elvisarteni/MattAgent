@echo off
rem Shows configuration, last run, dashboard and Task Scheduler state.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py status
pause
