"""
ARAIA - Portfolio Risk Analyzer Landing Page
Claude-inspired modern design with sleek interface
"""

import streamlit as st
import requests

# Configure page with dark theme
st.set_page_config(
    page_title="ARAIA",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8002"

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.token = None

# Modern CSS styling (Claude-inspired)
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Header Styling */
    .header-container {
        text-align: center;
        padding: 80px 20px 40px;
        margin-bottom: 40px;
    }
    
    .logo {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 16px;
        letter-spacing: -2px;
    }
    
    .tagline {
        font-size: 20px;
        color: #94a3b8;
        font-weight: 400;
        margin-bottom: 40px;
    }
    
    /* Auth Container */
    .auth-container {
        max-width: 480px;
        margin: 0 auto;
        padding: 48px;
        background: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(51, 65, 85, 0.5);
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Input Styling */
    [data-testid="textInputRootElement"] input,
    [data-testid="stTextInput"] input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1.5px solid rgba(51, 65, 85, 0.6) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        padding: 14px 18px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="textInputRootElement"] input:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
        background-color: rgba(15, 23, 42, 0.95) !important;
    }
    
    /* Button Styling */
    [data-testid="baseButton-primary"] button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        width: 100% !important;
        height: 48px !important;
        margin-top: 8px !important;
    }
    
    [data-testid="baseButton-primary"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px rgba(14, 165, 233, 0.4) !important;
    }
    
    /* Tab Styling */
    [role="tablist"] {
        border-bottom: 1px solid rgba(51, 65, 85, 0.5) !important;
        margin-bottom: 32px !important;
    }
    
    [role="tab"] {
        color: #94a3b8 !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    [role="tab"][aria-selected="true"] {
        color: #0ea5e9 !important;
        border-bottom: 2px solid #0ea5e9 !important;
    }
    
    /* Messages */
    .success-message {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 8px;
        padding: 14px;
        color: #86efac;
        margin: 16px 0;
        font-size: 14px;
    }
    
    .error-message {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 14px;
        color: #fca5a5;
        margin: 16px 0;
        font-size: 14px;
    }
    
    /* Features Grid */
    .features-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 28px;
        margin-top: 80px;
        padding: 60px 40px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .feature-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(51, 65, 85, 0.3);
        border-radius: 14px;
        padding: 32px;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-6px);
        border-color: rgba(14, 165, 233, 0.4);
        background: rgba(30, 41, 59, 0.8);
        box-shadow: 0 12px 32px rgba(14, 165, 233, 0.1);
    }
    
    .feature-icon {
        font-size: 40px;
        margin-bottom: 16px;
    }
    
    .feature-title {
        font-size: 17px;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Welcome State */
    .welcome-section {
        text-align: center;
        padding: 100px 40px;
    }
    
    .welcome-title {
        font-size: 36px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 12px;
    }
    
    .welcome-subtitle {
        font-size: 18px;
        color: #94a3b8;
        margin-bottom: 48px;
    }
    
    .demo-badge {
        display: inline-block;
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(14, 165, 233, 0.3);
        color: #0ea5e9;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 12px;
        margin-top: 24px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


def login_user(username: str, password: str) -> bool:
    """Attempt to login user."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        return False


def signup_user(username: str, email: str, password: str) -> bool:
    """Attempt to register new user."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/signup",
            json={"username": username, "email": email, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.logged_in = True
            st.session_state.username = data["username"]
            st.session_state.token = data["access_token"]
            return True
        return False
    except Exception:
        return False


def logout_user():
    """Logout current user."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.token = None


# Main app logic
if st.session_state.logged_in:
    # Logged in state
    st.markdown("""<div class="welcome-section">""", unsafe_allow_html=True)
    st.markdown(f'<div class="welcome-title">Welcome back, {st.session_state.username}! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Your portfolio analysis awaits</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            if st.button("📊 Dashboard", use_container_width=True, key="goto_dash"):
                try:
                    st.switch_page("pages/dashboard.py")
                except:
                    pass
        with subcol2:
            if st.button("🚪 Logout", use_container_width=True, key="logout"):
                logout_user()
                st.rerun()
    
    st.markdown("""</div>""", unsafe_allow_html=True)

else:
    # Not logged in state
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    
    with col_center:
        # Header
        st.markdown('<div class="header-container">', unsafe_allow_html=True)
        st.markdown('<div class="logo">ARAIA</div>', unsafe_allow_html=True)
        st.markdown('<div class="tagline">Portfolio Risk Analyzer</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auth Container
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        with tab1:
            st.markdown("##### Sign in to your account")
            login_user_input = st.text_input("Username", placeholder="Enter your username", key="login_username", label_visibility="collapsed")
            login_pass_input = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password", label_visibility="collapsed")
            
            if st.button("Sign In", use_container_width=True, key="sign_in_btn", type="primary"):
                if not login_user_input or not login_pass_input:
                    st.markdown('<div class="error-message">⚠️ Please enter both username and password</div>', unsafe_allow_html=True)
                elif login_user(login_user_input, login_pass_input):
                    # Fetch user data after login
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/auth/login",
                            json={"username": login_user_input, "password": login_pass_input},
                            timeout=5
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.logged_in = True
                            st.session_state.username = data["username"]
                            st.session_state.token = data["access_token"]
                    except:
                        pass
                    st.markdown('<div class="success-message">✓ Signed in successfully!</div>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown('<div class="error-message">✗ Invalid credentials</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="demo-badge">💡 Try: demo / demo123</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown("##### Create a new account")
            signup_user_input = st.text_input("Username", placeholder="Choose a username", key="signup_username", label_visibility="collapsed")
            signup_email_input = st.text_input("Email", placeholder="Enter your email", key="signup_email", label_visibility="collapsed")
            signup_pass_input = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password", label_visibility="collapsed")
            signup_pass_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="signup_confirm", label_visibility="collapsed")
            
            if st.button("Create Account", use_container_width=True, key="create_account_btn", type="primary"):
                if not signup_user_input or not signup_email_input or not signup_pass_input:
                    st.markdown('<div class="error-message">⚠️ Fill in all fields</div>', unsafe_allow_html=True)
                elif signup_pass_input != signup_pass_confirm:
                    st.markdown('<div class="error-message">✗ Passwords do not match</div>', unsafe_allow_html=True)
                elif len(signup_pass_input) < 6:
                    st.markdown('<div class="error-message">✗ Password must be 6+ characters</div>', unsafe_allow_html=True)
                elif len(signup_user_input) < 3:
                    st.markdown('<div class="error-message">✗ Username must be 3+ characters</div>', unsafe_allow_html=True)
                elif signup_user(signup_user_input, signup_email_input, signup_pass_input):
                    st.markdown('<div class="success-message">✓ Account created!</div>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown('<div class="error-message">✗ Signup failed (username taken?)</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class="features-section">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Risk Metrics</div>
            <div class="feature-desc">VaR, CVaR, Volatility & Drawdown analysis for comprehensive risk assessment</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔗</div>
            <div class="feature-title">Correlation Analysis</div>
            <div class="feature-desc">Understand asset relationships and identify portfolio concentration risks</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Diversification</div>
            <div class="feature-desc">Optimize your allocation with intelligent diversification scoring</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Insights</div>
            <div class="feature-desc">Get AI-powered recommendations tailored to your portfolio</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💪</div>
            <div class="feature-title">Stress Testing</div>
            <div class="feature-desc">Scenario analysis to prepare for extreme market conditions</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Performance</div>
            <div class="feature-desc">Track and analyze your investment performance over time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
