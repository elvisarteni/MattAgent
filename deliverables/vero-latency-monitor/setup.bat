@echo off
rem Guided first-time setup: configure -> test -> install background monitoring.
setlocal
cd /d "%~dp0"
title Vero Latency Monitor - setup
call scripts\_py.bat || exit /b 1
echo.
echo  Vero Latency Monitor setup  (Python: %PY%)
echo  ------------------------------------------------------------
:configure
%PY% vlm.py configure
if errorlevel 1 goto again
echo.
echo  Testing the Vero CLI (one call per model, nothing stored)...
%PY% vlm.py doctor
if errorlevel 1 goto again
echo.
choice /C YN /M " Install background monitoring (probe on a timer + dashboard at every logon)"
if errorlevel 2 goto manual
%PY% vlm.py install
echo.
echo  Done. The dashboard opens now and from the desktop shortcut "Vero Latency Dashboard".
%PY% vlm.py open
goto end
:manual
echo.
echo  Not installed. Use start_dashboard.bat (it also probes while its window is open).
goto end
:again
echo.
choice /C YN /M " Not ready. Run the configuration again"
if errorlevel 2 goto end
goto configure
:end
echo.
pause
