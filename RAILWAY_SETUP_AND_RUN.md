# Railway Commands Setup and Execution

## 🚀 Quick Start

### Step 1: Install Railway CLI (if not already installed)
```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway
```bash
railway login
```
This will open a browser for authentication.

### Step 3: Link to Your Project
Navigate to your backend directory and link:
```bash
cd earning-app/backend
railway link
```
Select your Railway project when prompted.

### Step 4: Run the Commands

**Option A: Use the Batch Script (Windows)**
```bash
cd earning-app/backend
run_railway_commands.bat
```

**Option B: Use the PowerShell Script**
```powershell
cd earning-app/backend
.\run_all_railway_commands.ps1
```

**Option C: Run Commands Manually**
```bash
# Step 1: Remove video tasks
railway run python manage.py remove_video_tasks

# Step 2: Create game tasks with new coin ranges
railway run python manage.py force_create_tasks

# Step 3: Verify tasks
railway run python manage.py verify_tasks
```

## 📋 What Each Command Does

### 1. `remove_video_tasks`
- Deactivates all video tasks in the database
- Makes them invisible on the frontend
- Does NOT delete them (can be restored if needed)

### 2. `force_create_tasks`
- Deletes existing game tasks (scratch_card, spin_wheel, puzzle, quiz)
- Creates fresh tasks with updated coin ranges:
  - **Scratch Card:** 10-80 coins
  - **Spin Wheel:** 10-50 coins
  - **Puzzle:** 5-20 coins
  - **Quiz:** 5-20 coins
- Ensures all tasks are active

### 3. `verify_tasks`
- Shows statistics about tasks in database
- Lists all active tasks
- Helps verify everything is correct

## ✅ Expected Output

After running all commands, you should see:

```
Step 1: Removing video tasks...
✅ Deactivated X video task(s)
Video tasks removed successfully!

Step 2: Creating game tasks...
Deleted X existing game tasks
✅ Created: Scratch Card - Win Coins! (type: scratch_card)
✅ Created: Spin the Wheel (type: spin_wheel)
✅ Created: Math Puzzle (type: puzzle)
✅ Created: Quick Quiz (type: quiz)

✅ Created 4 game tasks!
✅ Total active tasks: 4
✅ Game tasks: 4

Game tasks created successfully!

Step 3: Verifying tasks...
📊 Task Statistics:
   Total tasks in database: 4
   Active tasks: 4

✅ Active Tasks Found:
   - Scratch Card - Win Coins! (scratch_card)
   - Spin the Wheel (spin_wheel)
   - Math Puzzle (puzzle)
   - Quick Quiz (quiz)
```

## 🐛 Troubleshooting

### Error: "Unauthorized. Please login"
**Solution:** Run `railway login` first

### Error: "No project linked"
**Solution:** Run `railway link` in the backend directory

### Error: "Command not found: railway"
**Solution:** Install Railway CLI: `npm install -g @railway/cli`

### Error: "Python command not found"
**Solution:** Railway should have Python installed. Check your `nixpacks.toml` configuration.

## 🎯 Verification

After running commands:

1. **Check Railway Dashboard:**
   - Go to your Railway project
   - Check the "Deployments" tab
   - Look for successful deployments

2. **Check Frontend:**
   - Redeploy frontend (if needed)
   - Visit `/tasks` page
   - Verify:
     - ✅ No video tasks visible
     - ✅ Scratch Card shows "10-80 coins"
     - ✅ Spin Wheel shows "10-50 coins"
     - ✅ Quiz still visible

3. **Test the Games:**
   - Play Scratch Card → Should reward 10-80 coins
   - Play Spin Wheel → Should reward 10-50 coins
   - Check wallet balance updates correctly

## 📝 Notes

- All commands are idempotent (safe to run multiple times)
- Video tasks are deactivated, not deleted
- Coin ranges are enforced server-side
- Frontend will automatically show updated ranges after redeployment

---

**Ready to run!** Just follow the steps above.

