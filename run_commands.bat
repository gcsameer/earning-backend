@echo off
echo ========================================
echo Running Railway Commands
echo ========================================
echo.

echo Step 1: Removing video tasks...
railway run python manage.py remove_video_tasks
echo.

echo Step 2: Creating game tasks...
railway run python manage.py force_create_tasks
echo.

echo Step 3: Verifying tasks...
railway run python manage.py verify_tasks
echo.

echo ========================================
echo Done!
echo ========================================
pause

