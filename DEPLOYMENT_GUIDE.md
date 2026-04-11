# ============================================================================
# STREAMLIT CLOUD DEPLOYMENT GUIDE
# ============================================================================

## Step 1: Prepare Your Repository

✅ Files already created:
- `streamlit_app.py` - Entry point for Streamlit Cloud
- `.streamlit/secrets.toml` - Local development secrets
- `requirements.txt` - Dependencies (already exists)

## Step 2: Push to GitHub

```bash
git add .
git commit -m "Setup Streamlit Cloud deployment"
git push origin main
```

## Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub (create account if needed)
3. Click "New app"
4. Fill in:
   - **Repository:** your-username/migration
   - **Branch:** main
   - **Main file path:** streamlit_app.py
5. Click "Deploy"

## Step 4: Configure Secrets in Streamlit Cloud

⚠️ **IMPORTANT:** Don't commit .env or hardcoded secrets!

1. After deployment, go to your app's settings (⋮ menu → Settings)
2. Click "Secrets" tab
3. Paste this in the secrets editor:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. Save and app will redeploy

## Step 5: Deploy Backend

Your frontend needs a backend API running. Choose one:

### Option A: Render (Recommended - Free tier)
1. Go to https://render.com/
2. Create account
3. Click "New +" → "Web Service"
4. Connect GitHub repo
5. Fill in:
   - **Name:** pdms-backend
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8002`
   - **Environment:** Python 3.9+

### Option B: Railway
1. Go to https://railway.app/
2. Create project
3. Deploy from GitHub
4. Set start command: `uvicorn app.main:app --host 0.0.0.0`

### Option C: Azure Container Instances
```bash
az container create --resource-group mygroup --name pdms-backend \
  --image myregistry.azurecr.io/pdms:latest \
  --environment-variables GROQ_API_KEY=your_key
```

## Step 6: Update Backend URL in Streamlit App

After deploying backend, update `BACKEND_URL` in `app/dashboard/streamlit_app.py`:

```python
# Change from local:
BACKEND_URL = "http://127.0.0.1:8002/portfolio"

# To deployed backend (example Render):
BACKEND_URL = "https://pdms-backend.onrender.com/portfolio"
```

Then push changes:
```bash
git add app/dashboard/streamlit_app.py
git commit -m "Update backend URL for production"
git push origin main
```

Streamlit Cloud will auto-redeploy.

## Step 7: Test Your App

Visit: `https://your-app-name.streamlit.app`

✅ Verify:
- Landing page loads
- Login works (demo@pdms.com / demo123)
- Portfolio analysis works end-to-end

## Troubleshooting

**Backend connection error?**
- Check backend is running: `curl https://pdms-backend.onrender.com/health`
- Update BACKEND_URL correctly
- Check CORS settings in `app/main.py`

**Secrets not loading?**
- View app logs: Check "Settings" → "Logs"
- Ensure secrets are saved in Streamlit Cloud dashboard
- Clear browser cache and refresh

**App crashes?**
- Check requirements.txt has all packages
- View full error: Settings → Logs
- Enable debug mode locally

## Cost Estimates

- Streamlit Cloud: Free (tier limits apply)
- Render Backend: $7/month (paid tier)
- Total: ~$7/month for production deployment

