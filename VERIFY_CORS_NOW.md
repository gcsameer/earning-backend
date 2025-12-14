# ⚡ QUICK CORS VERIFICATION - Do This Now

## 🎯 The Problem
Even after setting environment variables, CORS might still fail if:
1. The variable value has **spaces** or **formatting issues**
2. The backend **wasn't redeployed** after setting variables
3. The **browser cache** is blocking the fix

---

## ✅ 5-Minute Fix Checklist

### 1. Check Railway Environment Variable Format

Go to Railway → Your Backend → **Variables** tab

**Variable: `CORS_ALLOWED_ORIGINS`**

❌ **WRONG (has spaces):**
```
http://localhost:3000, https://nepearn.vercel.app
```

✅ **CORRECT (no spaces):**
```
http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

**Copy this EXACT value:**
```
http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

---

### 2. Check CSRF Variable Format

**Variable: `CSRF_TRUSTED_ORIGINS`**

✅ **CORRECT value:**
```
https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

**Copy this EXACT value:**
```
https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app
```

---

### 3. Redeploy Backend

1. Go to Railway → Your Backend → **Deployments** tab
2. Click **"Redeploy"** button
3. Wait 2-3 minutes
4. Check logs to ensure deployment succeeded

---

### 4. Test CORS Endpoint

Open this URL in your browser:
```
https://earning-backend-production.up.railway.app/api/cors-test/
```

**Expected Result:**
You should see JSON like:
```json
{
  "message": "CORS is working!",
  "origin": "...",
  "cors_allowed_origins": ["http://localhost:3000", "https://earning-frontend.vercel.app", "https://nepearn.vercel.app"]
}
```

If you see this, CORS is configured correctly! ✅

---

### 5. Clear Browser Cache & Test Login

1. **Open Incognito/Private window** (or clear cache)
2. Go to: `https://nepearn.vercel.app/login`
3. Try logging in
4. Open DevTools (F12) → Network tab
5. Check the `/api/auth/token/` request:
   - **Status should be 200 or 401** (not blocked)
   - **Response Headers should show:** `Access-Control-Allow-Origin: https://nepearn.vercel.app`
   - **"Provisional headers" warning should be GONE** ✅

---

## 🚨 Still Not Working?

### Test from Browser Console

1. Open `https://nepearn.vercel.app` in browser
2. Press F12 → Console tab
3. Run this command:
   ```javascript
   fetch('https://earning-backend-production.up.railway.app/api/cors-test/', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ test: 'data' })
   })
   .then(r => r.json())
   .then(data => {
     console.log('✅ CORS Working!', data);
   })
   .catch(err => {
     console.error('❌ CORS Error:', err);
   });
   ```

**If you see "✅ CORS Working!"** → CORS is fixed, the issue might be with login credentials.

**If you see "❌ CORS Error"** → The environment variable is still not set correctly or backend wasn't redeployed.

---

## 📋 Final Checklist

- [ ] `CORS_ALLOWED_ORIGINS` value has NO SPACES
- [ ] `CSRF_TRUSTED_ORIGINS` value has NO SPACES  
- [ ] Backend was REDEPLOYED after setting variables
- [ ] CORS test endpoint (`/api/cors-test/`) returns JSON
- [ ] Browser cache was cleared (or using Incognito)
- [ ] DevTools shows `Access-Control-Allow-Origin` header in response

---

## 💡 Pro Tip

If you're still having issues, check Railway logs:
1. Railway → Your Backend → **Logs** tab
2. Look for lines starting with: `CORS_ALLOWED_ORIGINS:`
3. Verify the logged values match what you set

If the logged values are wrong, the environment variable wasn't saved correctly. Delete it and recreate it.

