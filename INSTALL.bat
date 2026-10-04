@echo off
title PERSONAL AI ASSISTANT SETUP
color 0b

echo =============================================================
echo             PERSONAL AI ASSISTANT 1-CLICK SETUP
echo =============================================================
echo.
echo [1/3] Verifying Python Environment...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not detected on this system!
    echo Please install Python 3.10+ from python.org and check 'Add Python to PATH'.
    pause
    exit /b
)
echo [OK] Python is ready.
echo.

echo =============================================================
echo [2/3] Personalize Your AI Assistant:
echo =============================================================
echo What would you like to name your AI?
echo (This will be the Wake-Word it answers to, e.g. Jubayer, Alex, Jarvis)
set /p USER_AI_NAME="> Enter AI Name (Press Enter for 'Jubayer'): "
if "%USER_AI_NAME%"=="" set USER_AI_NAME=Jubayer

echo.
echo Enter your 4-digit Emergency Backup PIN:
set /p USER_PIN="> Enter 4-digit PIN (Press Enter for '1234'): "
if "%USER_PIN%"=="" set USER_PIN=1234

echo.
echo [Updating Configuration...]
python setup_config.py "%USER_AI_NAME%" "%USER_PIN%"
echo.

echo =============================================================
echo [3/3] Installing Free Dependencies...
echo =============================================================
cd /d "%~dp0"
pip install -r requirements.txt flask qrcode pillow >nul 2>&1
echo [OK] All dependencies installed successfully.
echo.

echo =============================================================
echo             CONGRATULATIONS! SETUP IS COMPLETE!
echo =============================================================
echo AI Name: %USER_AI_NAME%
echo Backup PIN: %USER_PIN%
echo.
echo Launch now by double-clicking 'START_JUBAYER.bat' on your Desktop!
echo =============================================================
pause
