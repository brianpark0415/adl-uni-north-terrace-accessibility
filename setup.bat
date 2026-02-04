@echo off
echo ===================================
echo Accessible Campus Navigation Setup
echo ===================================

REM Check Python installation
echo.
echo 1. Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found. Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo + Python found
python --version

REM Create virtual environment
echo.
echo 2. Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo + Virtual environment created
) else (
    echo + Virtual environment already exists
)

REM Activate virtual environment
echo.
echo 3. Activating virtual environment...
call venv\Scripts\activate.bat
echo + Virtual environment activated

REM Upgrade pip
echo.
echo 4. Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo 5. Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)
echo + Dependencies installed

REM Run demo
echo.
echo 6. Running demo to verify installation...
python demo.py

echo.
echo ===================================
echo Setup complete!
echo ===================================
echo.
echo To start the web server:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate
echo   2. Run: python app.py
echo   3. Open: http://localhost:5000
echo.
pause
