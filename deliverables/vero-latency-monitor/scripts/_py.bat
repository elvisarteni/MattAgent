@echo off
rem Finds Python 3.8+ and sets PY. Called by the other .bat files.
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY goto nopy
%PY% -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul || goto nopy
exit /b 0
:nopy
echo.
echo  Python 3.8 or newer was not found.
echo  Install it from Software Center, or python.org (tick "Add python.exe to PATH"),
echo  or run:  winget install Python.Python.3.12
echo  Then run this file again.
echo.
pause
exit /b 1
