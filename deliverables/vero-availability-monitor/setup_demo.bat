@echo off
rem Demo: fake Vero CLI + 7 days of sample data in data-demo\ (separate from real data).
setlocal
cd /d "%~dp0"
call scripts\_py.bat || exit /b 1
%PY% vam.py init --demo --force || goto end
%PY% scripts\seed_demo_data.py || goto end
echo.
echo  Demo ready. The status page opens now; close this window to stop it.
%PY% vam.py serve --open
:end
pause
