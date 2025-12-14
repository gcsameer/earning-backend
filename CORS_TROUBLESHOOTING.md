# 🔧 CORS Troubleshooting Guide

## Current Issue
- ❌ "Provisional headers are shown" warning
- ❌ "Invalid credentials" or "Cannot connect to server" errors
- ❌ Login/Register requests failing

---

## ✅ Step-by-Step Fix

### Step 1: Verify Environment Variable on Railway

1. Go to Railway Dashboard → Your Backend Project → **Variables** tab
2. Check if `CORS_ALLOWED_ORIGINS` exists
3. **VERIFY THE VALUE** - It should be EXACTLY:
   ```
   http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app
   ```
4. **Common Mistakes:**
   - ❌ Extra spaces: `http://localhost:3000, https://nepearn.vercel.app` (space after comma)
   - ❌ Missing `https://`: `nepearn.vercel.app` (should be `https://nepearn.vercel.app`)
   - ❌ Trailing slash: `https://nepearn.vercel.app/` (should NOT have trailing slash)
   - ✅ Correct: `http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app`

### Step 2: Verify CSRF_TRUSTED_ORIGINS

1. Check if `CSRF_TRUSTED_ORIGINS` exists
2. **VERIFY THE VALUE** - It should be EXACTLY:
   ```
   https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app
   ```

### Step 3: Redeploy Backend

**IMPORTANT:** Environment variables only take effect after redeployment!

1. Go to Railway Dashboard → Your Backend Project → **Deployments** tab
2. Click **"Redeploy"** or **"Deploy Latest"**
3. Wait 2-3 minutes for deployment to complete
4. Check deployment logs for any errors

### Step 4: Test CORS Endpoint

After redeployment, test the CORS endpoint:

1. Open browser and go to:
   ```
   https://earning-backend-production.up.railway.app/api/cors-test/
   ```
2. You should see a JSON response with CORS configuration
3. If you see the response, CORS middleware is working

### Step 5: Test from Frontend

1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Run this command:
   ```javascript
   fetch('https://earning-backend-production.up.railway.app/api/cors-test/', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ test: 'data' })
   })
   .then(r => r.json())
   .then(console.log)
   .catch(console.error)
   ```
4. If you see the response in console, CORS is working! ✅
5. If you see a CORS error, the environment variable is still not set correctly

### Step 6: Clear Browser Cache

Sometimes browsers cache CORS responses:

1. **Chrome/Edge:**
   - Press `Ctrl+Shift+Delete`
   - Select "Cached images and files"
   - Click "Clear data"
   - OR use Incognito/Private mode

2. **Firefox:**
   - Press `Ctrl+Shift+Delete`
   - Select "Cache"
   - Click "Clear Now"
   - OR use Private mode

### Step 7: Check Railway Logs

1. Go to Railway Dashboard → Your Backend Project → **Logs** tab
2. Look for lines containing:
   - `CORS_ALLOWED_ORIGINS:`
   - `CSRF_TRUSTED_ORIGINS:`
3. Verify these match what you set in environment variables

---

## 🔍 Debugging Checklist

- [ ] Environment variable `CORS_ALLOWED_ORIGINS` is set on Railway
- [ ] Environment variable `CSRF_TRUSTED_ORIGINS` is set on Railway
- [ ] No spaces in environment variable values
- [ ] All origins use correct protocol (`http://` or `https://`)
- [ ] No trailing slashes in origins
- [ ] Backend was redeployed after setting variables
- [ ] Browser cache was cleared
- [ ] CORS test endpoint (`/api/cors-test/`) returns data
- [ ] Railway logs show correct CORS configuration

---

## 🚨 Still Not Working?

If CORS is still not working after following all steps:

1. **Check Railway Logs:**
   - Look for any errors during startup
   - Check if CORS configuration is being logged

2. **Verify Backend is Running:**
   - Go to: `https://earning-backend-production.up.railway.app/api/cors-test/`
   - If you get a 404 or connection error, the backend might not be deployed correctly

3. **Try Temporary Fix (Development Only):**
   - On Railway, set `CORS_ALLOWED_ORIGINS` to `*` (allows all origins)
   - **WARNING:** This is insecure for production! Only use for testing.
   - Redeploy and test
   - If this works, the issue is with the specific origin value

4. **Check Frontend API URL:**
   - Verify frontend is using correct backend URL
   - Check `NEXT_PUBLIC_API_BASE_URL` in Vercel environment variables

---

## 📞 Need More Help?

If none of these steps work:
1. Check Railway deployment logs for errors
2. Verify the backend is actually running
3. Test the CORS endpoint directly in browser
4. Check if there are any firewall or network restrictions

