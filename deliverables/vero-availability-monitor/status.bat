@echo off
rem Configuration, last result, status page and Task Scheduler state.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py status
pause
