@echo off
REM Start the API on Windows. Open http://127.0.0.1:8000/docs in your browser.
cd /d "%~dp0"

if not exist .venv\Scripts\python.exe (
    echo Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

echo Starting API... open http://127.0.0.1:8000/docs  (press CTRL+C to stop)
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
