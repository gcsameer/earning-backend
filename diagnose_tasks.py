#!/usr/bin/env python
"""
Diagnostic script to check tasks in the database.
Run this locally: python diagnose_tasks.py
Or on Railway: railway run python diagnose_tasks.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'earning_backend.settings')
django.setup()

from core.models import Task, User

def diagnose():
    print("\n" + "="*60)
    print("TASK DIAGNOSTIC REPORT")
    print("="*60 + "\n")
    
    # Check tasks
    all_tasks = Task.objects.all()
    active_tasks = Task.objects.filter(is_active=True)
    
    print(f"📊 Task Statistics:")
    print(f"   Total tasks in database: {all_tasks.count()}")
    print(f"   Active tasks: {active_tasks.count()}\n")
    
    if active_tasks.count() == 0:
        print("❌ PROBLEM: No active tasks found!")
        print("\n🔧 Solution:")
        print("   Run: python manage.py create_game_tasks")
        print("   Or: railway run python manage.py create_game_tasks\n")
    else:
        print("✅ Active Tasks Found:")
        for task in active_tasks:
            print(f"   - ID: {task.id}")
            print(f"     Title: {task.title}")
            print(f"     Type: {task.type}")
            print(f"     Reward: {task.reward_coins} coins")
            print(f"     Active: {task.is_active}")
            print()
    
    # Check users
    user_count = User.objects.count()
    print(f"👥 Users in database: {user_count}")
    
    if user_count == 0:
        print("   ⚠️  No users found - you may need to register first")
    
    print("\n" + "="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60 + "\n")
    
    # Return status code
    return 0 if active_tasks.count() > 0 else 1

if __name__ == "__main__":
    try:
        exit_code = diagnose()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

