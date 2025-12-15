# 🔍 Backend Deployment Verification Guide

## ✅ Git Status: All Code Committed

All backend code is committed and pushed to GitHub. Here's what should be deployed:

## 📋 All Backend Files That Should Be Deployed

### Core Views (API Endpoints)
- ✅ `core/views.py` - Main views (auth, tasks, wallet, withdraw)
- ✅ `core/views_email_verification.py` - Email verification API
- ✅ `core/views_daily_bonus.py` - Daily bonus API
- ✅ `core/views_referrals.py` - Referral analytics API
- ✅ `core/views_games.py` - Game task completion API
- ✅ `core/views_analytics.py` - User analytics API
- ✅ `core/views_streak.py` - Login streak API
- ✅ `core/views_achievements.py` - Achievements API
- ✅ `core/views_challenges.py` - Daily challenges API
- ✅ `core/views_cors_test.py` - CORS test endpoint
- ✅ `core/views_health.py` - Health check endpoint
- ✅ `core/views_cpx.py` - CPX offerwall integration

### Models
- ✅ `core/models.py` - All database models (User, Task, Achievement, Challenge, etc.)

### URLs
- ✅ `core/urls.py` - All API route definitions

### Management Commands
- ✅ `core/management/commands/create_game_tasks.py` - Create game tasks
- ✅ `core/management/commands/verify_tasks.py` - Verify tasks
- ✅ `core/management/commands/remove_video_tasks.py` - Remove video tasks

### Configuration
- ✅ `earning_backend/settings.py` - Django settings (DEBUG=False by default)
- ✅ `nixpacks.toml` - Railway build configuration
- ✅ `requirements.txt` - All Python dependencies

---

## 🚨 If Backend Code Is Missing on Railway

### Step 1: Force Redeploy on Railway

1. Go to Railway Dashboard: https://railway.app
2. Select your **backend project**
3. Go to **Deployments** tab
4. Click **"..."** on the latest deployment
5. Click **"Redeploy"**
6. Wait 3-5 minutes for deployment to complete

### Step 2: Clear Build Cache

1. In Railway Dashboard → Your Backend Project
2. Go to **Settings** → **General**
3. Look for **"Clear Build Cache"** or **"Rebuild"** option
4. Clear cache and redeploy

### Step 3: Verify Git Connection

1. Go to **Settings** → **Source**
2. Verify the repository is connected: `gcsameer/earning-backend`
3. Check that it's deploying from `main` branch
4. Verify the **Root Directory** is set correctly (should be `earning-app/backend` or `.`)

### Step 4: Check Build Logs

1. Go to **Deployments** tab
2. Click on the latest deployment
3. Check **Build Logs** for:
   - ✅ "Collecting static files"
   - ✅ "Running migrations"
   - ✅ "Creating game tasks"
   - ✅ "Starting gunicorn"
   - ❌ Any error messages

---

## 🔍 How to Verify API Endpoints Are Live

### Test Each Endpoint:

1. **Health Check:**
   ```
   GET https://your-backend.railway.app/health/
   ```
   Should return: `{"status": "ok"}`

2. **Login:**
   ```
   POST https://your-backend.railway.app/api/auth/token/
   ```

3. **Register:**
   ```
   POST https://your-backend.railway.app/api/auth/register/
   ```

4. **Email Verification:**
   ```
   POST https://your-backend.railway.app/api/auth/verify-email/
   ```

5. **Tasks:**
   ```
   GET https://your-backend.railway.app/api/tasks/
   ```

6. **Analytics:**
   ```
   GET https://your-backend.railway.app/api/analytics/
   ```

7. **Streak:**
   ```
   POST https://your-backend.railway.app/api/streak/
   ```

8. **Achievements:**
   ```
   GET https://your-backend.railway.app/api/achievements/
   ```

9. **Challenges:**
   ```
   GET https://your-backend.railway.app/api/challenges/
   ```

---

## 🛠️ Common Issues & Fixes

### Issue 1: API Returns 404
**Fix:**
- Check Railway deployment logs
- Verify `core/urls.py` is correct
- Ensure migrations ran successfully
- Check if endpoint path is correct

### Issue 2: Database Errors
**Fix:**
- Check Railway logs for migration errors
- Verify PostgreSQL is connected
- Run migrations manually if needed:
  ```bash
  railway run python manage.py migrate
  ```

### Issue 3: Environment Variables Not Working
**Fix:**
- Verify variables are set in Railway
- Check variable names (case-sensitive)
- Redeploy after adding/changing variables
- Check logs for variable loading

### Issue 4: Build Fails
**Fix:**
- Check build logs in Railway
- Verify `requirements.txt` is correct
- Check `nixpacks.toml` configuration
- Test build locally: `pip install -r requirements.txt`

---

## ✅ Quick Verification Checklist

- [ ] All view files committed to Git
- [ ] All models committed to Git
- [ ] All URLs configured correctly
- [ ] All migrations created and committed
- [ ] `requirements.txt` includes all dependencies
- [ ] `nixpacks.toml` configured correctly
- [ ] Railway deployment successful
- [ ] All API endpoints accessible
- [ ] Database migrations applied
- [ ] Game tasks created successfully

---

## 📊 Expected API Endpoints

### Authentication
- ✅ `POST /api/auth/token/` - Login
- ✅ `POST /api/auth/token/refresh/` - Refresh token
- ✅ `POST /api/auth/register/` - Register
- ✅ `POST /api/auth/verify-email/` - Verify email

### User Profile
- ✅ `GET /api/me/` - Get user profile

### Tasks
- ✅ `GET /api/tasks/` - List tasks
- ✅ `POST /api/tasks/start/<id>/` - Start task
- ✅ `POST /api/tasks/complete/<id>/` - Complete task
- ✅ `POST /api/tasks/game/complete/<id>/` - Complete game task

### Wallet & Withdraw
- ✅ `GET /api/wallet/` - Get wallet
- ✅ `POST /api/withdraw/` - Request withdrawal
- ✅ `GET /api/withdraws/` - List withdrawals

### Features
- ✅ `POST /api/daily-bonus/` - Claim daily bonus
- ✅ `GET /api/referrals/` - Referral analytics
- ✅ `GET /api/analytics/` - User analytics
- ✅ `POST /api/streak/` - Login streak
- ✅ `GET /api/achievements/` - List achievements
- ✅ `POST /api/achievements/claim/<id>/` - Claim achievement
- ✅ `GET /api/challenges/` - List challenges
- ✅ `POST /api/challenges/claim/<id>/` - Claim challenge

### Ads
- ✅ `POST /api/ads/rewarded/complete/` - Rewarded ad completion

### CPX
- ✅ `GET /api/cpx/wall/` - CPX offerwall
- ✅ `POST /api/cpx/postback/` - CPX postback

### Health
- ✅ `GET /health/` - Health check

---

## 🎯 Next Steps

1. **Verify all endpoints are accessible** on Railway
2. **Check Railway deployment logs** for any errors
3. **Test each API endpoint** from frontend
4. **Verify database migrations** ran successfully
5. **Check that game tasks** were created

---

## 📝 Notes

- All code is committed and pushed ✅
- If endpoints are missing, it's likely a Railway deployment issue
- Force redeploy should fix most issues
- Check build logs for specific errors
- Environment variables must be set before deployment

---

## 🔧 Railway Commands (If Needed)

If you need to run commands manually on Railway:

```bash
# Connect to Railway
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate

# Create game tasks
railway run python manage.py create_game_tasks

# Verify tasks
railway run python manage.py verify_tasks

# Create superuser
railway run python manage.py createsuperuser
```

---

## ✅ Status

**Code Status:** ✅ All committed and pushed  
**Deployment:** ⚠️ Verify on Railway  
**Endpoints:** ⚠️ Test each endpoint  
**Database:** ⚠️ Verify migrations applied  

