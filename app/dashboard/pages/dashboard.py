"""
ARAIA Dashboard - Portfolio Risk Analyzer
Modern, fancy interface with enhanced visualizations
"""

import streamlit as st

# Set page config first
st.set_page_config(
    page_title="ARAIA Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Check if user is logged in
if not st.session_state.get("logged_in"):
    st.warning("⚠️ Please log in first!")
    st.stop()

# Modern CSS styling
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 24px;
        background: rgba(30, 41, 59, 0.6);
        border-radius: 14px;
        border: 1px solid rgba(51, 65, 85, 0.3);
        margin-bottom: 32px;
    }
    
    .header-title {
        font-size: 32px;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .header-user {
        display: flex;
        align-items: center;
        gap: 12px;
        color: #94a3b8;
        font-size: 14px;
    }
    
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(51, 65, 85, 0.4);
        border-radius: 12px;
        padding: 24px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(14, 165, 233, 0.3);
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.1);
    }
    
    .metric-label {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .metric-change {
        font-size: 12px;
        color: #86efac;
    }
    
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #f1f5f9;
        margin: 32px 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(14, 165, 233, 0.2);
    }
    
    .card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(51, 65, 85, 0.3);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
    }
    
    .feature-badge {
        display: inline-block;
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(14, 165, 233, 0.3);
        color: #0ea5e9;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    /* Button Styling */
    [data-testid="baseButton-primary"] button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="baseButton-primary"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(14, 165, 233, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↩️ Back", use_container_width=True):
            st.switch_page("landing_page.py")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.token = None
            st.switch_page("landing_page.py")
    
    st.markdown("---")
    st.markdown("### Quick Links")
    st.markdown("""
    - 📊 Portfolio Analysis
    - 📈 Risk Metrics
    - 🔗 Correlations
    - 🎯 Diversification
    - 🤖 AI Insights
    - 💪 Stress Tests
    """)

# Main Header
st.markdown(f"""
<div class="dashboard-header">
    <div class="header-title">📊 Portfolio Dashboard</div>
    <div class="header-user">
        👤 {st.session_state.username}
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Stats Row
st.markdown("### Key Metrics")
metric_cols = st.columns(4)

with metric_cols[0]:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Portfolio Value</div>
        <div class="metric-value">$100,000</div>
        <div class="metric-change">↑ +2.5% today</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[1]:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Return</div>
        <div class="metric-value">+12.8%</div>
        <div class="metric-change">YTD Performance</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[2]:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Risk (Volatility)</div>
        <div class="metric-value">18.2%</div>
        <div class="metric-change">Annual</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[3]:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Sharpe Ratio</div>
        <div class="metric-value">1.45</div>
        <div class="metric-change">Risk-adjusted returns</div>
    </div>
    """, unsafe_allow_html=True)

# Portfolio Upload Section
st.markdown("### Portfolio Management")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
    <h4>📤 Upload Portfolio</h4>
    <p>Import your portfolio data from a CSV file with ticker symbols and weights.</p>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="portfolio_upload")
    
    if uploaded_file:
        st.success(f"✓ File uploaded: {uploaded_file.name}")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h4>📊 Sample Portfolio</h4>
    <p>Start with sample data to explore the dashboard features.</p>
    """, unsafe_allow_html=True)
    
    if st.button("Load Sample Portfolio", use_container_width=True):
        st.success("✓ Sample portfolio loaded!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Analysis Sections
st.markdown("### Analysis Tools")

tab1, tab2, tab3, tab4 = st.tabs(["🔗 Correlations", "🎯 Diversification", "💪 Stress Tests", "🤖 AI Insights"])

with tab1:
    st.markdown("""
    <div class="card">
    <h4>Correlation Matrix Analysis</h4>
    <p>Analyze how your portfolio assets move together. High correlations indicate elevated concentration risk.</p>
    
    <div>
        <span class="feature-badge">Pairwise Correlations</span>
        <span class="feature-badge">Heatmap Visualization</span>
        <span class="feature-badge">Risk Identification</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Run Correlation Analysis"):
        st.info("Correlation analysis would run here - connect with your portfolio data")
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="card">
    <h4>Diversification Scoring</h4>
    <p>Measure how well-diversified your portfolio is and identify optimization opportunities.</p>
    
    <div>
        <span class="feature-badge">Diversification Score</span>
        <span class="feature-badge">ENB Analysis</span>
        <span class="feature-badge">Cluster Concentration</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Calculate Diversification"):
        st.info("Diversification analysis would run here - connect with your portfolio data")
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="card">
    <h4>Stress Testing Scenarios</h4>
    <p>Test your portfolio performance under extreme market conditions and correlation changes.</p>
    
    <div>
        <span class="feature-badge">Correlation Stress</span>
        <span class="feature-badge">Joint Stress</span>
        <span class="feature-badge">Scenario Analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Run Stress Tests"):
        st.info("Stress tests would run here - connect with your portfolio data")
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="card">
    <h4>AI-Generated Insights</h4>
    <p>Get intelligent recommendations based on your portfolio composition, risk profile, and market conditions.</p>
    
    <div>
        <span class="feature-badge">AI Analysis</span>
        <span class="feature-badge">Recommendations</span>
        <span class="feature-badge">Optimization Tips</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Generate AI Insights"):
        st.info("AI insights would generate here - connect with your portfolio data")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Risk Metrics Section
st.markdown("### Risk Assessment")

risk_cols = st.columns(2)

with risk_cols[0]:
    st.markdown("""
    <div class="card">
    <h5>Value at Risk (VaR)</h5>
    <p><strong>95% Confidence:</strong> -$2,500</p>
    <p><small>Expected maximum loss with 95% confidence</small></p>
    </div>
    """, unsafe_allow_html=True)

with risk_cols[1]:
    st.markdown("""
    <div class="card">
    <h5>Conditional Value at Risk (CVaR)</h5>
    <p><strong>95% Confidence:</strong> -$3,200</p>
    <p><small>Average loss in worst 5% of scenarios</small></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 12px; margin-top: 40px;">
    <p>💡 Connect your portfolio data from the Upload section to activate all analysis features</p>
    <p style="margin-top: 20px;">Last updated: Just now</p>
</div>
""", unsafe_allow_html=True)
