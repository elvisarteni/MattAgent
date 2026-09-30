@echo off
rem Runs one probe cycle now and prints the run manifest.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py probe
pause
