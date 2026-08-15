@echo off
title SelfCraft Media Editor — First Time Setup
color 0A

echo.
echo  =============================================
echo   SelfCraft Media Editor — Setup
echo  =============================================
echo.
echo  This will set up everything you need.
echo  Please do not close this window.
echo.
pause

:: Check Python
echo  Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Python is not installed.
    echo  Opening the Python download page now.
    echo.
    echo  When it opens:
    echo  1. Click the big Download button
    echo  2. Run the installer
    echo  3. TICK "Add python.exe to PATH" on the first screen
    echo  4. Click Install Now
    echo  5. Come back here and press any key when done.
    echo.
    start https://python.org/downloads
    pause
)

:: Check FFmpeg
echo  Checking FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Installing FFmpeg...
    winget install ffmpeg
    echo.
    echo  FFmpeg installed.
    echo  Please close this window, reopen it, and run setup.bat again.
    echo.
    pause
    exit
)

:: Create virtual environment
echo.
echo  Setting up the application environment...
if not exist .venv (
    python -m venv .venv
)

:: Activate and install libraries
echo  Installing required libraries (this may take a few minutes)...
call .venv\Scripts\activate
pip install fastapi uvicorn openai-whisper watchdog python-multipart --quiet

:: Create media folders
echo  Creating your media folders...
set MEDIA=%USERPROFILE%\Desktop\SelfCraft Media
if not exist "%MEDIA%\Raw Videos\Recorded Classes" mkdir "%MEDIA%\Raw Videos\Recorded Classes"
if not exist "%MEDIA%\Raw Videos\Teaching Reels" mkdir "%MEDIA%\Raw Videos\Teaching Reels"
if not exist "%MEDIA%\Raw Videos\Testimonials" mkdir "%MEDIA%\Raw Videos\Testimonials"
if not exist "%MEDIA%\Edited Videos" mkdir "%MEDIA%\Edited Videos"
if not exist "%MEDIA%\Temp" mkdir "%MEDIA%\Temp"

:: Write config with correct Windows paths
echo  Configuring folder paths...
python -c "
import json, os
config_path = 'config/settings.json'
with open(config_path) as f:
    cfg = json.load(f)
base = os.path.join(os.path.expanduser('~'), 'Desktop', 'SelfCraft Media')
cfg['folders']['raw_videos'] = base + '/Raw Videos'
cfg['folders']['edited_videos'] = base + '/Edited Videos'
cfg['folders']['temp'] = base + '/Temp'
cfg['file_manager'] = 'explorer'
with open(config_path, 'w') as f:
    json.dump(cfg, f, indent=2)
print('Config updated.')
"

echo.
echo  =============================================
echo   Setup complete!
echo  =============================================
echo.
echo  Your media folders have been created on your Desktop
echo  inside a folder called "SelfCraft Media".
echo.
echo  To use the app, double-click "start.bat"
echo.
pause