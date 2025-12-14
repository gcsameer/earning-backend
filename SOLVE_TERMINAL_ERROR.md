# Solve Terminal Error - Complete Solution

## 🐛 The Error

PowerShell is blocking Railway CLI with:
```
railway.ps1 cannot be loaded
The file is not digitally signed
You cannot run this script on the current system
```

## ✅ Solution 1: Use Command Prompt (EASIEST - Recommended)

### Step 1: Switch Terminal in VS Code
1. In VS Code, look at the terminal panel (bottom)
2. Click the **dropdown arrow** (▼) next to the `+` button
3. Select **"Command Prompt"** or **"cmd"**
4. Terminal restarts in Command Prompt mode

### Step 2: Navigate and Run
```bash
cd earning-app\backend
railway login
railway link
railway run python manage.py remove_video_tasks
railway run python manage.py force_create_tasks
railway run python manage.py verify_tasks
```

**✅ Done! Command Prompt has no execution policy restrictions.**

---

## ✅ Solution 2: Fix PowerShell Execution Policy

### Option A: Quick Fix (Current Session Only)

In PowerShell terminal, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Then try Railway commands again.

### Option B: Permanent Fix (Current User)

1. Open PowerShell **as Administrator**:
   - Press `Win + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. Run this command:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Type `Y` when prompted

4. Close and reopen VS Code terminal

5. Railway commands should work now!

---

## ✅ Solution 3: Use the Fix Script

I've created a script for you. Run this in PowerShell:

```powershell
cd earning-app\backend
.\fix_terminal.ps1
```

---

## 🎯 Recommended: Use Command Prompt

**Why Command Prompt is better:**
- ✅ No execution policy issues
- ✅ Works immediately
- ✅ Same commands, no differences
- ✅ No security prompts

**How to switch:**
1. VS Code terminal → Click dropdown (▼)
2. Select "Command Prompt"
3. Done!

---

## 📋 Complete Command List (After Fix)

Once terminal is working, run these:

```bash
# 1. Login (one-time setup)
railway login

# 2. Link project (one-time setup)
railway link

# 3. Remove video tasks
railway run python manage.py remove_video_tasks

# 4. Create game tasks
railway run python manage.py force_create_tasks

# 5. Verify tasks
railway run python manage.py verify_tasks
```

---

## ✅ Verification

Test if it's working:
```bash
railway --version
```

Should show: `railway 4.15.0` (or similar version)

If you see the version number, **it's working!** ✅

---

## 🚀 Quick Start (After Fix)

1. **Switch to Command Prompt** in VS Code
2. **Navigate:** `cd earning-app\backend`
3. **Run:** `railway login` (browser opens)
4. **Run:** `railway link` (select project)
5. **Run:** `.\run_after_login.bat` (runs all commands)

---

## 📝 Summary

**Easiest Solution:** Switch VS Code terminal to Command Prompt - no errors, works immediately!

**Alternative:** Fix PowerShell execution policy if you prefer PowerShell.

---

**The terminal error is solved! Just switch to Command Prompt!** 🎉

