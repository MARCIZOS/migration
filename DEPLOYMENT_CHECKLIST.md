# 🚀 STREAMLIT CLOUD DEPLOYMENT CHECKLIST

## Pre-Deployment ✅

- [ ] All code committed to GitHub
- [ ] `.env` and `.streamlit/secrets.toml` added to `.gitignore`
- [ ] `requirements.txt` up to date with all dependencies
- [ ] `streamlit_app.py` exists at project root (✅ Already created)
- [ ] Backend API working locally on http://127.0.0.1:8002
- [ ] Streamlit app working locally with `streamlit run streamlit_app.py`

## Deployment Steps 🌐

### 1. Prepare Repository
```bash
# Make sure everything is committed
git status
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy Frontend to Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Click "New app"
3. Enter:
   - Repository: `your-username/migration`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
4. Click "Deploy"
5. Wait 2-3 minutes for deployment to complete

### 3. Add Secrets in Streamlit Cloud
1. Go to your app URL (will be shown after deployment)
2. Click ⋮ menu (top right)
3. Click "Settings"
4. Click "Secrets" tab
5. Paste this exactly:
```
GROQ_API_KEY = "your_groq_api_key_here"
```
6. Click "Save"
7. App will redeploy automatically

### 4. Deploy Backend (Choose ONE)

#### Option A: Render (Recommended)
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Fill in:
   - Name: `pdms-backend`
   - Environment: `Python 3.9`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Click "Create Web Service"
7. Wait for build to complete (2-5 minutes)
8. Copy your backend URL (e.g., `https://pdms-backend.onrender.com`)

#### Option B: Railway
1. Go to https://railway.app
2. Create project → Deploy from GitHub
3. Select your repo
4. Add environment variable:
   - Key: `GROQ_API_KEY`
   - Value: `your_groq_api_key_here` (from https://console.groq.com/keys)
5. Deploy

### 5. Update Backend URL
After backend is deployed, update the URL in your code:

File: `app/dashboard/streamlit_app.py` (line ~21)

Find:
```python
BACKEND_URL = "http://127.0.0.1:8002/portfolio"
```

Replace with:
```python
BACKEND_URL = "https://pdms-backend.onrender.com/portfolio"  # Use YOUR backend URL
```

Commit and push:
```bash
git add app/dashboard/streamlit_app.py
git commit -m "Update backend URL for production"
git push origin main
```

Streamlit Cloud will auto-redeploy.

### 6. Test Your Deployment ✅

1. Visit your Streamlit Cloud URL (you'll have received it in email)
2. Login with demo credentials:
   - Email: `demo@pdms.com`
   - Password: `demo123`
3. Upload sample portfolio or use defaults
4. Click "Analyze Portfolio"
5. Verify all charts and metrics load

## Troubleshooting 🔧

### "Cannot connect to backend"
- ✓ Check backend URL is correct in `streamlit_app.py`
- ✓ Verify backend is running: `curl https://pdms-backend.onrender.com/docs`
- ✓ Wait 30 seconds for changes to deploy in Streamlit Cloud
- ✓ Check CORS is enabled in `app/main.py`

### "ModuleNotFoundError: No module named..."
- ✓ Ensure all packages are in `requirements.txt`
- ✓ Rebuild by redeploying in Streamlit Cloud (Settings → Reboot)

### "GROQ_API_KEY not found"
- ✓ Verify secrets are added in Streamlit Cloud dashboard
- ✓ Check exact formatting: `GROQ_API_KEY = "your-key"`
- ✓ Force redeploy: Settings → Reboot app

### "Backend returning 502 Bad Gateway"
- ✓ Check render.com backend logs for errors
- ✓ Verify yfinance can download data
- ✓ Test locally: `python -m pytest test_system.py`

## Monitoring 📊

### Streamlit Cloud
- View logs: App page → ⋮ → View logs
- View app analytics: No built-in, use browser dev tools

### Backend (Render)
- View logs: Dashboard → Service → Logs
- Check metrics: Dashboard → Service → Metrics

## Scaling (Later) 📈

If you need:
- **More users:** Streamlit Community → Streamlit Cloud Professional
- **Better backend:** Render → Paid tier or Railway Professional
- **Database:** Add MongoDB Atlas
- **Caching:** Streamlit `@st.cache_data` or Redis

---

## Quick Links 🔗

| Service | URL |
|---------|-----|
| Streamlit Cloud | https://share.streamlit.io |
| Render | https://render.com |
| Railway | https://railway.app |
| Your Groq Docs | https://console.groq.com |

---

✨ **You're all set! Deploy today and share with the world!** ✨
