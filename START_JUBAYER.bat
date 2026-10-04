@echo off
chcp 65001 > nul
title JUBAYER AI // AUTONOMOUS OPERATOR
color 0b

echo =============================================================
echo             JUBAYER AI // AUTONOMOUS OPERATOR
echo         (100%% Free Open-Source Arc Reactor Edition)
echo =============================================================
echo.
echo Launching Jubayer AI Assistant...
echo The Cyber Arc Reactor Orb will appear floating on your screen.
echo.
cd /d "%~dp0"
python RUN_JARVIS_HUD.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application encountered an issue. Press any key to exit.
    pause > nul
)
