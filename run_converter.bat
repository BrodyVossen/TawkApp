@echo off
echo JSON to Excel Converter
echo =====================

:: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

:: Check if requirements are installed
echo Checking dependencies...
pip install -r requirements.txt

:: Run the application
echo Starting the converter...
python json_to_excel.py

pause 