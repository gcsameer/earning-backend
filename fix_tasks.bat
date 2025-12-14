@echo off
REM Script to fix tasks issue - run on Railway or locally
REM Usage: railway run fix_tasks.bat

echo ==========================================
echo FIXING TASKS - DIAGNOSTIC AND CREATION
echo ==========================================
echo.

REM Step 1: Run migrations
echo Step 1: Running migrations...
python manage.py migrate --noinput
if errorlevel 1 (
    echo Migration failed!
    exit /b 1
)
echo Migrations completed
echo.

REM Step 2: Verify current tasks
echo Step 2: Checking existing tasks...
python manage.py verify_tasks
echo.

REM Step 3: Create tasks
echo Step 3: Creating/updating game tasks...
python manage.py create_game_tasks
if errorlevel 1 (
    echo Task creation failed!
    exit /b 1
)
echo.

REM Step 4: Verify tasks were created
echo Step 4: Verifying tasks...
python manage.py verify_tasks
echo.

echo ==========================================
echo TASK CREATION COMPLETE!
echo ==========================================
echo.
echo NEXT STEPS:
echo 1. Check Railway logs for any errors
echo 2. Test API endpoint
echo 3. Verify frontend can fetch tasks
echo ==========================================

