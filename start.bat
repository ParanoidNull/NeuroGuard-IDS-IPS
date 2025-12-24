@echo off
setlocal
title NeuroGuard Launcher
color 0A
cls

:: --- SET WORKING DIRECTORY ---
:: Ensures the script runs from the correct folder path
cd /d "%~dp0"

echo ========================================================
echo   NeuroGuard - Environment Manager
echo ========================================================

:: --- STEP 1: DETECT PYTHON (GOTO STRATEGY) ---
:: Attempt 1: Try standard 'python' command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo [INFO] Detected Standard Python.
    goto :CheckVenv
)

:: Attempt 2: Try 'py' launcher (common on Windows)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo [INFO] Detected Python Launcher.
    goto :CheckVenv
)

:: If both fail, display error and stop
color 0C
echo [ERROR] Python could not be found!
echo Please install Python 3.10+ and ensure "Add to PATH" is selected.
pause
exit /b

:CheckVenv
:: --- STEP 2: VIRTUAL ENVIRONMENT CHECK ---
:: If venv exists, skip installation and jump to launch
if exist "venv\Scripts\activate.bat" goto :LaunchSystem

echo [INFO] Virtual environment not found. Initializing setup...
echo [STEP 1/2] Creating virtual environment...
"%PYTHON_CMD%" -m venv venv

:: Verify if venv was created successfully
if not exist "venv\Scripts\activate.bat" (
    color 0C
    echo [ERROR] Failed to create venv.
    pause
    exit /b
)

echo [STEP 2/2] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo [SUCCESS] Installation complete.
timeout /t 2 >nul
cls

:LaunchSystem
:: --- STEP 3: SYSTEM LAUNCH ---
:: Activate the environment
if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat

echo [INFO] Starting NeuroGuard...
echo.
"%PYTHON_CMD%" main.py

:: --- STEP 4: EXIT HANDLING ---
echo.
echo [INFO] Process terminated.
pause