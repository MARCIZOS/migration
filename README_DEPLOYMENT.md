# PDMS - AI Portfolio Optimizer

> Advanced portfolio analysis dashboard with AI-powered insights, stress testing, and hierarchical clustering.

## 🚀 Quick Start

### Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/your-username/migration.git
cd migration
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

2. **Start backend (Terminal 1):**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```

3. **Start frontend (Terminal 2):**
```bash
streamlit run app/dashboard/streamlit_app.py --server.port 8600
```

4. **Open browser:**
```
http://localhost:8600
```

### Demo Credentials
- **Email:** demo@pdms.com
- **Password:** demo123

---

## 📱 Cloud Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete Streamlit Cloud + Backend setup.

### Quick Summary
1. Push to GitHub
2. Deploy Streamlit Frontend → https://share.streamlit.io/
3. Deploy Backend → https://render.com/ (or Railway/Azure)
4. Add secrets in Streamlit Cloud dashboard
5. Update backend URL in code

---

## 📊 Features

- **Portfolio Input:** CSV upload or manual asset entry
- **Risk Analysis:** Volatility, VaR, CVaR, max drawdown
- **Correlation Matrix:** Interactive heatmap with clustering
- **Hierarchical Clustering:** Ward linkage asset grouping
- **Diversification Metrics:** ENB (Effective Number of Bets)
- **Stress Testing:** Macroeconomic scenario analysis
- **AI Insights:** Groq LLM-powered portfolio explanations
- **Export:** JSON download for further analysis

---

## 🏗️ Architecture

```
Frontend: Streamlit (Port 8600)
    ↓
FastAPI Backend (Port 8002)
    ↓
Services:
  - yfinance (data)
  - scipy (clustering)
  - scikit-learn (dimensionality reduction)
  - Plotly (visualization)
  - Groq (LLM)
```

---

## 📁 Project Structure

```
migration/
├── app/
│   ├── main.py                          # FastAPI entry point
│   ├── api/
│   │   ├── routes.py                    # Portfolio analysis endpoint
│   │   └── auth_routes.py               # Authentication
│   ├── dashboard/
│   │   ├── streamlit_app.py             # Main Streamlit UI (2560+ lines)
│   │   └── pages/
│   │       └── dashboard.py             # Legacy dashboard
│   ├── models/
│   │   ├── portfolio.py                 # Data models
│   │   └── auth.py
│   └── services/
│       ├── data_service.py              # yfinance data
│       ├── risk_service.py              # Risk metrics
│       ├── clustering_service.py        # Asset clustering
│       ├── correlation_service.py       # Correlation analysis
│       ├── diversification_service.py   # ENB scoring
│       ├── stress_service.py            # Stress testing
│       ├── ai_service.py                # Groq LLM
│       ├── portfolio_service.py         # Portfolio validation
│       └── auth_service.py              # Auth helpers
├── requirements.txt                     # Python dependencies
├── .env                                 # Environment variables (local)
├── .env.example                         # Example .env template
├── .streamlit/
│   └── secrets.toml                    # Streamlit secrets (local)
├── streamlit_app.py                     # Cloud entry point
├── DEPLOYMENT_GUIDE.md                  # Full deployment instructions
└── README.md                            # This file
```

---

## 🔐 Security

- **Secrets:** Store in `.env` (local) or Streamlit Cloud dashboard (production)
- **API Keys:** Never commit credentials
- **CORS:** Enabled for frontend-backend communication
- **Auth:** JWT + bcrypt for user management

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.104.1 | Backend framework |
| Streamlit | 1.28.1 | Frontend framework |
| Plotly | 5.17.0 | Interactive charts |
| yfinance | 0.2.32 | Stock price data |
| scipy | 1.11.3 | Clustering algorithms |
| scikit-learn | 1.3.2 | ML utilities |
| Groq | 0.4.2 | LLM API |
| Pandas | 2.1.0 | Data processing |
| NumPy | 1.24.3 | Numerical computing |

---

## 🐛 Troubleshooting

**Backend won't start?**
```bash
# Check port isn't in use
lsof -i :8002  # macOS/Linux
netstat -ano | findstr :8002  # Windows
```

**Streamlit can't find modules?**
```bash
# Ensure you're in venv
source venv/Scripts/activate
pip install -r requirements.txt
```

**Connection refused?**
- Backend at `http://127.0.0.1:8002/portfolio`
- Check `.env` and `BACKEND_URL` in `app/dashboard/streamlit_app.py`

**Groq API errors?**
- Verify `GROQ_API_KEY` in `.env`
- Check API key is valid at groq.com

---

## 📝 License

MIT License

---

## 👨‍💻 Support

For questions or issues:
1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review `.env.example` for configuration
3. Check logs: `tail -f app_logs.txt`

---

**Last Updated:** April 11, 2026
