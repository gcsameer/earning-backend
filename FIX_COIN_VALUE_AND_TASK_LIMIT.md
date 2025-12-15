# ✅ Fixed: Coin Value (0.1) and Task Limit (3 times per day)

## Issues Found

### 1. Coin Value Not Set
- **Problem:** `COIN_TO_RS_RATE` setting didn't exist in database
- **Default:** Code was using `0.05` in some places, `0.1` in others
- **Fix:** Created `setup_settings` command to create/update settings

### 2. Task Limit Not Working
- **Problem:** Code was checking if task was completed ONCE today, not 3 times
- **Fix:** Changed to allow 3 completions per task per day

## What Was Fixed

### 1. Coin Value (0.1)
- ✅ Created `setup_settings` management command
- ✅ Sets `COIN_TO_RS_RATE = 0.1` in database
- ✅ Fixed default value in `WalletView` to `0.1`
- ✅ Auto-runs on Railway deployment via `nixpacks.toml`

### 2. Task Limit (3 times per day)
- ✅ Changed from "once per day" to "3 times per day per task"
- ✅ Users can now complete each task 3 times per day
- ✅ Still respects overall daily limit (3 tasks total, excluding offerwall)

## How It Works Now

### Coin Value:
- **1 coin = Rs 0.1** (set in database)
- Used for wallet balance calculation
- Used for withdrawal calculations
- Auto-setup on deployment

### Task Limit:
- **Each task can be completed 3 times per day**
- Example: User can play Scratch Card 3 times, Spin Wheel 3 times, etc.
- Overall limit: 3 tasks per day (excluding offerwall)
- Offerwall has no limit

## Deployment Steps

### On Railway:

1. **Deploy the code** (already pushed)
2. **Run setup command** (auto-runs on deploy, or manually):
   ```bash
   railway run python manage.py setup_settings
   ```

3. **Verify settings**:
   ```bash
   railway run python manage.py shell
   ```
   Then in shell:
   ```python
   from core.models import Settings
   print(Settings.get_value("COIN_TO_RS_RATE", "not set"))
   # Should print: 0.1
   ```

## Manual Setup (If Needed)

If settings aren't created automatically:

```bash
# On Railway
railway run python manage.py setup_settings
```

Or via Django admin:
1. Go to `/admin/`
2. Settings → Add Setting
3. Key: `COIN_TO_RS_RATE`, Value: `0.1`
4. Save

## Testing

### Test Coin Value:
1. Check wallet balance
2. Should show: `coins * 0.1 = Rs amount`
3. Example: 100 coins = Rs 10

### Test Task Limit:
1. Complete a task (e.g., Scratch Card)
2. Complete it again (should work)
3. Complete it a 3rd time (should work)
4. Try 4th time (should fail: "You have already completed this task 3 times today")

## Files Changed

1. ✅ `core/views_games.py` - Allow 3 times per task per day
2. ✅ `core/views.py` - Fixed coin value default to 0.1
3. ✅ `core/management/commands/setup_settings.py` - New command
4. ✅ `nixpacks.toml` - Auto-run setup_settings on deploy

## Status

✅ **FIXED** - Coin value is 0.1 and users can play each task 3 times per day!

---

**Next Steps:**
1. Deploy to Railway (code is pushed)
2. Settings will auto-setup on deployment
3. Test coin value and task limits

