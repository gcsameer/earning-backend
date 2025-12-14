# 🚨 CRITICAL: Fix Redirect Loop (ERR_TOO_MANY_REDIRECTS)

## The Problem
- ❌ `net::ERR_TOO_MANY_REDIRECTS` error
- ❌ `301 (Moved Permanently)` status
- ❌ Requests are stuck in a redirect loop

**Root Cause:** Django's `SECURE_SSL_REDIRECT` is causing redirects because Railway's proxy isn't recognized. Railway handles HTTPS termination at the proxy level, so we need to trust the proxy headers.

---

## ✅ SOLUTION: Fixed in Code

I've updated `settings.py` to:
1. **Trust Railway's proxy headers** using `SECURE_PROXY_SSL_HEADER`
2. **Disable SSL redirect** since Railway handles HTTPS termination
3. **Keep security settings** for cookies and headers

---

## ✅ What You Need to Do

### Step 1: Redeploy Backend

1. Go to Railway → Your Backend → **Deployments** tab
2. Click **"Redeploy"** or **"Deploy Latest"**
3. Wait 3-5 minutes for deployment
4. This will pull the latest code with the redirect fix

### Step 2: Test After Redeployment

1. **Use Incognito/Private window** (clear cache)
2. Go to: `https://nepearn.vercel.app/register`
3. Try registering
4. Open DevTools (F12) → Network tab
5. Check the `/api/auth/register/` request:
   - Status should be **200** or **400** (not blocked, no redirect loop)
   - **"Provisional headers" warning should be GONE** ✅
   - No `ERR_TOO_MANY_REDIRECTS` error

### Step 3: Test OPTIONS Request

After redeployment, test from browser console:

```javascript
fetch('https://earning-backend-production.up.railway.app/api/auth/register/', {
  method: 'OPTIONS',
  headers: {
    'Origin': 'https://nepearn.vercel.app',
    'Access-Control-Request-Method': 'POST'
  }
})
.then(r => {
  console.log('✅ Status:', r.status);
  console.log('✅ CORS Headers:');
  r.headers.forEach((value, key) => {
    if (key.toLowerCase().includes('access-control')) {
      console.log(`  ${key}: ${value}`);
    }
  });
})
.catch(err => console.error('❌ Error:', err));
```

**Expected:**
- Status: 200 or 204 (not 301, not redirect loop)
- Headers include: `access-control-allow-origin: https://nepearn.vercel.app`
- No redirect errors

---

## 🔍 What Changed

**Before:**
```python
SECURE_SSL_REDIRECT = True  # This caused redirect loops
```

**After:**
```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False  # Railway handles HTTPS
```

This tells Django to:
- Trust Railway's proxy headers for HTTPS detection
- Don't redirect (Railway already handles HTTPS)
- Still enforce secure cookies and headers

---

## 📋 Quick Checklist

- [ ] Code fix pushed to GitHub `main` branch
- [ ] Redeployed backend on Railway
- [ ] Waited 3-5 minutes for deployment
- [ ] Tested register/login - no redirect errors
- [ ] Tested OPTIONS request - status 200/204
- [ ] No "Provisional headers" warning
- [ ] CORS headers appear in response

---

## 💡 Why This Happened

Railway uses a reverse proxy that:
1. Receives HTTPS requests from the internet
2. Forwards them as HTTP to your Django app internally
3. Django sees HTTP and tries to redirect to HTTPS
4. This creates an infinite redirect loop

The fix tells Django to trust Railway's `X-Forwarded-Proto` header to detect HTTPS, so it doesn't try to redirect.

---

## 🆘 Still Not Working?

If you still see redirect errors after redeployment:

1. **Check Railway Logs:**
   - Look for any errors during startup
   - Verify the deployment completed successfully

2. **Verify Environment Variables:**
   - `CORS_ALLOWED_ORIGINS` is set correctly
   - `CSRF_TRUSTED_ORIGINS` is set correctly

3. **Clear Browser Cache:**
   - Use Incognito/Private window
   - Or clear cache completely

The redirect loop fix is now in the code. Just redeploy and test!

