# 🚨 IMPORTANT: Railway Must Deploy from `main` Branch

## Current Issue
- ✅ All code pushed to GitHub `main` branch
- ❌ CORS still failing ("Provisional headers" warning)
- ❌ Railway might still be deploying from `master` branch

---

## ✅ SOLUTION: Update Railway to Deploy from `main`

### Step 1: Update Railway Branch Configuration

1. Go to Railway Dashboard → Your Backend Project
2. Go to **Settings** tab
3. Look for **"Source"** or **"Repository"** section
4. Find **"Branch"** or **"Deploy Branch"** setting
5. Change it from `master` to `main`
6. Save the changes

**OR if you can't find the branch setting:**

1. Go to Railway → Your Backend → **Settings** tab
2. Look for **"Connect GitHub"** or **"Source"** section
3. You might need to **disconnect and reconnect** the repository
4. When reconnecting, make sure to select the `main` branch

---

### Step 2: Force Redeploy from `main` Branch

1. Go to Railway → Your Backend → **Deployments** tab
2. Click **"Redeploy"** or **"Deploy Latest"**
3. This should now pull from the `main` branch
4. Wait 3-5 minutes for deployment

---

### Step 3: Verify CORS Configuration in Logs

After redeployment, check **Deploy Logs** for:

```
==================================================
CORS Configuration:
  CORS_ALLOWED_ORIGINS: ['http://localhost:3000', 'https://earning-frontend.vercel.app', 'https://nepearn.vercel.app']
  CSRF_TRUSTED_ORIGINS: ['https://earning-backend-production.up.railway.app', ...]
==================================================
```

**If you see this:** CORS is configured! Test login/register now.

**If you DON'T see this:** The latest code isn't deployed yet. Check Step 1 again.

---

### Step 4: Verify Environment Variables

1. Go to Railway → Your Backend → **Variables** tab
2. Verify `CORS_ALLOWED_ORIGINS` exists with value:
   ```
   http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app
   ```
   (NO SPACES after commas)

3. Verify `CSRF_TRUSTED_ORIGINS` exists with value:
   ```
   https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app
   ```
   (NO SPACES after commas)

---

### Step 5: Test After Redeployment

1. **Use Incognito/Private window** (clear cache)
2. Go to: `https://nepearn.vercel.app/register`
3. Try registering
4. Open DevTools (F12) → Network tab
5. Check the `/api/auth/register/` request:
   - Status should be **200** or **400** (not blocked)
   - **"Provisional headers" warning should be GONE** ✅
   - Response Headers should show: `Access-Control-Allow-Origin: https://nepearn.vercel.app`

---

## 🔍 How to Check Which Branch Railway is Using

1. Go to Railway → Your Backend → **Deployments** tab
2. Look at the latest deployment
3. Check the commit hash
4. Compare it with GitHub commits on `main` branch
5. If they don't match, Railway is using the wrong branch

---

## 📋 Quick Checklist

- [ ] Updated Railway to deploy from `main` branch (not `master`)
- [ ] Redeployed backend on Railway
- [ ] Verified CORS configuration appears in Deploy Logs
- [ ] Verified environment variables are set correctly (no spaces)
- [ ] Tested register/login - no "Provisional headers" warning
- [ ] Response headers show `Access-Control-Allow-Origin`

---

## 💡 Key Points

1. **Railway must deploy from `main`** - The latest CORS fixes are on `main`, not `master`
2. **Environment variables must be set** - `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`
3. **Must redeploy after changes** - Variables and code changes only take effect after redeployment
4. **CORS logs must appear** - If you don't see CORS configuration in logs, the latest code isn't deployed

The most important step is ensuring Railway is configured to deploy from the `main` branch!

