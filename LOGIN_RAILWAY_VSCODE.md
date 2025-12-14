# How to Login Railway in VS Code

## 🎯 Step-by-Step Guide

### Step 1: Open VS Code Terminal

**Method 1: Keyboard Shortcut**
- Press `` Ctrl + ` `` (Control + Backtick)
- The backtick key is usually above the Tab key

**Method 2: Menu**
- Click **Terminal** → **New Terminal**

**Method 3: Right-Click**
- Right-click on the `backend` folder in Explorer
- Select **"Open in Integrated Terminal"**

---

### Step 2: Navigate to Backend Folder (if needed)

If your terminal opens in a different folder, type:
```bash
cd earning-app/backend
```

Or if you're in the root:
```bash
cd earning-app\backend
```

---

### Step 3: Check Railway CLI is Installed

Type this to verify:
```bash
railway --version
```

**Expected output:** `railway 4.15.0` (or similar version number)

**If you get an error:** Install Railway CLI first:
```bash
npm install -g @railway/cli
```

---

### Step 4: Login to Railway

Type this command:
```bash
railway login
```

**What happens:**
1. Railway CLI will open your **default web browser** automatically
2. You'll see the Railway login page
3. **Login with your Railway account** (email and password)
4. Click **"Authorize"** or **"Allow"** to grant access
5. Browser will show: "Success! You can close this window"
6. VS Code terminal will show: "Logged in successfully"

**Note:** If browser doesn't open automatically, Railway will show a URL - copy it and paste in your browser.

---

### Step 5: Link to Your Project

After logging in, link to your backend project:
```bash
railway link
```

**What happens:**
1. Railway shows a list of your projects
2. Use arrow keys to navigate
3. Select your **backend project** (probably named "earning-backend" or similar)
4. Press **Enter**

**Expected output:** `Linked to project: your-project-name`

---

### Step 6: Verify You're Connected

Check your connection:
```bash
railway whoami
```

**Expected output:** Your Railway username/email

---

## ✅ You're Now Ready!

After completing these steps, you can run Railway commands:

```bash
railway run python manage.py remove_video_tasks
railway run python manage.py force_create_tasks
railway run python manage.py verify_tasks
```

Or use the batch script:
```bash
.\run_after_login.bat
```

---

## 🖼️ Visual Guide

### VS Code Terminal Location:
```
VS Code Window
  ├── File Explorer (left sidebar)
  ├── Editor (center)
  └── Terminal (bottom panel) ← Opens here
      └── Type commands here
```

### Terminal After Login:
```
PS C:\...\earning-app\backend> railway login
Opening browser...
Logged in successfully!

PS C:\...\earning-app\backend> railway link
? Select a project: (Use arrow keys)
  > earning-backend
    other-project
Linked to project: earning-backend

PS C:\...\earning-app\backend> railway whoami
your-email@example.com
```

---

## 🐛 Troubleshooting

### Problem: "railway: command not found"
**Solution:** Install Railway CLI
```bash
npm install -g @railway/cli
```

### Problem: Browser doesn't open
**Solution:** 
1. Railway will show a URL like: `https://railway.app/...`
2. Copy the URL
3. Paste it in your browser
4. Complete login there

### Problem: "Unauthorized" after login
**Solution:**
1. Make sure you completed the browser login
2. Try `railway logout` then `railway login` again
3. Make sure you clicked "Authorize" in the browser

### Problem: "No projects found" when linking
**Solution:**
1. Make sure you have a Railway account
2. Make sure you have at least one project created
3. Go to https://railway.app and create a project if needed

### Problem: Can't find the terminal
**Solution:**
- Press `` Ctrl + ` `` (backtick key)
- Or: View → Terminal
- Or: Terminal → New Terminal

---

## 📋 Quick Checklist

- [ ] Opened VS Code terminal (`` Ctrl + ` ``)
- [ ] Navigated to `earning-app/backend` folder
- [ ] Verified Railway CLI installed (`railway --version`)
- [ ] Ran `railway login` (browser opened)
- [ ] Completed login in browser
- [ ] Ran `railway link` (selected project)
- [ ] Verified with `railway whoami`
- [ ] Ready to run commands!

---

## 🎉 That's It!

Once you're logged in, you only need to do this **once**. Railway will remember your authentication for future commands.

**Next step:** Run `.\run_after_login.bat` to execute all the task update commands!

