# Fix PowerShell Execution Policy Error

## 🐛 Error You're Seeing

```
railway.ps1 cannot be loaded
The file is not digitally signed
You cannot run this script on the current system
```

## ✅ Solution

This is a PowerShell security setting. Here's how to fix it:

### Option 1: Change Execution Policy (Recommended)

Run this command in PowerShell (as Administrator if needed):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**What this does:**
- Allows locally created scripts to run
- Still requires downloaded scripts to be signed
- Only affects your user account (safe)

### Option 2: Bypass for Current Session Only

If you don't want to change the policy permanently:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

**What this does:**
- Only affects the current PowerShell window
- Resets when you close the terminal
- Good for one-time use

### Option 3: Run in Command Prompt Instead

If PowerShell keeps blocking, use Command Prompt (cmd):

1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to your folder:
   ```bash
   cd C:\Users\sgc59\OneDrive\Desktop\earning-app\earning-app\backend
   ```
4. Run Railway commands:
   ```bash
   railway login
   railway link
   ```

---

## 🔍 Verify It's Fixed

After changing the policy, test:

```powershell
railway --version
```

Should show: `railway 4.15.0` (or similar)

---

## 📋 Step-by-Step Fix

1. **Open PowerShell as Administrator:**
   - Right-click Start button
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Run the fix command:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Type `Y` when prompted** to confirm

4. **Close and reopen VS Code terminal**

5. **Try Railway command again:**
   ```powershell
   railway login
   ```

---

## 🎯 Alternative: Use Command Prompt

If you prefer not to change PowerShell settings:

1. In VS Code, click the dropdown next to the `+` in terminal
2. Select "Command Prompt" instead of "PowerShell"
3. Run Railway commands normally

---

## ✅ After Fixing

Once the execution policy is fixed, you can:

1. Login: `railway login`
2. Link: `railway link`
3. Run commands: `.\run_after_login.bat`

---

**The fix is simple - just run the Set-ExecutionPolicy command!** 🚀

