@echo off
rem Demo with a fake Vero CLI and 7 days of sample data (kept in data-demo\, separate from real data).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vlm.py init --demo --force || goto end
%PY% scripts\seed_demo_data.py || goto end
set "FAKE_VERO_FAIL=0"
%PY% vlm.py doctor
set "FAKE_VERO_FAIL="
echo.
echo  Demo ready. The dashboard opens now; close this window to stop it.
echo  For the real setup later, run setup.bat (it leaves demo mode).
%PY% vlm.py serve --open
:end
pause
