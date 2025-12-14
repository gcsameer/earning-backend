@echo off
REM Batch script to run all Railway commands for task updates
REM Make sure you're logged in: railway login
REM Make sure you're linked: railway link

echo ========================================
echo Running Railway Commands for Task Updates
echo ========================================
echo.

REM Check if railway is available
railway --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Railway CLI not found. Please install it first:
    echo npm install -g @railway/cli
    pause
    exit /b 1
)

echo Step 1: Removing video tasks...
railway run python manage.py remove_video_tasks
if errorlevel 1 (
    echo ERROR: Failed to remove video tasks
    echo Make sure you're logged in: railway login
    echo Make sure you're linked: railway link
    pause
    exit /b 1
)
echo Video tasks removed successfully!
echo.

echo Step 2: Creating game tasks with new coin ranges...
railway run python manage.py force_create_tasks
if errorlevel 1 (
    echo ERROR: Failed to create tasks
    pause
    exit /b 1
)
echo Game tasks created successfully!
echo.

echo Step 3: Verifying tasks...
railway run python manage.py verify_tasks
echo.

echo ========================================
echo All commands completed!
echo ========================================
pause

