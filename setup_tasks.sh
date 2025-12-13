#!/bin/bash
# Script to set up tasks after deployment
# Run this after migrations are complete

echo "Setting up game tasks..."
python manage.py create_game_tasks

echo "✅ Tasks setup complete!"

