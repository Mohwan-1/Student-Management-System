@echo off
echo Starting Student Management System...
echo.

if not exist ".venv" (
    echo Virtual environment not found. Please run setup.py first.
    pause
    exit /b 1
)

.venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo Program exited with an error.
    pause
)