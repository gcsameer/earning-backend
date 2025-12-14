# 🔍 How to Check if CORS is Configured on Railway

## The Problem
Backend is deployed, but CORS is still not working. We need to verify if the environment variables are being loaded.

---

## ✅ Step 1: Check Railway Logs for CORS Configuration

1. Go to Railway → Your Backend → **Deploy Logs** tab
2. Scroll to the **beginning** of the logs (when Django starts)
3. Look for these lines:
   ```
   CORS_ALLOWED_ORIGINS: ['http://localhost:3000', 'https://earning-frontend.vercel.app', 'https://nepearn.vercel.app']
   CSRF_TRUSTED_ORIGINS: ['https://earning-backend-production.up.railway.app', ...]
   ```

**What this means:**
- ✅ **If you see these lines** → CORS configuration is loaded correctly
- ❌ **If you DON'T see these lines** → Environment variables are not set or not being read

---

## ✅ Step 2: Check Environment Variables on Railway

1. Go to Railway → Your Backend → **Variables** tab
2. Look for these variables:

**Variable 1: `CORS_ALLOWED_ORIGINS`**
- Should exist
- Value should be: `http://localhost:3000,https://earning-frontend.vercel.app,https://nepearn.vercel.app`
- **NO SPACES** after commas

**Variable 2: `CSRF_TRUSTED_ORIGINS`**
- Should exist
- Value should be: `https://earning-backend-production.up.railway.app,https://earning-frontend.vercel.app,https://nepearn.vercel.app`
- **NO SPACES** after commas

---

## ✅ Step 3: Test CORS from Browser Console

1. Open `https://nepearn.vercel.app` in browser
2. Press **F12** → **Console** tab
3. Run this command:
   ```javascript
   fetch('https://earning-backend-production.up.railway.app/api/auth/token/', {
     method: 'OPTIONS',
     headers: {
       'Origin': 'https://nepearn.vercel.app',
       'Access-Control-Request-Method': 'POST',
       'Access-Control-Request-Headers': 'content-type'
     }
   })
   .then(r => {
     console.log('Status:', r.status);
     console.log('CORS Headers:');
     r.headers.forEach((value, key) => {
       if (key.toLowerCase().includes('access-control')) {
         console.log(`  ${key}: ${value}`);
       }
     });
     return r;
   })
   .catch(err => console.error('Error:', err));
   ```

**Expected Results:**

✅ **If CORS is working:**
- Status: 200 or 204
- Headers include: `access-control-allow-origin: https://nepearn.vercel.app`
- Headers include: `access-control-allow-methods: POST, GET, OPTIONS, ...`

❌ **If CORS is broken:**
- Status: 0 (blocked)
- Error: "Access to fetch at ... has been blocked by CORS policy"
- No CORS headers in response

---

## ✅ Step 4: Check HTTP Logs on Railway

1. Go to Railway → Your Backend → **HTTP Logs** tab
2. Try logging in from `https://nepearn.vercel.app`
3. Look for the `/api/auth/token/` request in the logs
4. Check if you see:
   - ✅ Request received (status 200, 401, etc.)
   - ❌ No request (means CORS is blocking it before it reaches the server)

---

## 🚨 Common Issues

### Issue 1: Variables Not in Logs

**Symptom:** CORS configuration lines don't appear in Deploy Logs

**Solution:**
1. Verify variables exist in Railway Variables tab
2. Delete and recreate them (sometimes Railway doesn't pick up edits)
3. Redeploy backend
4. Check logs again

### Issue 2: Variables Have Wrong Format

**Symptom:** Variables exist but CORS still doesn't work

**Check:**
- No spaces after commas
- Correct protocol (`https://` not `http://`)
- No trailing slashes
- Exact match: `https://nepearn.vercel.app` (not `.com` or `.net`)

### Issue 3: Backend Not Restarted

**Symptom:** Variables are set but logs don't show them

**Solution:**
- Redeploy the backend
- Environment variables are only loaded at startup

---

## 📋 Quick Verification Checklist

- [ ] Environment variables exist in Railway Variables tab
- [ ] Variable values have NO SPACES
- [ ] Backend was redeployed after setting variables
- [ ] CORS configuration appears in Deploy Logs
- [ ] OPTIONS preflight request returns CORS headers
- [ ] HTTP Logs show requests reaching the server

---

## 💡 Pro Tip

If CORS configuration doesn't appear in logs, the environment variables aren't being read. This usually means:
1. Variables don't exist (check Variables tab)
2. Variable names are misspelled (case-sensitive: `CORS_ALLOWED_ORIGINS`)
3. Backend wasn't restarted after setting variables (redeploy)

