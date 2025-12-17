# Daily Limits Implementation

## ✅ Changes Implemented

### 1. Daily Challenge Limits (Once Per Day)
- **Model Added**: `DailyChallengeClaim` to track daily challenge claims
- **Backend**: Updated `views_challenges.py` to:
  - Check if challenge was already claimed today before allowing claim
  - Mark challenge as claimed after successful claim
  - Return proper error message if already claimed
- **Frontend**: Updated dashboard to show "Already claimed" status
- **Mobile**: Updated dashboard to show "Already claimed" status

### 2. Task Completion Limits (3 Times Per Day Per Task)
- **Game Tasks**: Already had 3 times per day limit (in `views_games.py`)
- **Regular Tasks**: Added 3 times per day limit to `TaskCompleteView` in `views.py`
- Both now check how many times the user completed the specific task today
- Returns error message: "You have already completed this task 3 times today. Try again tomorrow."

## 📋 Database Migration Required

A new migration needs to be created for the `DailyChallengeClaim` model:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will be automatically run on Railway deployment.

## 🔧 Files Modified

### Backend:
1. `core/models.py` - Added `DailyChallengeClaim` model
2. `core/views_challenges.py` - Added claim tracking and limit enforcement
3. `core/views.py` - Added 3 times per day limit to regular tasks
4. `core/admin.py` - Registered `DailyChallengeClaim` in admin

### Frontend:
1. `pages/dashboard.js` - Added "Already claimed" status display

### Mobile:
1. `src/screens/DashboardScreen.js` - Added "Already claimed" status display

## 🎯 How It Works

### Daily Challenges:
1. When user tries to claim a challenge, backend checks if it was already claimed today
2. If already claimed, returns error: "This challenge reward has already been claimed today. Try again tomorrow."
3. If not claimed, marks it as claimed and credits coins
4. Frontend/Mobile shows "Already claimed" badge for claimed challenges

### Tasks:
1. When user completes a task (game or regular), backend checks how many times that specific task was completed today
2. If 3 or more times, returns error: "You have already completed this task 3 times today. Try again tomorrow."
3. If less than 3 times, allows completion and credits coins
4. Error messages are automatically displayed in frontend/mobile

## ✅ Testing Checklist

- [ ] Test claiming same challenge twice in one day (should fail)
- [ ] Test claiming challenge next day (should work)
- [ ] Test completing same task 4 times in one day (should fail on 4th)
- [ ] Test completing same task next day (should work)
- [ ] Verify error messages display correctly in web
- [ ] Verify error messages display correctly in mobile

