# Quick Start - Run Commands Now

## ⚡ Fastest Way (3 Steps)

### Step 1: Authenticate (One-Time Setup)
Open VS Code terminal (`Ctrl + ``) and run:
```bash
railway login
railway link
```

### Step 2: Run the Script
```bash
.\run_after_login.bat
```

### Step 3: Done!
All commands will run automatically!

---

## 📋 Manual Method (If Script Doesn't Work)

Copy and paste these 3 commands one by one in VS Code terminal:

```bash
railway run python manage.py remove_video_tasks
```

```bash
railway run python manage.py force_create_tasks
```

```bash
railway run python manage.py verify_tasks
```

---

## ✅ What Happens

1. **remove_video_tasks** → Removes video ad tasks
2. **force_create_tasks** → Creates:
   - Scratch Card (10-80 coins)
   - Spin Wheel (10-50 coins)
   - Puzzle (5-20 coins)
   - Quiz (5-20 coins)
3. **verify_tasks** → Shows all created tasks

---

## 🎯 Expected Result

After running, you'll see:
- ✅ Video tasks removed
- ✅ 4 game tasks created
- ✅ All tasks verified

Then redeploy your frontend and check the `/tasks` page!

---

**That's it!** Just authenticate once, then run the script! 🚀

