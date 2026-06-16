@echo off
REM Solar Sentinel AI - Windows Setup Script
REM Installs dependencies and prepares the application

echo.
echo ======================================
echo  Solar Sentinel AI - Setup
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python version check... OK
python --version

echo.
echo [2/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [4/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ======================================
echo  ✓ Setup Complete!
echo ======================================
echo.
echo To start the application, run:
echo   streamlit run app.py
echo.
echo The app will open at: http://localhost:8501
echo.
pause
