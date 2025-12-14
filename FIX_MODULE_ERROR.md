# Fix ModuleNotFoundError: rest_framework_simplejwt

## 🐛 The Error

```
ModuleNotFoundError: No module named 'rest_framework_simplejwt'
```

## ✅ Solution

The package is in `requirements.txt` but may not be installed on Railway. Here's how to fix it:

### Option 1: Reinstall Dependencies on Railway (Recommended)

Run this command on Railway:

```bash
railway run pip install -r requirements.txt
```

Or reinstall just the missing package:

```bash
railway run pip install djangorestframework-simplejwt==5.3.1
```

### Option 2: Redeploy on Railway

The easiest fix is to **redeploy** your Railway project:

1. Go to Railway Dashboard
2. Select your backend project
3. Click **"Redeploy"** or trigger a new deployment
4. Railway will automatically install all packages from `requirements.txt`

### Option 3: Check requirements.txt

Make sure `requirements.txt` has the package:

```txt
djangorestframework-simplejwt==5.3.1
```

If it's missing, add it and commit:

```bash
git add requirements.txt
git commit -m "Add missing djangorestframework-simplejwt"
git push origin master
```

Then redeploy on Railway.

---

## 🔍 Verify Package is Installed

After installing, verify:

```bash
railway run pip list | grep simplejwt
```

Should show: `djangorestframework-simplejwt 5.3.1`

---

## 📋 Complete Fix Steps

### On Railway (via terminal or dashboard):

1. **Install missing package:**
   ```bash
   railway run pip install djangorestframework-simplejwt==5.3.1
   ```

2. **Or reinstall all dependencies:**
   ```bash
   railway run pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   railway run python -c "import rest_framework_simplejwt; print('OK')"
   ```

4. **Redeploy if needed:**
   - Go to Railway Dashboard
   - Click "Redeploy" on your service

---

## ✅ Expected Result

After fixing, the error should be gone and your Django app should start normally.

---

## 🎯 Quick Fix Command

Run this single command on Railway:

```bash
railway run pip install djangorestframework-simplejwt==5.3.1 && railway run python -c "import rest_framework_simplejwt; print('Package installed successfully!')"
```

---

**The package is already in requirements.txt - just needs to be installed on Railway!** 🚀

