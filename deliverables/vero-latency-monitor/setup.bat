@echo off
rem First-time setup. Usage: setup.bat          (real Vero CLI)
rem                          setup.bat demo     (fake CLI + 7 days of sample data)
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
echo Using: %PY%
if /I "%~1"=="demo" (
  %PY% vlm.py init --demo --force
  %PY% scripts\seed_demo_data.py
  %PY% vlm.py doctor
  echo.
  echo Demo ready. Start the dashboard with start_dashboard.bat
  pause
  exit /b 0
)
if not exist config\monitor.json %PY% vlm.py init
echo.
echo Edit config\monitor.json: Vero command, cheapest model id. Notepad opens now; save and close it.
notepad config\monitor.json
%PY% vlm.py doctor
echo.
echo If RESULT says ready: run start_dashboard.bat and/or install_schedule.bat
pause
