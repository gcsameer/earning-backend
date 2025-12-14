@echo off
REM Use Command Prompt instead of PowerShell to avoid execution policy issues
echo ========================================
echo Railway Commands (Command Prompt)
echo ========================================
echo.
echo This uses Command Prompt to avoid PowerShell issues.
echo.

cd /d "%~dp0"

echo Checking Railway CLI...
railway --version
if errorlevel 1 (
    echo ERROR: Railway CLI not found!
    echo Please install: npm install -g @railway/cli
    pause
    exit /b 1
)

echo.
echo Railway CLI is working!
echo.
echo Now you can run:
echo   1. railway login
echo   2. railway link
echo   3. railway run python manage.py remove_video_tasks
echo   4. railway run python manage.py force_create_tasks
echo   5. railway run python manage.py verify_tasks
echo.
pause

