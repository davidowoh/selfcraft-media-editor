@echo off
title SelfCraft Media Editor
color 0A

echo.
echo  Starting SelfCraft Media Editor...
echo  Do not close this window while using the app.
echo.

cd /d "%~dp0"
call .venv\Scripts\activate

:: Open dashboard in browser after 3 seconds
start "" timeout /t 3 /nobreak >nul
start "" "%~dp0dashboard.html"

:: Start the server
uvicorn app.core.main:app