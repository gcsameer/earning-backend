# 🚨 URGENT: Fix CORS on Railway - Step by Step

## Current Problem
- ❌ "Cannot connect to server" error
- ❌ "Provisional headers are shown" warning
- ❌ Login/Register not working

## Root Cause
Railway environment variable `CORS_ALLOWED_ORIGINS` doesn't include `https://nepearn.vercel.app`

---

## ✅ SOLUTION: Set Environment Variable (5 Minutes)

### Step 1: Login to Railway
1. Go to: https://railway.app
2. Login with your Railway account

### Step 2: Select Your Backend Project
1. Click on your backend project (should be named something like "earning-backend" or similar)
2. You'll see the project dashboard

### Step 3: Open Variables Tab
1. Look for **"Variables"** in the left sidebar menu
2. OR click on the **"Variables"** tab at the top
3. You'll see a list of environment variables

### Step 4: Add/Update CORS_ALLOWED_ORIGINS
1. **If the variable exists:**
   - Click on `CORS_ALLOWED_ORIGINS`
   - Click "Edit" or double-click the value
   - Update the value to: `http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app`
   - Click "Save"

2. **If the variable doesn't exist:**
   - Click **"+ New Variable"** or **"Add Variable"**
   - **Name:** `CORS_ALLOWED_ORIGINS`
   - **Value:** `http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app`
   - Click "Save" or "Add"

### Step 5: Add/Update CSRF_TRUSTED_ORIGINS
1. **If the variable exists:**
   - Click on `CSRF_TRUSTED_ORIGINS`
   - Update the value to: `https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app`
   - Click "Save"

2. **If the variable doesn't exist:**
   - Click **"+ New Variable"**
   - **Name:** `CSRF_TRUSTED_ORIGINS`
   - **Value:** `https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app`
   - Click "Save"

### Step 6: Redeploy Backend
1. Go to **"Deployments"** tab (or look for "Redeploy" button)
2. Click **"Redeploy"** or **"Deploy"** or **"New Deployment"**
3. Wait 1-2 minutes for deployment to complete
4. You'll see logs showing the deployment progress

### Step 7: Test
1. Go to: https://nepearn.vercel.app/login
2. Try logging in
3. Open DevTools (F12) → Network tab
4. Check the request - "Provisional headers" should be GONE ✅
5. Login should work! ✅

---

## 🔍 Verify It's Working

After redeployment, check the Network tab:
1. Click on the `/api/auth/token/` request
2. Go to "Headers" tab
3. Scroll to "Response Headers"
4. You should see: `Access-Control-Allow-Origin: https://nepearn.vercel.app`

If you see that header, CORS is fixed! ✅

---

## ⚠️ Common Mistakes

1. **Spaces in values** - Make sure there are NO spaces:
   - ❌ Wrong: `http://localhost:3000, https://nepearn.vercel.app`
   - ✅ Correct: `http://localhost:3000,https://nepearn.vercel.app`

2. **Forgetting to redeploy** - Variables only take effect after redeployment

3. **Typo in domain** - Make sure it's exactly: `https://nepearn.vercel.app` (not `.com` or `.net`)

---

## 📞 Still Not Working?

If it's still not working after setting the variable and redeploying:
1. Check Railway logs for errors
2. Verify the variable was saved correctly
3. Make sure you redeployed after setting the variable
4. Clear browser cache and try again

