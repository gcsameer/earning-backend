# Running Railway Commands in VS Code

## 🎯 Quick Steps

### Step 1: Open VS Code Terminal
1. Open VS Code
2. Open the folder: `earning-app/backend`
3. Press `` Ctrl + ` `` (backtick) to open terminal
4. Or: Menu → Terminal → New Terminal

### Step 2: Check Railway CLI
```bash
railway --version
```

If not installed:
```bash
npm install -g @railway/cli
```

### Step 3: Login to Railway (First Time Only)
```bash
railway login
```
This opens a browser - complete the login.

### Step 4: Link to Your Project (First Time Only)
```bash
railway link
```
Select your backend project when prompted.

### Step 5: Run the Commands

Run these commands **one by one** in the VS Code terminal:

#### Command 1: Remove Video Tasks
```bash
railway run python manage.py remove_video_tasks
```

**Expected Output:**
```
✅ Deactivated X video task(s)
```

#### Command 2: Create Game Tasks
```bash
railway run python manage.py force_create_tasks
```

**Expected Output:**
```
Deleted X existing game tasks
✅ Created: Scratch Card - Win Coins! (type: scratch_card)
✅ Created: Spin the Wheel (type: spin_wheel)
✅ Created: Math Puzzle (type: puzzle)
✅ Created: Quick Quiz (type: quiz)

✅ Created 4 game tasks!
```

#### Command 3: Verify Tasks
```bash
railway run python manage.py verify_tasks
```

**Expected Output:**
```
📊 Task Statistics:
   Total tasks in database: 4
   Active tasks: 4

✅ Active Tasks Found:
   - Scratch Card - Win Coins! (scratch_card)
   - Spin the Wheel (spin_wheel)
   - Math Puzzle (puzzle)
   - Quick Quiz (quiz)
```

---

## 📋 Complete Command List (Copy-Paste Ready)

Copy and paste these commands one by one into VS Code terminal:

```bash
# Step 1: Remove video tasks
railway run python manage.py remove_video_tasks

# Step 2: Create game tasks with new coin ranges
railway run python manage.py force_create_tasks

# Step 3: Verify tasks were created
railway run python manage.py verify_tasks
```

---

## 🖼️ VS Code Terminal Setup

### Opening Terminal:
1. **Keyboard Shortcut:** `` Ctrl + ` ``
2. **Menu:** Terminal → New Terminal
3. **Right-click folder:** Open in Integrated Terminal

### Terminal Location:
Make sure you're in: `earning-app/backend`

You can check with:
```bash
pwd
# Should show: .../earning-app/backend
```

If not, navigate:
```bash
cd earning-app/backend
```

---

## ✅ Verification Checklist

After running all commands:

- [ ] Command 1 completed: Video tasks deactivated
- [ ] Command 2 completed: 4 game tasks created
- [ ] Command 3 completed: All tasks verified
- [ ] No error messages in terminal
- [ ] All tasks show correct coin ranges

---

## 🐛 Troubleshooting

### Error: "railway: command not found"
**Fix:** Install Railway CLI
```bash
npm install -g @railway/cli
```

### Error: "Unauthorized. Please login"
**Fix:** Login first
```bash
railway login
```

### Error: "No project linked"
**Fix:** Link to project
```bash
railway link
```

### Error: "python: command not found"
**Fix:** Railway should have Python. Check your deployment logs.

---

## 🎯 Quick Copy-Paste

Just copy these 3 commands and run them one by one:

```bash
railway run python manage.py remove_video_tasks
railway run python manage.py force_create_tasks
railway run python manage.py verify_tasks
```

---

**That's it!** Run these in VS Code terminal and you're done! 🎉

