@echo off
title JARVIS-AETHER AI AUTOMATION SYSTEM
color 0b
echo =======================================================
echo          JARVIS-AETHER AI AUTOMATION SYSTEM
echo           (100%% Free Open-Source Edition)
echo =======================================================
echo.
echo Launching Vision, Voice, and Gesture Engines...
echo.
cd /d "%~dp0"
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application encountered an issue. Press any key to exit.
    pause > nul
)
