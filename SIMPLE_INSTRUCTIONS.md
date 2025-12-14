# Simple Instructions - Run Commands in VS Code

## 🎯 Easiest Way

### Option 1: Use the Batch File (Double-Click)
1. In VS Code, navigate to `earning-app/backend` folder
2. Find `run_commands.bat` file
3. Right-click → "Run in Terminal"
4. Done! All commands run automatically

### Option 2: Copy Commands from Text File
1. Open `commands.txt` in VS Code
2. Copy each command
3. Paste into VS Code terminal (Ctrl + `)
4. Press Enter after each command

### Option 3: Type Commands Manually

Open VS Code terminal (Ctrl + `) and type:

**Command 1:**
```
railway run python manage.py remove_video_tasks
```

**Command 2:**
```
railway run python manage.py force_create_tasks
```

**Command 3:**
```
railway run python manage.py verify_tasks
```

---

## 📋 What Each Command Does

1. **remove_video_tasks** - Removes video ad tasks
2. **force_create_tasks** - Creates Scratch Card (10-80 coins) and Spin Wheel (10-50 coins)
3. **verify_tasks** - Shows all tasks to confirm they're created

---

## ✅ Expected Result

After running all 3 commands, you should see:
- ✅ Video tasks removed
- ✅ 4 game tasks created
- ✅ All tasks verified and active

---

## 🐛 If You Get Errors

### "railway: command not found"
Run: `npm install -g @railway/cli`

### "Unauthorized"
Run: `railway login` first

### "No project linked"
Run: `railway link` first

---

**That's it!** Just run the 3 commands in VS Code terminal! 🎉

