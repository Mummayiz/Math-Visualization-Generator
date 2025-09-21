@echo off
echo 🔄 Starting Educational Math Video Generator...
echo.

REM Kill any existing Python processes
taskkill /f /im python.exe >nul 2>&1

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start the app
echo 🚀 Starting app...
python app_educational_video.py

pause
