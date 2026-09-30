@echo off
rem Starts the live dashboard on http://127.0.0.1:8765 . Keep this window open.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py serve --open
pause
