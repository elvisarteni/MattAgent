@echo off
rem Guided first-time setup: configure -> test -> install background monitoring.
setlocal
cd /d "%~dp0"
title Vero availability monitor - setup
call scripts\_py.bat || exit /b 1
echo.
echo  Vero availability monitor 3  (Python: %PY%)
echo  ------------------------------------------------------------
:configure
%PY% vam.py configure
if errorlevel 1 goto again
echo.
echo  Testing Vero once (nothing stored). The task check can take about a minute...
%PY% vam.py doctor
if errorlevel 1 goto again
echo.
choice /C YN /M " Install background monitoring (check on a timer + status page at every logon)"
if errorlevel 2 goto manual
%PY% vam.py install
%PY% vam.py open
goto end
:manual
echo.
echo  Not installed. Use start_dashboard.bat (it also checks while its window is open).
goto end
:again
echo.
choice /C YN /M " Not ready. Run the configuration again"
if errorlevel 2 goto end
goto configure
:end
echo.
pause
