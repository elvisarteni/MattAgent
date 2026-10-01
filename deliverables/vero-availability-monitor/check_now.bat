@echo off
rem Runs all enabled checks once and stores the result.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py check
pause
