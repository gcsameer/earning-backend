#!/bin/bash
# Script to fix tasks issue - run on Railway or locally
# Usage: railway run bash fix_tasks.sh

echo "=========================================="
echo "FIXING TASKS - DIAGNOSTIC AND CREATION"
echo "=========================================="
echo ""

# Step 1: Run migrations
echo "Step 1: Running migrations..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "❌ Migration failed!"
    exit 1
fi
echo "✅ Migrations completed"
echo ""

# Step 2: Verify current tasks
echo "Step 2: Checking existing tasks..."
python manage.py verify_tasks
echo ""

# Step 3: Create tasks
echo "Step 3: Creating/updating game tasks..."
python manage.py create_game_tasks
if [ $? -ne 0 ]; then
    echo "❌ Task creation failed!"
    exit 1
fi
echo ""

# Step 4: Verify tasks were created
echo "Step 4: Verifying tasks..."
python manage.py verify_tasks
echo ""

# Step 5: Test API endpoint (if possible)
echo "Step 5: Task creation complete!"
echo ""
echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="
echo "1. Check Railway logs for any errors"
echo "2. Test API: curl -H 'Authorization: Bearer TOKEN' https://your-backend.railway.app/api/tasks/"
echo "3. Verify frontend can fetch tasks"
echo "=========================================="

