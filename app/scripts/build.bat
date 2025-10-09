@echo off
echo ========================================
echo Building Encrypt-D
echo ========================================
echo.

REM Change to project root
cd ..

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt

REM Run build script
echo.
echo Building executable...
python scripts\build.py

echo.
echo Press any key to exit...
pause >nul
