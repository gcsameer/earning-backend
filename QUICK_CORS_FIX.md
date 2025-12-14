# 🚨 QUICK CORS FIX - Railway Environment Variable

## The Problem
"Provisional headers are shown" = CORS is blocking requests from `https://nepearn.vercel.app`

## ✅ THE FIX (2 Minutes)

### Step 1: Go to Railway Dashboard
1. Open: https://railway.app
2. Login to your account
3. Click on your **backend project**

### Step 2: Open Variables Tab
1. Click on **"Variables"** tab (in the left sidebar or top menu)
2. You'll see a list of environment variables

### Step 3: Add/Update CORS Variables

**Find or Add this variable:**
- **Name:** `CORS_ALLOWED_ORIGINS`
- **Value:** `http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app`

**Find or Add this variable:**
- **Name:** `CSRF_TRUSTED_ORIGINS`
- **Value:** `https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app`

### Step 4: Save and Redeploy
1. Click **"Save"** or the variable will auto-save
2. Go to **"Deployments"** tab
3. Click **"Redeploy"** or trigger a new deployment
4. Wait 1-2 minutes for deployment to complete

### Step 5: Test
1. Go to `https://nepearn.vercel.app/login`
2. Try logging in
3. Check DevTools → Network tab
4. The "Provisional headers" warning should be GONE ✅

## ⚠️ Important Notes

- **NO SPACES** in the environment variable values
- Origins are **comma-separated** (no spaces after commas)
- **Must redeploy** after setting variables
- If variable already exists, **update** it (don't create duplicate)

## 🔍 How to Check if It Worked

After redeployment:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try logging in
4. Click on the `/api/auth/token/` request
5. Check the **Response Headers** section
6. You should see: `Access-Control-Allow-Origin: https://nepearn.vercel.app`

If you see that header, CORS is working! ✅

