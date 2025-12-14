# 🚨 FIX CORS - Action Plan

## The Problem
- Backend code is updated ✅
- Environment variables might be set ✅
- **But backend needs to be REDEPLOYED** ❌

---

## ✅ DO THIS NOW (3 Steps)

### Step 1: Verify Environment Variables on Railway

1. Go to: https://railway.app
2. Select your **backend project**
3. Click **"Variables"** tab
4. Check these two variables exist:

**Variable 1: `CORS_ALLOWED_ORIGINS`**
- Value should be (NO SPACES):
```
http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

**Variable 2: `CSRF_TRUSTED_ORIGINS`**
- Value should be (NO SPACES):
```
https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

**⚠️ IMPORTANT:** 
- NO spaces after commas
- NO trailing slashes
- Use `https://` (not `http://`) for production URLs

---

### Step 2: REDEPLOY Backend

**This is the critical step!**

1. In Railway Dashboard → Your Backend Project
2. Go to **"Deployments"** tab (or look for "Redeploy" button)
3. Click **"Redeploy"** or **"Deploy Latest"**
4. **Wait 2-3 minutes** for deployment to complete
5. Check the deployment logs to ensure it succeeded

**Why this is needed:**
- Environment variables only take effect after redeployment
- New code (CORS improvements) needs to be deployed
- Django settings are loaded at startup

---

### Step 3: Test Login

1. **Clear browser cache** or use **Incognito/Private window**
2. Go to: `https://nepearn.vercel.app/login`
3. Try logging in
4. Open DevTools (F12) → Network tab
5. Check the `/api/auth/token/` request:
   - Status should be **200** (success) or **401** (wrong credentials)
   - **NOT blocked** (no CORS error)
   - Response Headers should show: `Access-Control-Allow-Origin: https://nepearn.vercel.app`
   - **"Provisional headers" warning should be GONE** ✅

---

## 🔍 How to Verify It's Fixed

### Test 1: Check Response Headers
1. Open DevTools (F12) → Network tab
2. Try logging in
3. Click on the `/api/auth/token/` request
4. Go to "Headers" tab → Scroll to "Response Headers"
5. You should see: `Access-Control-Allow-Origin: https://nepearn.vercel.app`

### Test 2: Check Console
1. Open DevTools (F12) → Console tab
2. Try logging in
3. You should **NOT** see CORS errors like:
   - ❌ "Access to fetch at ... has been blocked by CORS policy"
   - ❌ "No 'Access-Control-Allow-Origin' header"

### Test 3: Check Network Tab
1. Open DevTools (F12) → Network tab
2. Try logging in
3. The request should show:
   - ✅ Status: 200 or 401 (not blocked)
   - ✅ No "Provisional headers" warning
   - ✅ Response received

---

## 🚨 If Still Not Working

### Check Railway Logs
1. Railway → Your Backend → **Logs** tab
2. Look for lines containing:
   - `CORS_ALLOWED_ORIGINS:`
   - `CSRF_TRUSTED_ORIGINS:`
3. Verify these match what you set in environment variables

### Common Issues

**Issue 1: Variable has spaces**
- ❌ Wrong: `http://localhost:3000, https://nepearn.vercel.app`
- ✅ Correct: `http://localhost:3000,https://nepearn.vercel.app`

**Issue 2: Backend not redeployed**
- Solution: Go to Deployments → Click "Redeploy"

**Issue 3: Browser cache**
- Solution: Use Incognito/Private window or clear cache

**Issue 4: Wrong protocol**
- ❌ Wrong: `http://nepearn.vercel.app` (should be `https://`)
- ✅ Correct: `https://nepearn.vercel.app`

---

## 📋 Quick Checklist

- [ ] `CORS_ALLOWED_ORIGINS` is set on Railway (no spaces)
- [ ] `CSRF_TRUSTED_ORIGINS` is set on Railway (no spaces)
- [ ] Backend was **REDEPLOYED** after setting variables
- [ ] Deployment completed successfully (check logs)
- [ ] Browser cache cleared (or using Incognito)
- [ ] Tested login - no CORS errors
- [ ] Response headers show `Access-Control-Allow-Origin`

---

## 💡 Pro Tip

After redeploying, wait 1-2 minutes for the backend to fully start, then test. Railway deployments can take a moment to propagate.

