@echo off
rem Removes the scheduled tasks and the desktop shortcut. Data and config stay.
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py uninstall
pause
