# Fix CORS Issue on Railway

## 🐛 Problem
"Provisional headers are shown" error when trying to login/register from `https://nepearn.vercel.app`

## ✅ Solution: Set Environment Variable on Railway

### Step 1: Go to Railway Dashboard
1. Open https://railway.app
2. Select your backend project

### Step 2: Add/Update Environment Variables
1. Click on the **"Variables"** tab
2. Add or update the following variables:

**Variable 1: `CORS_ALLOWED_ORIGINS`**
```
Value: http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

**Variable 2: `CSRF_TRUSTED_ORIGINS`**
```
Value: https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

### Step 3: Redeploy
1. After setting the variables, click **"Redeploy"** or trigger a new deployment
2. Wait for deployment to complete

### Step 4: Verify
1. Try logging in from `https://nepearn.vercel.app`
2. Check browser DevTools → Network tab
3. The "Provisional headers" warning should be gone
4. Requests should succeed with status 200

## 🔍 Why This Works

Environment variables on Railway override the code defaults. By explicitly setting `CORS_ALLOWED_ORIGINS` to include `https://nepearn.vercel.app`, the backend will allow requests from that origin.

## 📝 Notes

- Make sure there are **no spaces** in the environment variable values
- Origins should be **comma-separated** (no spaces after commas)
- After setting variables, **always redeploy** for changes to take effect

