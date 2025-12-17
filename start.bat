@echo off
setlocal
title NeuroGuard Launcher
color 0A
cd /d "%~dp0"

echo ========================================================
echo   NeuroGuard IDS/IPS - Sistem Baslatiliyor...
echo   Calisma Dizini: %CD%
echo ========================================================
echo.

:: --- 1. YONETICI IZNI KONTROLU ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [UYARI] Yonetici izinleri gerekiyor...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

:: --- 2. PYTHON NEREDE? (Dedektif Modu) ---
:: Once standart 'python' komutunu dene
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :FOUND
)

:: Olmadiysa Windows Launcher 'py' komutunu dene
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :FOUND
)

:: O da olmadiysa 'python3' komutunu dene
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :FOUND
)

:: HICBIRI YOKSA HATA VER
echo [HATA] Python hicbir sekilde bulunamadi!
echo Lutfen Python'u tekrar kurun ve "Add to PATH" secenegini isaretleyin.
pause
exit

:FOUND
echo [OK] Python bulundu! Komut: %PYTHON_CMD%

:: --- 3. SANAL ORTAM (VENV) KURULUMU ---
if not exist "venv" (
    echo [BILGI] Sanal ortam kuruluyor...
    %PYTHON_CMD% -m venv venv
    
    echo [BILGI] Kutuphaneler yukleniyor...
    call venv\Scripts\activate
    
    %PYTHON_CMD% -m pip install --upgrade pip
    if exist "requirements.txt" (
        pip install -r requirements.txt
    )
    echo [OK] Hazir!
    timeout /t 2 >nul
) else (
    echo [OK] Sanal ortam aktif ediliyor...
    call venv\Scripts\activate
)

:: --- 4. NPCAP KONTROLU ---
if not exist "%SystemRoot%\System32\Npcap\wpcap.dll" (
    echo [UYARI] Npcap bulunamadi. Hata alirsaniz https://npcap.com kurun.
    timeout /t 2
)

:: --- 5. BASLAT ---
echo.
echo [BILGI] Menu Aciliyor...
%PYTHON_CMD% main.py

pause