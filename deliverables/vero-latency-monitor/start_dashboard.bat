@echo off
rem Opens the dashboard; starts it first if it is not running. Keep this window open in that case.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py serve --open
pause
