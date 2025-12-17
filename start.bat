@echo off
setlocal
title NeuroGuard Launcher
color 0A

:: --- CRITICAL FIX ---
:: Force execution in the script's directory (Fixes System32 issues)
cd /d "%~dp0"

echo ========================================================
echo   NeuroGuard IDS/IPS - System Initializing...
echo   Working Directory: %CD%
echo ========================================================
echo.

:: --- 1. ADMIN PRIVILEGES CHECK ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Administrator privileges required...
    echo Requesting elevation...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

:: --- 2. PYTHON DETECTION (Detective Mode) ---
:: Try standard 'python' command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :FOUND
)

:: Try Windows Launcher 'py' command
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :FOUND
)

:: Try 'python3' command
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :FOUND
)

:: IF NOT FOUND
echo [ERROR] Python not found in PATH!
echo Please reinstall Python and check "Add to PATH" option.
pause
exit

:FOUND
echo [OK] Python found! Command: %PYTHON_CMD%

:: --- 3. VIRTUAL ENVIRONMENT (VENV) SETUP ---
if not exist "venv" (
    echo [INFO] Creating virtual environment (first run)...
    %PYTHON_CMD% -m venv venv
    
    echo [INFO] Installing dependencies...
    call venv\Scripts\activate
    
    %PYTHON_CMD% -m pip install --upgrade pip
    if exist "requirements.txt" (
        pip install -r requirements.txt
    )
    echo [OK] Setup complete!
    timeout /t 2 >nul
) else (
    echo [OK] Activating virtual environment...
    call venv\Scripts\activate
)

:: --- 4. NPCAP CHECK ---
if not exist "%SystemRoot%\System32\Npcap\wpcap.dll" (
    echo [WARNING] Npcap driver not found! Scapy might fail.
    echo If you see errors, please install Npcap from https://npcap.com
    timeout /t 3
)

:: --- 5. LAUNCH ---
echo.
echo [INFO] Launching NeuroGuard Menu...
%PYTHON_CMD% main.py

pause