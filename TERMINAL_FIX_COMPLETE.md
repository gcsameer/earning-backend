# Terminal Issue - Complete Fix Guide

## ✅ Solution: Use Command Prompt Instead

PowerShell has execution policy restrictions. **Use Command Prompt (cmd) instead** - it doesn't have these restrictions!

---

## 🎯 Quick Fix (3 Steps)

### Step 1: Switch to Command Prompt in VS Code

1. In VS Code terminal, click the **dropdown arrow** next to the `+` button
2. Select **"Command Prompt"** instead of "PowerShell"
3. Terminal will restart in Command Prompt mode

### Step 2: Navigate to Backend Folder

```bash
cd earning-app\backend
```

### Step 3: Run Railway Commands

Now Railway commands will work without execution policy errors!

```bash
railway login
railway link
railway run python manage.py remove_video_tasks
railway run python manage.py force_create_tasks
railway run python manage.py verify_tasks
```

---

## 🔧 Alternative: Fix PowerShell (If You Prefer PowerShell)

### Option A: Run Fix Script

In PowerShell, run:
```powershell
.\fix_terminal.ps1
```

### Option B: Manual Fix

Open PowerShell **as Administrator** and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then close and reopen VS Code terminal.

---

## 📋 Complete Command List (Command Prompt)

Once you're in Command Prompt, run these in order:

```bash
# 1. Login (one-time)
railway login

# 2. Link project (one-time)
railway link

# 3. Remove video tasks
railway run python manage.py remove_video_tasks

# 4. Create game tasks
railway run python manage.py force_create_tasks

# 5. Verify tasks
railway run python manage.py verify_tasks
```

---

## 🎯 Recommended: Use Command Prompt

**Why Command Prompt is better here:**
- ✅ No execution policy issues
- ✅ Railway CLI works immediately
- ✅ Simpler, no security restrictions
- ✅ Same commands work the same way

**How to switch:**
1. VS Code terminal dropdown → "Command Prompt"
2. Done! No more PowerShell errors

---

## ✅ Verification

After switching to Command Prompt, test:

```bash
railway --version
```

Should show: `railway 4.15.0` (or similar)

If it works, you're ready to run all Railway commands!

---

## 🚀 Next Steps

1. **Switch to Command Prompt** in VS Code
2. **Navigate:** `cd earning-app\backend`
3. **Login:** `railway login`
4. **Link:** `railway link`
5. **Run commands:** Use `run_after_login.bat` or run manually

---

**The easiest solution: Just use Command Prompt instead of PowerShell!** 🎉

