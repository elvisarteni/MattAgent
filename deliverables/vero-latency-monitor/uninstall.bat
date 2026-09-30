@echo off
rem Removes the scheduled tasks and the desktop shortcut. Data and config stay; delete the folder to remove everything.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py uninstall
pause
