@echo off
REM Script to set up tasks after deployment on Windows
REM Run this after migrations are complete

echo Setting up game tasks...
python manage.py create_game_tasks

echo ✅ Tasks setup complete!

