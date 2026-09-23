@echo off
REM One-time setup for Windows: creates .venv, installs packages, creates .env
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")

if not exist .venv\Scripts\python.exe (
    echo Creating virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 goto :error
)

echo Installing packages...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error

if not exist .env (
    echo Creating .env with a random SECRET_KEY...
    copy .env.example .env >nul
    .venv\Scripts\python.exe -c "import secrets, pathlib; p = pathlib.Path('.env'); p.write_text(p.read_text().replace('change-me-to-a-long-random-string', secrets.token_hex(32)))"
)

echo.
echo Setup complete!
echo   Add demo data:  .venv\Scripts\python.exe seed.py
echo   Start the API:  run.bat
pause
exit /b 0

:error
echo.
echo Setup failed. Make sure Python 3.9+ is installed from https://www.python.org/downloads/
echo and that "Add python.exe to PATH" was ticked during installation.
pause
exit /b 1
