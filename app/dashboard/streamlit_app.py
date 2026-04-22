"""
PDMS - AI Portfolio Optimization under Macroeconomic Stress.
Premium fintech dashboard with glassmorphism and neon glow effects.
"""

import json
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from plotly.subplots import make_subplots


# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

API_BASE_URL = "http://127.0.0.1:8002"
BACKEND_URL = f"{API_BASE_URL}/portfolio"
DEFAULT_ASSETS = []

# Page config
st.set_page_config(
    page_title="PDMS - AI Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# PREMIUM FINTECH STYLING (Bella-Inspired)
# ============================================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Dark gradient background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(10, 20, 40, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 255, 255, 0.1);
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        color: #ffffff;
        margin: 15px 0;
    }
    
    .glass-card:hover {
        background: rgba(0, 255, 255, 0.08);
        border-color: rgba(0, 255, 255, 0.4);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-box {
        background: rgba(0, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
        color: #00ffff;
    }
    
    .metric-box:hover {
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.05);
        transform: translateY(-2px);
    }
    
    /* Glow effects */
    .glow-text {
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.8), 0 0 20px rgba(0, 100, 255, 0.5);
        font-weight: 700;
    }
    
    .glow-header {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin: 20px 0;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    /* Stress indicators */
    .stress-low {
        color: #00ff88;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
    }
    
    .stress-medium {
        color: #ffaa00;
        text-shadow: 0 0 10px rgba(255, 170, 0, 0.8);
    }
    
    .stress-high {
        color: #ff3333;
        text-shadow: 0 0 10px rgba(255, 51, 51, 0.8);
    }
    
    /* Info/Warning/Error boxes */
    .warning-box {
        background: rgba(255, 170, 0, 0.1);
        border: 1px solid rgba(255, 170, 0, 0.3);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 12px;
        color: #ffaa00;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(255, 170, 0, 0.1);
    }
    
    .success-box {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 12px;
        color: #00ff88;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
    }
    
    .error-box {
        background: rgba(255, 51, 51, 0.1);
        border: 1px solid rgba(255, 51, 51, 0.3);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 12px;
        color: #ff6666;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(255, 51, 51, 0.1);
    }
    
    .ai-explanation {
        background: rgba(0, 100, 255, 0.08);
        backdrop-filter: blur(10px);
        border-left: 3px solid rgba(0, 200, 255, 0.5);
        padding: 20px;
        border-radius: 10px;
        color: #a0d8ff;
        line-height: 1.7;
        margin: 15px 0;
        font-style: italic;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00ffcc, #0099ff);
        color: #000;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(0, 255, 200, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 30px rgba(0, 255, 200, 0.6);
        transform: translateY(-2px);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(0, 255, 200, 0.1);
        border: 1px solid rgba(0, 255, 200, 0.2);
        color: #00ffcc;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 200, 255, 0.2);
        border-color: rgba(0, 255, 255, 0.5);
    }
    
    /* Text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    
    p, span, text {
        color: #d0d0d0;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "portfolio_data" not in st.session_state:
        st.session_state.portfolio_data = None
    if "assets" not in st.session_state:
        st.session_state.assets = []
    if "error_message" not in st.session_state:
        st.session_state.error_message = None
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    if "stress_mode" not in st.session_state:
        st.session_state.stress_mode = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "token" not in st.session_state:
        st.session_state.token = None
    if "workspace_tab" not in st.session_state:
        st.session_state.workspace_tab = "Dashboard"


def login_user(username: str, password: str) -> tuple[bool, dict | str]:
    """Authenticate user against backend auth API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=5,
        )
        if response.status_code == 200:
            return True, response.json()
        detail = response.json().get("detail", "Invalid username or password")
        return False, detail
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to auth backend at http://127.0.0.1:8002."
    except Exception as exc:
        return False, f"Login failed: {exc}"


def signup_user(username: str, email: str, password: str) -> tuple[bool, dict | str]:
    """Register user against backend auth API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/signup",
            json={"username": username, "email": email, "password": password},
            timeout=5,
        )
        if response.status_code == 200:
            return True, response.json()
        detail = response.json().get("detail", "Signup failed")
        return False, detail
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to auth backend at http://127.0.0.1:8002."
    except Exception as exc:
        return False, f"Signup failed: {exc}"


def set_authenticated_user(auth_payload: dict) -> None:
    """Persist authenticated user info in session state."""
    st.session_state.logged_in = True
    st.session_state.username = auth_payload.get("username")
    st.session_state.token = auth_payload.get("access_token")


def logout_user() -> None:
    """Clear authenticated user info from session state."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.token = None


def normalize_weights(assets: list[dict]) -> list[dict]:
    """Normalize weights to sum to 1.0."""
    total = sum(asset["weight"] for asset in assets if asset["weight"] > 0)
    if total == 0:
        return assets
    return [
        {
            "ticker": asset["ticker"],
            "weight": asset["weight"] / total,
        }
        for asset in assets
        if asset["weight"] > 0
    ]


def parse_csv_file(uploaded_file) -> tuple[bool, list[dict] | str]:
    """
    Parse CSV file to extract portfolio data.
    
    Expected CSV format:
    - Column 1: ticker (required)
    - Column 2: weight (required)
    
    Or with headers:
    ticker,weight
    AAPL,0.3
    MSFT,0.3
    ...
    """
    try:
        df = pd.read_csv(uploaded_file)
        
        # Handle different column configurations
        if len(df.columns) < 2:
            return False, "CSV must have at least 2 columns: ticker and weight"
        
        # Try to identify ticker and weight columns
        cols = [col.lower().strip() for col in df.columns]
        
        # Find ticker column
        ticker_col = None
        for col_idx, col in enumerate(cols):
            if "ticker" in col or "symbol" in col or "stock" in col:
                ticker_col = col_idx
                break
        if ticker_col is None:
            ticker_col = 0  # First column as default
        
        # Find weight column
        weight_col = None
        for col_idx, col in enumerate(cols):
            if "weight" in col or "allocation" in col or "percent" in col:
                weight_col = col_idx
                break
        if weight_col is None:
            weight_col = 1  # Second column as default
        
        # Parse data
        assets = []
        for _, row in df.iterrows():
            ticker = str(row.iloc[ticker_col]).strip().upper()
            try:
                weight = float(row.iloc[weight_col])
            except (ValueError, TypeError):
                continue
            
            if ticker and weight > 0:
                assets.append({"ticker": ticker, "weight": weight})
        
        if not assets:
            return False, "No valid ticker-weight pairs found in CSV"
        
        # Normalize weights
        assets = normalize_weights(assets)
        
        return True, assets
        
    except Exception as exc:
        return False, f"Error parsing CSV: {str(exc)}"


def call_backend_api(assets: list[dict]) -> tuple[bool, dict | str]:
    """
    Call the backend API with portfolio data.

    Args:
        assets: List of dicts with 'ticker' and 'weight'.

    Returns:
        Tuple of (success: bool, data: dict | error_message: str)
    """
    # Normalize weights
    normalized_assets = normalize_weights(assets)

    if not normalized_assets:
        return False, "Portfolio must contain at least one asset with weight > 0."

    payload = {"assets": normalized_assets}

    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=30)

        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 400:
            return False, f"Bad Request: {response.json().get('detail', 'Invalid input')}"
        elif response.status_code == 502:
            return False, f"Backend Error: {response.json().get('detail', 'API error')}"
        else:
            return False, f"Unexpected error (HTTP {response.status_code})"

    except requests.exceptions.Timeout:
        return False, "⏱️ Request timed out. Is the backend running at http://127.0.0.1:8002?"
    except requests.exceptions.ConnectionError:
        return False, "❌ Cannot connect to backend. Ensure it's running at http://127.0.0.1:8002"
    except Exception as exc:
        return False, f"Unexpected error: {str(exc)}"


# ============================================================================
# UI BUILDING BLOCKS
# ============================================================================


def render_landing_page():
    """Render MetaCap-style landing page with white text and geometric background."""
    st.markdown(
        """
        <style>
        /* Background with geometric pattern */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a1e24 0%, #0d2d35 50%, #081b24 100%);
            background-attachment: fixed;
        }
        
        /* Geometric background pattern overlay */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(0, 255, 200, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 153, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(0, 255, 136, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        /* Navigation Bar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 25px 60px;
            background: rgba(10, 30, 36, 0.7);
            backdrop-filter: blur(10px);
            margin-bottom: 60px;
            border-bottom: 1px solid rgba(0, 255, 200, 0.1);
        }
        
        .nav-logo {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #00ffcc, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
        }
        
        .nav-center {
            display: flex;
            gap: 50px;
            font-size: 14px;
            color: #ffffff;
            flex: 1;
            justify-content: center;
            font-weight: 500;
        }
        
        .nav-center a {
            color: #ffffff;
            text-decoration: none;
            transition: color 0.3s;
            font-weight: 500;
        }
        
        .nav-center a:hover {
            color: #00ffcc;
        }
        
        .nav-right {
            display: flex;
            gap: 20px;
            align-items: center;
            font-size: 13px;
        }
        
        .nav-right a {
            color: #ffffff;
            text-decoration: none;
            transition: color 0.3s;
            font-weight: 500;
        }
        
        .nav-right a:hover {
            color: #00ffcc;
        }
        
        .nav-button {
            border: 1px solid rgba(0, 255, 200, 0.6);
            color: #00ffcc;
            padding: 8px 20px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            background: transparent;
        }
        
        .nav-button:hover {
            border-color: #00ffcc;
            background: rgba(0, 255, 200, 0.15);
        }
        
        /* Hero Section */
        .hero-wrapper {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 80px;
            align-items: center;
            padding: 80px 60px;
            margin-bottom: 120px;
        }
        
        .hero-left h1 {
            font-size: 68px;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 30px;
            color: #ffffff;
            letter-spacing: -2px;
        }
        
        .hero-left h1 span {
            background: linear-gradient(135deg, #00ffcc, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-left p {
            font-size: 16px;
            color: #dddddd;
            line-height: 1.8;
            margin-bottom: 40px;
            font-weight: 400;
        }
        
        .hero-button {
            display: inline-block;
            background: linear-gradient(135deg, #00ffcc, #00ff88);
            color: #081b24;
            padding: 15px 45px;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 0 30px rgba(0, 255, 200, 0.25);
        }
        
        .hero-button:hover {
            box-shadow: 0 0 60px rgba(0, 255, 200, 0.5);
            transform: translateY(-3px);
        }
        
        /* Geometric Shapes */
        .hero-right {
            position: relative;
            height: 500px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .hexagon {
            position: absolute;
            background: linear-gradient(135deg, rgba(0, 255, 200, 0.2), rgba(0, 255, 136, 0.1));
            border: 2px solid rgba(0, 255, 200, 0.4);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            animation: float 6s ease-in-out infinite;
        }
        
        .hexagon:nth-child(1) {
            width: 200px;
            height: 230px;
            left: 0;
            top: 0;
            animation-delay: 0s;
        }
        
        .hexagon:nth-child(2) {
            width: 180px;
            height: 210px;
            right: 0;
            bottom: 40px;
            animation-delay: 1s;
        }
        
        .hexagon:nth-child(3) {
            width: 150px;
            height: 180px;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            animation-delay: 2s;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-25px);
            }
        }
        
        /* Dashboard Section */
        .dashboard-section {
            background: rgba(13, 45, 53, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 200, 0.2);
            border-radius: 15px;
            padding: 50px 60px;
            margin: 0 60px 80px 60px;
        }
        
        .dashboard-section h3 {
            font-size: 20px;
            color: #ffffff;
            margin-bottom: 30px;
            font-weight: 700;
        }
        
        .dashboard-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .dashboard-table th {
            text-align: left;
            padding: 18px 20px;
            border-bottom: 1px solid rgba(0, 255, 200, 0.2);
            color: #ffffff;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        
        .dashboard-table td {
            padding: 14px 20px;
            border-bottom: 1px solid rgba(0, 255, 200, 0.1);
            color: #dddddd;
            font-size: 14px;
        }
        
        .dashboard-table tr:hover {
            background: rgba(0, 255, 200, 0.08);
        }
        
        /* Features Section */
        .features-section {
            padding: 100px 60px;
            text-align: center;
            margin-bottom: 80px;
        }
        
        .features-section h2 {
            font-size: 52px;
            font-weight: 700;
            margin-bottom: 70px;
            color: #ffffff;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
        }
        
        .feature-card {
            background: rgba(13, 45, 53, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 200, 0.2);
            border-radius: 12px;
            padding: 40px 30px;
            transition: all 0.3s;
            text-align: center;
        }
        
        .feature-card:hover {
            border-color: rgba(0, 255, 200, 0.5);
            box-shadow: 0 0 40px rgba(0, 255, 200, 0.2);
            transform: translateY(-5px);
            background: rgba(13, 45, 53, 0.7);
        }
        
        .feature-icon {
            font-size: 45px;
            margin-bottom: 18px;
        }
        
        .feature-card h3 {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #ffffff;
        }
        
        .feature-card p {
            font-size: 14px;
            color: #dddddd;
            line-height: 1.6;
        }
        
        @media (max-width: 768px) {
            .hero-wrapper, .features-grid {
                grid-template-columns: 1fr;
            }
            .hero-left h1 {
                font-size: 42px;
            }
        }
        </style>
        
        <!-- Navigation Bar -->
        <div class='navbar'>
            <div class='nav-logo'>📊 PDMS</div>
            <div class='nav-center'>
                <a href='#'>Portfolio</a>
                <a href='#'>Analytics</a>
                <a href='#'>Insights</a>
                <a href='#'>Docs</a>
            </div>
            <div class='nav-right'>
                <button class='nav-button'>Schedule Demo</button>
            </div>
        </div>
        
        
        """,
        unsafe_allow_html=True,
    )

    hero_left, hero_right = st.columns([1, 1], gap="large")
    with hero_left:
        st.markdown(
            """
            <div class='hero-left'>
                <h1>Optimize Your Portfolio <span>Under Any Market</span></h1>
                <p>Advanced AI-powered analysis with real-time risk metrics, stress testing, and correlation analysis. Diversify confidently with macroeconomic scenarios and hierarchical clustering.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Get Started", key="get_started_btn"):
            st.session_state.page = "login"
            st.rerun()

    with hero_right:
        st.markdown(
            """
            <div class='hero-right'>
                <div class='hexagon'></div>
                <div class='hexagon'></div>
                <div class='hexagon'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <!-- Dashboard Preview Section -->
        <div class='dashboard-section'>
            <h3>📈 Portfolio Analysis Sample</h3>
            <table class='dashboard-table'>
                <thead>
                    <tr>
                        <th>Asset</th>
                        <th>Weight</th>
                        <th>Volatility</th>
                        <th>Correlation</th>
                        <th>Risk Score</th>
                        <th>Diversification</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>AAPL</td>
                        <td>40%</td>
                        <td>28.5%</td>
                        <td>High</td>
                        <td>7.2</td>
                        <td>Moderate</td>
                    </tr>
                    <tr>
                        <td>MSFT</td>
                        <td>30%</td>
                        <td>24.1%</td>
                        <td>High</td>
                        <td>6.8</td>
                        <td>Moderate</td>
                    </tr>
                    <tr>
                        <td>GOOGL</td>
                        <td>30%</td>
                        <td>26.3%</td>
                        <td>High</td>
                        <td>7.1</td>
                        <td>Good</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Features Section -->
        <div class='features-section'>
            <h2>Core Features</h2>
            <div class='features-grid'>
                <div class='feature-card'>
                    <div class='feature-icon'>📊</div>
                    <h3>Risk Metrics</h3>
                    <p>Volatility, VaR, CVaR & Drawdown</p>
                </div>
                <div class='feature-card'>
                    <div class='feature-icon'>🔗</div>
                    <h3>Correlation</h3>
                    <p>Hidden relationships analysis</p>
                </div>
                <div class='feature-card'>
                    <div class='feature-icon'>⚡</div>
                    <h3>Stress Testing</h3>
                    <p>Market shock simulation</p>
                </div>
                <div class='feature-card'>
                    <div class='feature-icon'>🎯</div>
                    <h3>Clustering</h3>
                    <p>Smart asset grouping</p>
                </div>
                <div class='feature-card'>
                    <div class='feature-icon'>🤖</div>
                    <h3>AI Insights</h3>
                    <p>Intelligent recommendations</p>
                </div>
                <div class='feature-card'>
                    <div class='feature-icon'>📈</div>
                    <h3>Live Analytics</h3>
                    <p>Interactive visualizations</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_login_page():
    """Render MetaCap-style login page."""
    st.markdown(
        """
        <style>
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #0a1e24 0%, #0d2d35 50%, #081b24 100%);
        }
        
        .login-box {
            background: rgba(13, 45, 53, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 200, 0.2);
            border-radius: 15px;
            padding: 50px 40px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 0 60px rgba(0, 255, 200, 0.1);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .login-logo {
            font-size: 48px;
            margin-bottom: 20px;
        }
        
        .login-title {
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 10px;
        }
        
        .login-subtitle {
            font-size: 14px;
            color: #dddddd;
        }
        
        .login-footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #dddddd;
        }
        
        .login-footer a {
            color: #00ffcc;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        
        .login-footer a:hover {
            color: #00ff88;
        }
        </style>
        
        <div class='login-container'>
            <div class='login-box'>
                <div class='login-header'>
                    <div class='login-logo'>📊</div>
                    <div class='login-title'>Sign In to PDMS</div>
                    <div class='login-subtitle'>Portfolio Diversification Management System</div>
                </div>
                <div class='login-footer'>
                    <p style="margin-bottom: 30px; font-size: 16px; color: #99ddff;">Demo Login Page</p>
                    <p>Email: <strong>demo@pdms.com</strong></p>
                    <p>Password: <strong>demo123</strong></p>
                    <p style="margin-top: 30px; color: #dddddd;">This is a demo interface</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Back button and Login button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Home", key="back_from_login", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    with col2:
        if st.button("Go to Dashboard", key="login_to_dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()


def render_login_page_functional():
    """Render a working login and signup experience."""
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 18% 82%, rgba(24, 192, 145, 0.24), transparent 0 18%),
                radial-gradient(circle at 42% 20%, rgba(54, 255, 210, 0.28), transparent 0 13%),
                radial-gradient(circle at 74% 50%, rgba(107, 255, 184, 0.24), transparent 0 16%),
                radial-gradient(circle at 62% 88%, rgba(38, 231, 162, 0.26), transparent 0 7%),
                linear-gradient(135deg, #0b2e29 0%, #08241f 45%, #041411 100%);
            overflow: hidden;
        }

        .block-container {
            padding-top: 0.25rem !important;
            padding-bottom: 1rem !important;
        }

        .orb {
            position: fixed;
            border-radius: 50%;
            pointer-events: none;
            filter: blur(1px);
            z-index: 0;
        }

        .orb-one {
            width: 230px;
            height: 230px;
            top: 18%;
            left: 33%;
            background: radial-gradient(circle at 35% 30%, rgba(233,255,244,0.9), rgba(63,255,203,0.88) 35%, rgba(17,182,128,0.12) 75%, transparent 100%);
        }

        .orb-two {
            width: 250px;
            height: 250px;
            right: 16%;
            top: 37%;
            background: radial-gradient(circle at 40% 35%, rgba(243,255,246,0.86), rgba(95,255,190,0.88) 32%, rgba(10,148,95,0.15) 72%, transparent 100%);
        }

        .orb-three {
            width: 230px;
            height: 230px;
            left: 18%;
            bottom: 15%;
            background: radial-gradient(circle at 35% 30%, rgba(213,255,228,0.76), rgba(42,214,141,0.82) 32%, rgba(6,97,63,0.24) 70%, transparent 100%);
        }

        .orb-four {
            width: 96px;
            height: 96px;
            right: 33%;
            bottom: 16%;
            background: radial-gradient(circle at 35% 30%, rgba(245,255,249,0.95), rgba(72,255,198,0.92) 40%, rgba(24,169,111,0.18) 78%, transparent 100%);
        }

        .login-title-block {
            text-align: center;
            margin: 16px 0 18px;
        }

        .login-title-block h2 {
            margin: 0;
            font-size: 2.1rem;
            font-weight: 600;
            color: #eef7ff;
            letter-spacing: 0.02em;
        }

        .login-title-block p {
            margin: 10px 0 0;
            color: #c4e9dc;
            font-size: 0.98rem;
        }

        .auth-tabs-spacer {
            height: 14px;
        }

        .auth-meta {
            text-align: center;
            color: #daf6ea;
            font-size: 0.9rem;
            margin-top: 12px;
        }

        .auth-switch {
            text-align: center;
            color: #d5f0e4;
            font-size: 0.95rem;
            margin-top: 10px;
        }

        .auth-switch strong {
            color: #35f1a8;
        }

        .forgot-copy {
            text-align: right;
            color: #dbefe7;
            font-size: 0.86rem;
            margin: -4px 0 10px;
        }

        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            justify-content: center;
            gap: 10px;
            background: transparent;
            margin-bottom: 18px;
            border-bottom: none !important;
            box-shadow: none !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab"] {
            border-radius: 999px;
            border: 1px solid rgba(116, 238, 185, 0.2);
            background: rgba(7, 27, 22, 0.44);
            color: #daf8eb;
            min-width: 132px;
            font-weight: 500;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(43, 216, 146, 0.28), rgba(17, 146, 95, 0.28));
            border-color: rgba(93, 249, 179, 0.46);
            color: #ffffff;
        }

        [data-testid="stTextInput"] input {
            background: linear-gradient(135deg, rgba(25, 205, 138, 0.96), rgba(16, 167, 113, 0.96)) !important;
            border: none !important;
            border-radius: 14px !important;
            color: #eefdf7 !important;
            height: 52px !important;
            padding: 0 16px !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.14) !important;
        }

        [data-testid="stTextInput"] input::placeholder {
            color: rgba(234, 255, 245, 0.8) !important;
        }

        [data-testid="stTextInput"] label p {
            color: #e5fbf2 !important;
            font-size: 0.88rem !important;
        }

        .stButton > button {
            border-radius: 14px !important;
            min-height: 52px !important;
            font-weight: 600 !important;
            border: none !important;
        }

        button[kind="primary"], .stButton > button {
            background: linear-gradient(135deg, #21d88f, #149f68) !important;
            color: #eefdf7 !important;
            box-shadow: 0 12px 30px rgba(27, 188, 122, 0.3) !important;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 0 !important;
            }

            .orb-one, .orb-two, .orb-three {
                opacity: 0.72;
            }
        }
        </style>
        <div class="orb orb-one"></div>
        <div class="orb orb-two"></div>
        <div class="orb orb-three"></div>
        <div class="orb orb-four"></div>
        """,
        unsafe_allow_html=True,
    )

    left_spacer, center_col, right_spacer = st.columns([1.35, 1.0, 1.35])
    with center_col:
        st.markdown(
            """
        <div class='login-title-block'>
            <h2>Sign In</h2>
            <p>Access your portfolio workspace and continue your analysis.</p>
        </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='auth-tabs-spacer'></div>", unsafe_allow_html=True)

        tab_sign_in, tab_sign_up = st.tabs(["Sign In", "Sign Up"])

        with tab_sign_in:
            login_username = st.text_input(
                "Email or Username",
                key="pdms_login_username",
                placeholder="Username or email",
                label_visibility="collapsed",
            )
            login_password = st.text_input(
                "Password",
                key="pdms_login_password",
                placeholder="Password",
                type="password",
                label_visibility="collapsed",
            )
            st.markdown("<div class='forgot-copy'>Forgot password?</div>", unsafe_allow_html=True)
            if st.button("Login", key="pdms_sign_in_btn", use_container_width=True):
                if not login_username or not login_password:
                    st.markdown(
                        "<div class='error-box'>Please enter both username and password.</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    success, result = login_user(login_username, login_password)
                    if success:
                        set_authenticated_user(result)
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.markdown(
                            f"<div class='error-box'>{result}</div>",
                            unsafe_allow_html=True,
                        )
            st.markdown(
                "<div class='auth-switch'>Don't have an account? <strong>Sign up</strong> in the next tab.</div>",
                unsafe_allow_html=True,
            )

        with tab_sign_up:
            signup_username = st.text_input(
                "New Username",
                key="pdms_signup_username",
                placeholder="Username",
                label_visibility="collapsed",
            )
            signup_email = st.text_input(
                "Signup Email",
                key="pdms_signup_email",
                placeholder="Email",
                label_visibility="collapsed",
            )
            signup_password = st.text_input(
                "New Password",
                key="pdms_signup_password",
                placeholder="Password",
                type="password",
                label_visibility="collapsed",
            )
            signup_confirm_password = st.text_input(
                "Confirm Password",
                key="pdms_signup_confirm_password",
                placeholder="Confirm password",
                type="password",
                label_visibility="collapsed",
            )
            if st.button("Create Account", key="pdms_sign_up_btn", use_container_width=True):
                if not signup_username or not signup_email or not signup_password:
                    st.markdown(
                        "<div class='error-box'>Fill in all required fields.</div>",
                        unsafe_allow_html=True,
                    )
                elif signup_password != signup_confirm_password:
                    st.markdown(
                        "<div class='error-box'>Passwords do not match.</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    success, result = signup_user(signup_username, signup_email, signup_password)
                    if success:
                        set_authenticated_user(result)
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.markdown(
                            f"<div class='error-box'>{result}</div>",
                            unsafe_allow_html=True,
                        )
            st.markdown(
                "<div class='auth-meta'>Create an account to unlock the full dashboard.</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='auth-meta'>Demo account example: <strong>demo / demo123</strong></div>",
            unsafe_allow_html=True,
        )

        footer_left, footer_right = st.columns(2)
        with footer_left:
            if st.button("Back", key="back_from_login_v2", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()
        with footer_right:
            if st.button(
                "Dashboard",
                key="login_to_dashboard_v2",
                use_container_width=True,
                disabled=not st.session_state.logged_in,
            ):
                st.session_state.page = "dashboard"
                st.rerun()


def render_portfolio_input_section():
    """Render portfolio input form with dynamic asset rows and CSV upload."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>📝 Configure Your Portfolio</h3>
        """,
        unsafe_allow_html=True,
    )
    
    # CSV Upload Section
    st.markdown("**📤 Upload Portfolio from CSV**")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="CSV should have columns: ticker, weight",
    )

    if uploaded_file is not None:
        success, result = parse_csv_file(uploaded_file)
        if success:
            st.session_state.assets = result
            st.markdown(
                f"""
                <div class='success-box'>
                ✅ Loaded {len(result)} assets from CSV
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class='error-box'>
                ❌ CSV Error: {result}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("**📝 Manual Entry**")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write("**Ticker**")
    with col2:
        st.write("**Weight**")
    with col3:
        st.write("**Action**")

    assets = []
    for i in range(len(st.session_state.assets)):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            ticker = st.text_input(
                "ticker",
                value=st.session_state.assets[i].get("ticker", ""),
                label_visibility="collapsed",
                key=f"ticker_{i}",
            )

        with col2:
            weight = st.number_input(
                "weight",
                value=st.session_state.assets[i].get("weight", 0.25),
                min_value=0.0,
                max_value=1.0,
                step=0.05,
                label_visibility="collapsed",
                key=f"weight_{i}",
            )

        with col3:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.assets.pop(i)
                st.rerun()

        if ticker.strip():
            assets.append({"ticker": ticker.strip().upper(), "weight": weight})

    # Always update session state with valid assets
    st.session_state.assets = assets

    if st.button("➕ Add Asset", key="add_asset"):
        st.session_state.assets.append({"ticker": "", "weight": 0.25})
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    return st.session_state.assets


def render_analyze_button() -> bool:
    """Render the analyze portfolio button."""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        return st.button("🚀 Analyze Portfolio", use_container_width=True)


def render_top_metrics_cards(data: dict):
    """Render 3 premium top metric cards with mini charts."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class='metric-box'>
                <h4 style='margin: 0 0 10px 0;'>Portfolio Volatility</h4>
                <h2 style='color: #00ffcc; margin: 0;'>{:.2%}</h2>
                <p style='font-size: 12px; margin: 10px 0 0 0;'>Annualized Risk</p>
            </div>
            """.format(data.get("metrics", {}).get("volatility", 0)),
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div class='metric-box'>
                <h4 style='margin: 0 0 10px 0;'>Value at Risk (95%)</h4>
                <h2 style='color: #00ffff; margin: 0;'>{:.4f}</h2>
                <p style='font-size: 12px; margin: 10px 0 0 0;'>Max Expected Loss</p>
            </div>
            """.format(data.get("metrics", {}).get("var", 0)),
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            """
            <div class='metric-box'>
                <h4 style='margin: 0 0 10px 0;'>Max Drawdown</h4>
                <h2 style='color: #00ff88; margin: 0;'>{:.2%}</h2>
                <p style='font-size: 12px; margin: 10px 0 0 0;'>Peak-to-Trough</p>
            </div>
            """.format(data.get("metrics", {}).get("max_drawdown", 0)),
            unsafe_allow_html=True,
        )


def render_dashboard_section(data: dict):
    """Render main dashboard with glassmorphic cards."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>📊 Risk Analysis Dashboard</h3>
        """,
        unsafe_allow_html=True,
    )
    
    render_top_metrics_cards(data)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")


def render_clusters_section(data: dict):
    """Render asset clustering analysis with glass card."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>🔗 Asset Clustering</h3>
        """,
        unsafe_allow_html=True,
    )

    clusters = data.get("clusters", {})
    if not clusters:
        st.info("No clustering data available")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Cluster Groups:**")
        for cluster_id, tickers in clusters.items():
            st.markdown(
                f"<p><strong>Cluster {cluster_id}:</strong> {', '.join(tickers)}</p>",
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("**High Correlation Pairs:**")
        high_corr_pairs = data.get("high_correlation_pairs", [])
        if high_corr_pairs:
            for pair in high_corr_pairs:
                ticker_a, ticker_b, corr = pair
                st.markdown(
                    f"<p>🔥 <strong>{ticker_a} ↔ {ticker_b}</strong>: {corr:.4f}</p>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("<p>No high correlations detected</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_diversification_section(data: dict):
    """Render diversification metrics with glass card."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>🎯 Diversification Analysis</h3>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        enb = data.get("diversification", {}).get("enb", 0)
        st.markdown(
            f"""
            <div style='background: rgba(0, 255, 150, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 150, 0.2);'>
                <p style='color: #888; margin: 0;'>Effective Number of Bets</p>
                <h3 style='color: #00ff88; margin: 10px 0 0 0;'>{enb:.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        div_score = data.get("diversification", {}).get("diversification_score", 0)
        st.markdown(
            f"""
            <div style='background: rgba(0, 200, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 200, 255, 0.2);'>
                <p style='color: #888; margin: 0;'>Diversification Score</p>
                <h3 style='color: #00ddff; margin: 10px 0 0 0;'>{div_score:.4f}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    cluster_conc = data.get("diversification", {}).get("cluster_concentration", {})
    if cluster_conc:
        st.markdown("**Cluster Concentration by Weight**")
        conc_df_data = [
            {"Cluster": k.replace("cluster_", "Cluster "), "Weight": v}
            for k, v in cluster_conc.items()
        ]
        conc_df = pd.DataFrame(conc_df_data)
        
        fig = px.bar(
            conc_df,
            x="Cluster",
            y="Weight",
            color="Weight",
            color_continuous_scale=[[0, "#00ff88"], [1, "#ff6666"]],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#fff"),
            hovermode="x unified",
        )
        fig.update_traces(marker_line_color="rgba(0,255,200,0.3)")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_stress_test_section(data: dict):
    """Render stress test comparison with glass card."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>⚠️ Stress Test Analysis</h3>
        """,
        unsafe_allow_html=True,
    )

    stress = data.get("stress", {})
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style='background: rgba(0, 200, 100, 0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(0, 200, 100, 0.2);'>
                <p style='color: #888; font-size: 11px; margin: 0;'>Normal VaR</p>
                <p style='color: #00ff88; margin: 5px 0 0 0; font-weight: 600;'>{stress.get('normal_var', 0):.4f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style='background: rgba(255, 100, 100, 0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 100, 100, 0.2);'>
                <p style='color: #888; font-size: 11px; margin: 0;'>Stressed VaR</p>
                <p style='color: #ff6666; margin: 5px 0 0 0; font-weight: 600;'>{stress.get('stressed_var', 0):.4f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style='background: rgba(0, 200, 100, 0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(0, 200, 100, 0.2);'>
                <p style='color: #888; font-size: 11px; margin: 0;'>Normal CVaR</p>
                <p style='color: #00ff88; margin: 5px 0 0 0; font-weight: 600;'>{stress.get('normal_cvar', 0):.4f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div style='background: rgba(255, 100, 100, 0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 100, 100, 0.2);'>
                <p style='color: #888; font-size: 11px; margin: 0;'>Stressed CVaR</p>
                <p style='color: #ff6666; margin: 5px 0 0 0; font-weight: 600;'>{stress.get('stressed_cvar', 0):.4f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Stress comparison chart
    stress_data = pd.DataFrame(
        {
            "Metric": ["VaR (95%)", "CVaR (95%)"],
            "Normal": [stress.get("normal_var", 0), stress.get("normal_cvar", 0)],
            "Stressed": [stress.get("stressed_var", 0), stress.get("stressed_cvar", 0)],
        }
    )

    fig = px.bar(
        stress_data,
        x="Metric",
        y=["Normal", "Stressed"],
        barmode="group",
        color_discrete_map={"Normal": "#00ff88", "Stressed": "#ff6666"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fff"),
        hovermode="x unified",
        legend=dict(x=0.7, y=1),
    )
    fig.update_traces(marker_line_color="rgba(255,255,255,0.2)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_ai_explanation_section(data: dict):
    """Render AI-generated portfolio explanation."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>🤖 AI-Powered Insights</h3>
        """,
        unsafe_allow_html=True,
    )

    ai_explanation = data.get("ai_explanation", "")
    if ai_explanation:
        st.markdown(
            f"""
            <div class='ai-explanation'>
            {ai_explanation}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<p style='color: #888;'>AI insights not available. Check Groq API configuration.</p>",
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================


def plot_correlation_heatmap(data: dict):
    """Create interactive correlation matrix heatmap with glow effect."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>🔥 Correlation Heatmap</h3>
        """,
        unsafe_allow_html=True,
    )

    import numpy as np

    corr_matrix_dict = data.get("correlation_matrix", {})
    if not corr_matrix_dict:
        st.warning("Correlation matrix not available")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    try:
        df_corr = pd.DataFrame(corr_matrix_dict)
    except Exception as e:
        st.warning(f"Could not parse correlation matrix: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    fig = go.Figure(
        data=go.Heatmap(
            z=df_corr.values,
            x=df_corr.columns,
            y=df_corr.index,
            colorscale="Turbo",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=np.round(df_corr.values, 3),
            texttemplate="%{text:.3f}",
            textfont={"size": 10, "color": "#fff"},
            colorbar=dict(title="Correlation", tickfont=dict(color="#fff")),
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
        font=dict(color="#fff"),
        height=500,
        hovermode="closest",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def plot_risk_contribution(data: dict):
    """Create risk contribution bar chart by asset with glow effect."""
    st.markdown(
        """
        <div class='glass-card'>
            <h3 class='glow-text'>📊 Risk Contribution Analysis</h3>
        """,
        unsafe_allow_html=True,
    )

    assets_info = data.get("assets", [])
    volatility = data.get("volatility", 0.1)

    if not assets_info:
        st.warning("Asset information not available")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    tickers = [asset.get("ticker", "Unknown") for asset in assets_info]
    weights = [asset.get("weight", 0) for asset in assets_info]
    risk_contrib = [w * volatility for w in weights]

    df_risk = pd.DataFrame(
        {"Ticker": tickers, "Risk Contribution": risk_contrib, "Weight": weights}
    )

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "bar"}, {"type": "pie"}]],
        subplot_titles=("Risk Contribution by Asset", "Weight Distribution"),
    )

    fig.add_trace(
        go.Bar(
            x=df_risk["Ticker"],
            y=df_risk["Risk Contribution"],
            name="Risk Contribution",
            marker=dict(
                color="rgba(0, 200, 255, 0.8)",
                line=dict(color="rgba(0,255,200,0.5)", width=2),
            ),
        ),
        row=1,
        col=1,
    )

    # Generate colors for pie chart - list of colors from Turbo palette
    import numpy as np
    norm_weights = (df_risk["Weight"] - df_risk["Weight"].min()) / (df_risk["Weight"].max() - df_risk["Weight"].min() + 1e-10)
    turbo_colors = ["rgb(64,224,208)", "rgb(0,191,255)", "rgb(30,144,255)"]
    colors = [turbo_colors[i % len(turbo_colors)] for i in range(len(df_risk))]

    fig.add_trace(
        go.Pie(
            labels=df_risk["Ticker"],
            values=df_risk["Weight"],
            name="Weight",
            marker=dict(
                colors=colors,
                line=dict(color="rgba(255,255,255,0.2)", width=2),
            ),
        ),
        row=1,
        col=2,
    )

    fig.update_xaxes(title_text="Asset", row=1, col=1, title_font=dict(color="#fff"), tickfont=dict(color="#fff"))
    fig.update_yaxes(title_text="Risk Contribution", row=1, col=1, title_font=dict(color="#fff"), tickfont=dict(color="#fff"))

    fig.update_layout(
        height=500,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
        font=dict(color="#fff"),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def apply_dashboard_workspace_styles():
    """Apply multi-panel control-center styling for the dashboard view."""
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 8% 8%, rgba(18, 255, 178, 0.11), transparent 0 18%),
                radial-gradient(circle at 92% 92%, rgba(4, 165, 109, 0.14), transparent 0 20%),
                linear-gradient(135deg, #031612 0%, #071f1a 45%, #020907 100%);
        }

        .dashboard-shell {
            background: rgba(6, 17, 14, 0.88);
            border: 1px solid rgba(54, 148, 112, 0.18);
            border-radius: 30px;
            padding: 14px;
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.33);
        }

        .dashboard-sidebar {
            background: linear-gradient(180deg, rgba(11, 45, 33, 0.95), rgba(8, 28, 22, 0.95));
            border: 1px solid rgba(72, 188, 139, 0.15);
            border-radius: 24px;
            padding: 24px 18px;
            min-height: 82vh;
        }

        .dashboard-brand {
            color: #33f0ab;
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .dashboard-date {
            color: #8fbea9;
            font-size: 0.82rem;
            margin-bottom: 22px;
        }

        .dashboard-profile {
            background: rgba(21, 66, 49, 0.5);
            border: 1px solid rgba(92, 214, 161, 0.18);
            border-radius: 22px;
            padding: 18px 14px;
            text-align: center;
            margin-bottom: 22px;
        }

        .dashboard-avatar {
            width: 78px;
            height: 78px;
            border-radius: 50%;
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at 30% 30%, #9bffe0, #1acd8b 58%, #0a5f42 100%);
            color: #052018;
            font-size: 1.6rem;
            font-weight: 700;
            box-shadow: 0 0 30px rgba(52, 236, 166, 0.28);
        }

        .dashboard-profile-name {
            color: #f0fff8;
            font-weight: 600;
        }

        .dashboard-profile-sub {
            color: #88b7a3;
            font-size: 0.82rem;
        }

        .nav-group {
            margin-top: 10px;
        }

        .nav-item {
            padding: 12px 14px;
            margin-bottom: 8px;
            border-radius: 16px;
            color: #d4f6e6;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid transparent;
            font-weight: 500;
        }

        .nav-item.active {
            background: linear-gradient(135deg, rgba(34, 213, 143, 0.18), rgba(19, 96, 66, 0.22));
            border-color: rgba(95, 242, 175, 0.28);
            color: #35f1a8;
        }

        .workspace-main {
            padding: 10px 8px 10px 2px;
        }

        .workspace-topbar {
            background: rgba(8, 22, 18, 0.75);
            border: 1px solid rgba(70, 175, 131, 0.14);
            border-radius: 22px;
            padding: 16px 18px;
            margin-bottom: 16px;
        }

        .workspace-title {
            color: #f2fff8;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0;
        }

        .workspace-subtitle {
            color: #86b7a1;
            font-size: 0.88rem;
            margin-top: 4px;
        }

        .panel-card {
            background: linear-gradient(180deg, rgba(10, 27, 21, 0.88), rgba(7, 18, 15, 0.92));
            border: 1px solid rgba(73, 179, 135, 0.12);
            border-radius: 22px;
            padding: 16px 18px;
            margin-bottom: 16px;
            box-shadow: inset 0 1px 0 rgba(120, 255, 207, 0.04);
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .workspace-main [data-testid="column"] > div {
            height: 100%;
        }

        .workspace-main .stButton > button,
        .workspace-main .stDownloadButton > button {
            width: 100%;
        }

        .panel-title {
            color: #ecfff5;
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 6px;
        }

        .panel-caption {
            color: #82ae9a;
            font-size: 0.82rem;
            margin-bottom: 12px;
        }

        .mini-metric {
            background: linear-gradient(180deg, rgba(20, 64, 48, 0.65), rgba(10, 28, 22, 0.85));
            border: 1px solid rgba(83, 206, 154, 0.14);
            border-radius: 18px;
            padding: 16px;
            min-height: 118px;
        }

        .mini-metric-label {
            color: #8bb8a4;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .mini-metric-value {
            color: #f1fff8;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 6px 0;
        }

        .mini-metric-sub {
            color: #65eba9;
            font-size: 0.82rem;
        }

        .pill-stat {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(35, 221, 148, 0.12);
            color: #7ef4bc;
            font-size: 0.78rem;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_correlation_heatmap_figure(data: dict) -> go.Figure | None:
    """Build correlation heatmap figure without surrounding UI wrappers."""
    import numpy as np

    corr_matrix_dict = data.get("correlation_matrix", {})
    if not corr_matrix_dict:
        return None

    try:
        df_corr = pd.DataFrame(corr_matrix_dict)
    except Exception:
        return None

    fig = go.Figure(
        data=go.Heatmap(
            z=df_corr.values,
            x=df_corr.columns,
            y=df_corr.index,
            colorscale=[
                [0.0, "#04110d"],
                [0.25, "#0e4f38"],
                [0.5, "#1ea36f"],
                [0.75, "#47efab"],
                [1.0, "#d9ffef"],
            ],
            zmin=-1,
            zmax=1,
            zmid=0,
            text=np.round(df_corr.values, 2),
            texttemplate="%{text}",
            textfont={"color": "#ebfff6", "size": 10},
            colorbar=dict(title="Corr", tickfont=dict(color="#dffcef")),
        )
    )
    fig.update_layout(
        height=360,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ecfff6"),
    )
    return fig


def create_risk_contribution_figure(data: dict) -> go.Figure | None:
    """Build risk contribution visualization without wrapper UI."""
    assets_info = data.get("assets", [])
    volatility = data.get("metrics", {}).get("volatility", 0.1)
    if not assets_info:
        return None

    tickers = [asset.get("ticker", "Unknown") for asset in assets_info]
    weights = [asset.get("weight", 0) for asset in assets_info]
    risk_contrib = [w * volatility for w in weights]
    df_risk = pd.DataFrame(
        {"Ticker": tickers, "Risk Contribution": risk_contrib, "Weight": weights}
    )

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "bar"}, {"type": "pie"}]],
        subplot_titles=("Risk Contribution", "Weight Mix"),
    )
    fig.add_trace(
        go.Bar(
            x=df_risk["Ticker"],
            y=df_risk["Risk Contribution"],
            marker=dict(color="#20d58d", line=dict(color="#9fffd7", width=1.5)),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Pie(
            labels=df_risk["Ticker"],
            values=df_risk["Weight"],
            marker=dict(
                colors=["#103e2f", "#16885d", "#1bc37f", "#67efb4", "#bdfbe0"],
                line=dict(color="rgba(255,255,255,0.15)", width=1),
            ),
            hole=0.45,
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        height=320,
        margin=dict(l=6, r=6, t=36, b=6),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#effff7"),
    )
    return fig


def create_stress_figure(data: dict) -> go.Figure:
    """Build grouped stress comparison chart."""
    stress = data.get("stress", {})
    stress_data = pd.DataFrame(
        {
            "Metric": ["VaR", "CVaR"],
            "Normal": [stress.get("normal_var", 0), stress.get("normal_cvar", 0)],
            "Stressed": [stress.get("stressed_var", 0), stress.get("stressed_cvar", 0)],
        }
    )
    fig = px.bar(
        stress_data,
        x="Metric",
        y=["Normal", "Stressed"],
        barmode="group",
        color_discrete_map={"Normal": "#1bd58d", "Stressed": "#72ffbf"},
    )
    fig.update_layout(
        height=300,
        margin=dict(l=6, r=6, t=10, b=6),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#effff7"),
        legend=dict(orientation="h", y=1.12, x=0.52),
    )
    return fig


def create_cluster_bar_figure(data: dict) -> go.Figure | None:
    """Build cluster concentration bar chart."""
    cluster_conc = data.get("diversification", {}).get("cluster_concentration", {})
    if not cluster_conc:
        return None

    conc_df = pd.DataFrame(
        [
            {"Cluster": key.replace("cluster_", "Cluster "), "Weight": value}
            for key, value in cluster_conc.items()
        ]
    )
    fig = px.bar(
        conc_df,
        x="Cluster",
        y="Weight",
        color="Weight",
        color_continuous_scale=[[0, "#0f3f2f"], [0.5, "#1fbb79"], [1, "#a5ffd7"]],
    )
    fig.update_layout(
        height=280,
        margin=dict(l=6, r=6, t=6, b=6),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        font=dict(color="#effff7"),
    )
    return fig


def create_radar_figure(data: dict) -> go.Figure:
    """Build radar summary figure from portfolio metrics."""
    metrics = data.get("metrics", {})
    stress = data.get("stress", {})
    diversification = data.get("diversification", {})

    volatility = min(abs(metrics.get("volatility", 0)) / 0.5, 1.0)
    var_score = min(abs(metrics.get("var", 0)) / 0.08, 1.0)
    cvar_score = min(abs(metrics.get("cvar", 0)) / 0.1, 1.0)
    drawdown = min(abs(metrics.get("max_drawdown", 0)) / 0.35, 1.0)
    stress_gap = abs(stress.get("stressed_cvar", 0) - stress.get("normal_cvar", 0))
    stress_score = min(stress_gap / 0.08, 1.0)
    diversity = min(max(diversification.get("diversification_score", 0), 0), 1.0)

    categories = [
        "Volatility",
        "VaR",
        "CVaR",
        "Drawdown",
        "Stress",
        "Diversity",
    ]
    values = [volatility, var_score, cvar_score, drawdown, stress_score, diversity]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            line=dict(color="#39f2ac", width=2),
            fillcolor="rgba(57, 242, 172, 0.22)",
        )
    )
    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor="rgba(130, 205, 172, 0.15)",
                tickfont=dict(color="#d6fff0"),
            ),
            angularaxis=dict(
                gridcolor="rgba(130, 205, 172, 0.14)",
                tickfont=dict(color="#eafff6", size=11),
            ),
        ),
        showlegend=False,
    )
    return fig


def render_dashboard_workspace(assets: list[dict]):
    """Render the redesigned multi-panel dashboard workspace."""
    apply_dashboard_workspace_styles()
    data = st.session_state.portfolio_data
    tab_options = ["Home", "Dashboard", "Portfolio", "Stress Lab", "AI Insights"]
    selected_tab = st.session_state.workspace_tab

    if selected_tab not in tab_options:
        selected_tab = "Dashboard"
        st.session_state.workspace_tab = selected_tab

    tab_subtitles = {
        "Home": "Overview of your workspace and latest portfolio status.",
        "Dashboard": "Portfolio monitoring, diversification, and stress analysis in one grid.",
        "Portfolio": "Build and analyze your portfolio allocations and correlations.",
        "Stress Lab": "Inspect downside behavior under stressed market assumptions.",
        "AI Insights": "Review generated portfolio narrative and export analysis artifacts.",
    }

    st.markdown("<div class='dashboard-shell'>", unsafe_allow_html=True)
    shell_left, shell_right = st.columns([0.9, 3.3], gap="medium")

    with shell_left:
        st.markdown(
            f"""
            <div class='dashboard-sidebar'>
                <div class='dashboard-brand'>Portfolio OS</div>
                <div class='dashboard-date'>Control Center</div>
                <div class='dashboard-profile'>
                    <div class='dashboard-avatar'>{(st.session_state.username or 'U')[:1].upper()}</div>
                    <div class='dashboard-profile-name'>{st.session_state.username or 'Analyst'}</div>
                    <div class='dashboard-profile-sub'>Risk workspace</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for tab in tab_options:
            if st.button(
                tab,
                key=f"workspace_tab_{tab}",
                use_container_width=True,
                type="primary" if selected_tab == tab else "secondary",
            ):
                st.session_state.workspace_tab = tab
                st.rerun()

        if st.button("Logout", key="workspace_logout", use_container_width=True):
            logout_user()
            st.session_state.page = "landing"
            st.rerun()

    with shell_right:
        st.markdown("<div class='workspace-main'>", unsafe_allow_html=True)
        top_left, top_mid, top_right = st.columns([2.4, 1.2, 0.9], gap="medium")
        with top_left:
            st.markdown(
                f"""
                <div class='workspace-topbar'>
                    <div class='workspace-title'>{selected_tab}</div>
                    <div class='workspace-subtitle'>{tab_subtitles[selected_tab]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with top_mid:
            st.markdown(
                """
                <div class='workspace-topbar'>
                    <div class='panel-title'>Search</div>
                    <div class='panel-caption'>Quick lookup and navigation</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with top_right:
            st.markdown(
                """
                <div class='workspace-topbar'>
                    <div class='panel-title'>Status</div>
                    <div class='panel-caption'>Live session</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if selected_tab in {"Dashboard", "Portfolio"}:
            input_col, insight_col = st.columns([2.0, 1.0], gap="medium")
            with input_col:
                assets = render_portfolio_input_section()
                st.markdown(
                    """
                    <div class='panel-card'>
                        <div class='panel-title'>Run Analysis</div>
                        <div class='panel-caption'>Submit the current portfolio to refresh all dashboard modules.</div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Analyze Portfolio", key="workspace_analyze", use_container_width=True):
                    success, result = call_backend_api(assets)
                    if success:
                        st.session_state.portfolio_data = result
                        st.session_state.error_message = None
                    else:
                        st.session_state.error_message = result
                        st.session_state.portfolio_data = None
                st.markdown("</div>", unsafe_allow_html=True)
            with insight_col:
                st.markdown(
                    """
                    <div class='panel-card'>
                        <div class='panel-title'>Workspace Controls</div>
                        <div class='panel-caption'>Core assumptions used by the analytics engine.</div>
                        <div class='pill-stat'>Confidence 95%</div>
                        <div class='pill-stat'>Period 1Y</div>
                        <div class='pill-stat'>Source Yahoo Finance</div>
                        <div class='pill-stat'>Mode Historical</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.session_state.error_message:
                    st.markdown(
                        f"<div class='panel-card'><div class='panel-title'>Alert</div><div class='panel-caption'>{st.session_state.error_message}</div></div>",
                        unsafe_allow_html=True,
                    )
                elif data is None:
                    st.markdown(
                        """
                        <div class='panel-card'>
                            <div class='panel-title'>Ready To Analyze</div>
                            <div class='panel-caption'>Run an analysis to populate the metric grid, charts, clustering panel, and AI insight modules.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        elif selected_tab == "Home":
            st.markdown(
                """
                <div class='panel-card'>
                    <div class='panel-title'>Welcome</div>
                    <div class='panel-caption'>Use Portfolio tab to upload assets and run a fresh analysis. Dashboard tab shows the complete multi-panel view.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class='panel-card'>
                    <div class='panel-title'>Focused View</div>
                    <div class='panel-caption'>This tab highlights a subset of modules from your latest analysis output.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if data and "metrics" in data:
            if selected_tab in {"Home", "Dashboard", "Portfolio", "Stress Lab"}:
                metric_cols = st.columns(4, gap="medium")
                metric_specs = [
                    ("Volatility", f"{data['metrics'].get('volatility', 0):.2%}", "Annualized risk"),
                    ("VaR 95%", f"{data['metrics'].get('var', 0):.4f}", "Downside threshold"),
                    ("CVaR 95%", f"{data['metrics'].get('cvar', 0):.4f}", "Tail loss average"),
                    ("Max Drawdown", f"{data['metrics'].get('max_drawdown', 0):.2%}", "Peak-to-trough"),
                ]
                for col, (label, value, sub) in zip(metric_cols, metric_specs):
                    with col:
                        st.markdown(
                            f"""
                            <div class='mini-metric'>
                                <div class='mini-metric-label'>{label}</div>
                                <div class='mini-metric-value'>{value}</div>
                                <div class='mini-metric-sub'>{sub}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            if selected_tab in {"Dashboard", "Portfolio"}:
                top_cards_left, top_cards_right = st.columns(2, gap="medium")

                with top_cards_left:
                    st.markdown("<div class='panel-card'><div class='panel-title'>Clusters & Correlations</div><div class='panel-caption'>Concentration pockets and pair relationships.</div>", unsafe_allow_html=True)
                    clusters = data.get("clusters", {})
                    for cluster_id, tickers in clusters.items():
                        st.markdown(f"<div class='pill-stat'>Cluster {cluster_id}: {', '.join(tickers)}</div>", unsafe_allow_html=True)
                    high_corr_pairs = data.get("high_correlation_pairs", [])
                    if high_corr_pairs:
                        st.dataframe(
                            pd.DataFrame(high_corr_pairs, columns=["Asset A", "Asset B", "Correlation"]),
                            use_container_width=True,
                            hide_index=True,
                        )
                    else:
                        st.caption("No high-correlation pairs above threshold.")
                    st.markdown("</div>", unsafe_allow_html=True)

                with top_cards_right:
                    st.markdown("<div class='panel-card'><div class='panel-title'>Diversification</div><div class='panel-caption'>Effective number of bets and cluster concentration.</div>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='pill-stat'>ENB {data.get('diversification', {}).get('enb', 0):.2f}</div>"
                        f"<div class='pill-stat'>Score {data.get('diversification', {}).get('diversification_score', 0):.2f}</div>",
                        unsafe_allow_html=True,
                    )
                    cluster_fig = create_cluster_bar_figure(data)
                    if cluster_fig is not None:
                        st.plotly_chart(cluster_fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with st.container():
                    st.markdown("<div class='panel-card'><div class='panel-title'>Correlation Matrix</div><div class='panel-caption'>Cross-asset dependency view.</div>", unsafe_allow_html=True)
                    heatmap_fig = create_correlation_heatmap_figure(data)
                    if heatmap_fig is not None:
                        st.plotly_chart(heatmap_fig, use_container_width=True)
                    else:
                        st.info("Correlation matrix not available.")
                    st.markdown("</div>", unsafe_allow_html=True)

            if selected_tab in {"Dashboard", "Stress Lab"}:
                lower_left, lower_right = st.columns([1.15, 0.85], gap="medium")
                with lower_left:
                    st.markdown("<div class='panel-card'><div class='panel-title'>Risk Contribution</div><div class='panel-caption'>Asset exposure versus total portfolio risk.</div>", unsafe_allow_html=True)
                    risk_fig = create_risk_contribution_figure(data)
                    if risk_fig is not None:
                        st.plotly_chart(risk_fig, use_container_width=True)
                    else:
                        st.info("Risk contribution not available.")
                    st.markdown("</div>", unsafe_allow_html=True)
                with lower_right:
                    st.markdown("<div class='panel-card'><div class='panel-title'>Stress Comparison</div><div class='panel-caption'>Normal versus stressed tail risk.</div>", unsafe_allow_html=True)
                    st.plotly_chart(create_stress_figure(data), use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with st.container():
                    st.markdown("<div class='panel-card'><div class='panel-title'>Portfolio Radar</div><div class='panel-caption'>Normalized view of portfolio health dimensions.</div>", unsafe_allow_html=True)
                    st.plotly_chart(create_radar_figure(data), use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            if selected_tab in {"Dashboard", "AI Insights"}:
                final_left, final_right = st.columns([1.2, 0.8], gap="medium")
                with final_left:
                    st.markdown("<div class='panel-card'><div class='panel-title'>AI Insights</div><div class='panel-caption'>Natural-language explanation of current risk posture.</div>", unsafe_allow_html=True)
                    ai_text = data.get("ai_explanation", "AI insights unavailable.")
                    st.markdown(f"<div class='ai-explanation'>{ai_text}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                with final_right:
                    st.markdown("<div class='panel-card'><div class='panel-title'>Export & Raw Data</div><div class='panel-caption'>Download the latest analysis or inspect the payload.</div>", unsafe_allow_html=True)
                    json_str = json.dumps(data, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_str,
                        file_name="portfolio_analysis.json",
                        mime="application/json",
                        use_container_width=True,
                        key="workspace_download_json",
                    )
                    with st.expander("Open raw response"):
                        st.json(data)
                    st.markdown("</div>", unsafe_allow_html=True)
        elif selected_tab != "Home":
            st.markdown(
                """
                <div class='panel-card'>
                    <div class='panel-title'>No Analysis Data Yet</div>
                    <div class='panel-caption'>Run an analysis from the Portfolio tab to populate this view.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    """Main application - Landing page, Login page, or dashboard workspace."""
    initialize_session_state()

    if st.session_state.page == "landing":
        render_landing_page()
    elif st.session_state.page == "login":
        render_login_page_functional()
    else:
        if not st.session_state.logged_in:
            st.session_state.page = "login"
            st.rerun()
        render_dashboard_workspace(st.session_state.assets)


if __name__ == "__main__":
    main()
