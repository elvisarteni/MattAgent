@echo off
rem Opens the status page; starts it first if it is not running (keep this window open then).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py serve --open
pause
