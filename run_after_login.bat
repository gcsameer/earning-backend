@echo off
echo ========================================
echo Railway Commands Runner
echo ========================================
echo.

echo Checking authentication...
railway whoami >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Not authenticated!
    echo.
    echo Please run these commands first:
    echo   1. railway login
    echo   2. railway link
    echo.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo Authenticated! Running commands...
echo.

echo [1/3] Removing video tasks...
railway run python manage.py remove_video_tasks
if errorlevel 1 (
    echo ERROR: Failed to remove video tasks
    pause
    exit /b 1
)
echo Done!
echo.

echo [2/3] Creating game tasks...
railway run python manage.py force_create_tasks
if errorlevel 1 (
    echo ERROR: Failed to create tasks
    pause
    exit /b 1
)
echo Done!
echo.

echo [3/3] Verifying tasks...
railway run python manage.py verify_tasks
echo Done!
echo.

echo ========================================
echo All commands completed successfully!
echo ========================================
pause

