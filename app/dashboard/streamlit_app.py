"""
ARAIA - Portfolio Risk Analyzer Dashboard.

Interactive Streamlit application for visualizing and analyzing portfolio risk metrics,
correlations, diversification, stress tests, and AI-generated insights.
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

BACKEND_URL = "http://127.0.0.1:8000/portfolio"
DEFAULT_ASSETS = []

# Page config
st.set_page_config(
    page_title="ARAIA - Portfolio Risk Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS for styling
st.markdown(
    """
    <style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 15px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 15px 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 15px 0;
    }
    .ai-explanation {
        background: transparent;
        padding: 0;
        border-radius: 0;
        border: none;
        margin: 15px 0;
        font-style: italic;
        color: #ffffff;
        line-height: 1.6;
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
        return False, "⏱️ Request timed out. Is the backend running at http://127.0.0.1:8000?"
    except requests.exceptions.ConnectionError:
        return False, "❌ Cannot connect to backend. Ensure it's running at http://127.0.0.1:8000"
    except Exception as exc:
        return False, f"Unexpected error: {str(exc)}"


# ============================================================================
# UI BUILDING BLOCKS
# ============================================================================


def render_title():
    """Render the application title and description."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            """
            # 📊 ARAIA - Portfolio Risk Analyzer
            ### Interactive Risk Analysis & AI-Powered Insights
            """
        )
    with col2:
        st.markdown(
            """
            <div style='text-align: right; padding: 20px;'>
            <p style='color: gray; font-size: 12px;'>Advanced Risk Analysis via AI</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_portfolio_input_section():
    """Render portfolio input form with dynamic asset rows and CSV upload."""
    st.markdown("## 📝 Portfolio Input")

    st.write(
        "Enter tickers and weights for your portfolio. Weights will be normalized to sum to 1.0."
    )

    # CSV Upload Section
    st.markdown("### 📤 Upload Portfolio from CSV")
    uploaded_file = st.file_uploader(
        "Choose a CSV file with ticker and weight columns:",
        type=["csv"],
        help="CSV should have columns: ticker, weight (or symbol, allocation, etc.)",
    )

    if uploaded_file is not None:
        success, result = parse_csv_file(uploaded_file)
        if success:
            st.session_state.assets = result
            st.success(f"✅ Loaded {len(result)} assets from CSV")
            st.write("Parsed portfolio:")
            for asset in result:
                st.write(f"• {asset['ticker']}: {asset['weight']:.1%}")
        else:
            st.error(f"❌ CSV Error: {result}")

    st.markdown("---")
    st.markdown("### 📝 Manual Entry")

    st.write("Or manually enter assets below:")

    # Create input columns for assets
    col1, col2, col3 = st.columns([2, 1, 1])

    assets = []

    with col1:
        st.write("**Ticker**")
    with col2:
        st.write("**Weight**")
    with col3:
        st.write("**Action**")

    # Display all asset rows (no limit)
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

    # Update session state with current assets
    if assets:
        st.session_state.assets = assets
    elif not st.session_state.assets:
        # Start with empty, user must add assets
        st.session_state.assets = []

    # Add asset button
    if st.button("➕ Add Asset", key="add_asset"):
        st.session_state.assets.append({"ticker": "", "weight": 0.25})
        st.rerun()

    return st.session_state.assets


def render_analyze_button() -> bool:
    """Render the analyze portfolio button."""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        return st.button("🚀 Analyze Portfolio", use_container_width=True)


def render_metrics_section(data: dict):
    """Render key risk metrics in a card layout."""
    st.markdown("## 📊 Risk Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        volatility = data.get("metrics", {}).get("volatility", 0)
        st.metric(
            "Volatility",
            f"{volatility:.2%}",
            help="Annualized portfolio standard deviation",
        )

    with col2:
        var_95 = data.get("metrics", {}).get("var", 0)
        st.metric(
            "VaR (95%)",
            f"{var_95:.4f}",
            help="Value at Risk - worst expected loss at 95% confidence",
        )

    with col3:
        cvar_95 = data.get("metrics", {}).get("cvar", 0)
        st.metric(
            "CVaR (95%)",
            f"{cvar_95:.4f}",
            help="Conditional VaR - average loss beyond VaR",
        )

    with col4:
        max_drawdown = data.get("metrics", {}).get("max_drawdown", 0)
        st.metric(
            "Max Drawdown",
            f"{max_drawdown:.2%}",
            help="Maximum peak-to-trough decline",
        )


def render_clusters_section(data: dict):
    """Render asset clustering analysis."""
    st.markdown("## 🔗 Asset Clustering")

    clusters = data.get("clusters", {})
    if not clusters:
        st.info("No clustering data available")
        return

    cluster_details = []
    for cluster_id, tickers in clusters.items():
        cluster_details.append(
            f"**Cluster {cluster_id}:** {', '.join(tickers)} ({len(tickers)} assets)"
        )

    for detail in cluster_details:
        st.write(detail)

    # Show high correlation pairs
    high_corr_pairs = data.get("high_correlation_pairs", [])
    if high_corr_pairs:
        st.markdown("### 🔥 High Correlation Pairs (> 0.7)")
        for pair in high_corr_pairs:
            ticker_a, ticker_b, corr = pair
            st.write(f"• {ticker_a} ↔ {ticker_b}: **{corr:.4f}**")


def render_diversification_section(data: dict):
    """Render diversification metrics."""
    st.markdown("## 🎯 Diversification Analysis")

    col1, col2 = st.columns(2)

    with col1:
        enb = data.get("diversification", {}).get("enb", 0)
        st.metric(
            "Effective Number of Bets (ENB)",
            f"{enb:.2f}",
            help="Number of equally-weighted bets in portfolio",
        )

    with col2:
        div_score = data.get("diversification", {}).get("diversification_score", 0)
        st.metric(
            "Diversification Score",
            f"{div_score:.4f}",
            help="ENB normalized by asset count (max = 1.0)",
        )

    # Cluster concentration
    cluster_conc = data.get("diversification", {}).get("cluster_concentration", {})
    if cluster_conc:
        st.markdown("### Cluster Concentration by Weight")
        conc_df_data = [
            {"Cluster": k.replace("cluster_", "Cluster "), "Weight": v}
            for k, v in cluster_conc.items()
        ]
        # Display as bar chart
        import pandas as pd

        conc_df = pd.DataFrame(conc_df_data)
        fig = px.bar(
            conc_df,
            x="Cluster",
            y="Weight",
            title="Portfolio Weight Distribution by Cluster",
            labels={"Weight": "Portfolio Weight"},
            color="Weight",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True)


def render_stress_test_section(data: dict):
    """Render stress test comparison."""
    st.markdown("## ⚠️ Stress Test Analysis")

    stress = data.get("stress", {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("**Normal Scenario**")
        st.write(f"VaR (95%): {stress.get('normal_var', 0):.4f}")

    with col2:
        st.write("**Stressed Scenario**")
        st.write(f"Stressed VaR: {stress.get('stressed_var', 0):.4f}")

    with col3:
        st.write("**Normal**")
        st.write(f"CVaR: {stress.get('normal_cvar', 0):.4f}")

    with col4:
        st.write("**Stressed**")
        st.write(f"Stressed CVaR: {stress.get('stressed_cvar', 0):.4f}")

    # Stress comparison chart
    import pandas as pd

    stress_data = pd.DataFrame(
        {
            "Metric": ["VaR (95%)", "CVaR (95%)"],
            "Normal": [stress.get("normal_var", 0), stress.get("normal_cvar", 0)],
            "Stressed": [
                stress.get("stressed_var", 0),
                stress.get("stressed_cvar", 0),
            ],
        }
    )

    fig = px.bar(
        stress_data,
        x="Metric",
        y=["Normal", "Stressed"],
        title="Normal vs Stressed Scenario Comparison",
        barmode="group",
        labels={"value": "Risk Value", "variable": "Scenario"},
        color_discrete_map={"Normal": "#2ecc71", "Stressed": "#e74c3c"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_ai_explanation_section(data: dict):
    """Render AI-generated portfolio explanation."""
    st.markdown("## 🤖 AI-Powered Insights")

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


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================


def plot_correlation_heatmap(data: dict):
    """Create interactive correlation matrix heatmap."""
    st.markdown("## 🔥 Correlation Heatmap")

    import pandas as pd
    import numpy as np

    # Extract correlation matrix from data
    corr_matrix_dict = data.get("correlation_matrix", {})
    if not corr_matrix_dict:
        st.warning("Correlation matrix not available")
        return

    # Convert dict to DataFrame
    try:
        df_corr = pd.DataFrame(corr_matrix_dict)
    except Exception as e:
        st.warning(f"Could not parse correlation matrix: {e}")
        return

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=df_corr.values,
            x=df_corr.columns,
            y=df_corr.index,
            colorscale="RdBu",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=np.round(df_corr.values, 3),
            texttemplate="%{text:.3f}",
            textfont={"size": 10},
            colorbar=dict(title="Correlation"),
        )
    )

    fig.update_layout(
        title="Asset Correlation Matrix",
        xaxis_title="Asset",
        yaxis_title="Asset",
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_risk_contribution(data: dict):
    """Create risk contribution bar chart by asset."""
    st.markdown("## 📊 Risk Contribution Analysis")

    import pandas as pd

    # Extract weights and cmetrics", {}).get("alculate risk contribution
    assets_info = data.get("assets", [])
    volatility = data.get("volatility", 0.1)  # Default fallback

    if not assets_info:
        st.warning("Asset information not available")
        return

    # Simple risk contribution: weight * volatility
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
        subplot_titles=("Risk Contribution by Asset", "Portfolio Weight Distribution"),
    )

    fig.add_trace(
        go.Bar(
            x=df_risk["Ticker"],
            y=df_risk["Risk Contribution"],
            name="Risk Contribution",
            marker_color="indianred",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Pie(
            labels=df_risk["Ticker"],
            values=df_risk["Weight"],
            name="Weight",
            marker=dict(colors=px.colors.qualitative.Set3),
        ),
        row=1,
        col=2,
    )

    fig.update_xaxes(title_text="Asset", row=1, col=1)
    fig.update_yaxes(title_text="Risk Contribution", row=1, col=1)

    fig.update_layout(height=500, showlegend=True)

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================


def main():
    """Main application flow."""
    initialize_session_state()

    # Title section
    render_title()

    st.markdown("---")

    # Portfolio Input Section
    st.markdown("### Step 1: Configure Your Portfolio")
    assets = render_portfolio_input_section()

    st.markdown("---")

    # Analyze Button
    st.markdown("### Step 2: Analyze")
    if render_analyze_button():
        success, result = call_backend_api(assets)

        if success:
            st.session_state.portfolio_data = result
            st.session_state.error_message = None
        else:
            st.session_state.error_message = result
            st.session_state.portfolio_data = None

    # Display Results
    if st.session_state.error_message:
        st.markdown(
            f"""
            <div class='error-box'>
            <strong>❌ Error:</strong> {st.session_state.error_message}
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.portfolio_data:
        st.markdown("---")
        st.markdown("### Step 3: Review Analysis Results")

        data = st.session_state.portfolio_data

        # Debug: Show if we got data
        if "metrics" not in data:
            st.error("❌ Backend response missing metrics. Check backend logs.")
            st.json(data)
            return

        # Metrics Section
        render_metrics_section(data)

        st.markdown("---")

        # Clusters Section
        render_clusters_section(data)

        st.markdown("---")

        # Diversification Section
        render_diversification_section(data)

        st.markdown("---")

        # Stress Test Section
        render_stress_test_section(data)

        st.markdown("---")

        # Visualization Section
        st.markdown("### 📈 Detailed Visualizations")

        # Tabs for different charts
        tab1, tab2, tab3 = st.tabs(
            [
                "Correlation Heatmap",
                "Risk Contribution",
                "Raw Data",
            ]
        )

        with tab1:
            plot_correlation_heatmap(data)

        with tab2:
            plot_risk_contribution(data)

        with tab3:
            st.markdown("#### Full API Response")
            st.json(data)

        st.markdown("---")

        # AI Explanation Section
        render_ai_explanation_section(data)

        st.markdown("---")

        # Download option
        st.markdown("### 📥 Export Results")
        import json

        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="Download Analysis as JSON",
            data=json_str,
            file_name="portfolio_analysis.json",
            mime="application/json",
        )


if __name__ == "__main__":
    main()
