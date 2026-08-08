# dashboard.py
import streamlit as st
import pandas as pd
from modules.loader import load_fo_stocks, load_nse_indices, load_bse_indices
from modules.market import get_market_overview, calculate_index_bias
from modules.scoring import calculate_scores
from modules.analyzer import analyze_stock
from modules.signals import get_strong_signals, get_top_movers
import config

# Page Config
st.set_page_config(
    page_title="MySignal - F&O Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1a73e8, #0d47a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        color: #5f6368;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border: 1px solid #e8eaed;
        border-radius: 12px;
        padding: 12px 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] label {
        color: #5f6368 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #e8eaed;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8f0fe !important;
        color: #1a73e8 !important;
    }
    .signal-strong-bull {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .signal-bull {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .signal-strong-bear {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .signal-bear {
        background-color: #ffebee;
        color: #c62828;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .signal-neutral {
        background-color: #f1f3f4;
        color: #5f6368;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    fo_df = load_fo_stocks()
    nse_df = load_nse_indices()
    bse_df = load_bse_indices()
    market = get_market_overview(nse_df, bse_df)
    index_bias = calculate_index_bias(market)
    scored_df = calculate_scores(fo_df, market, index_bias)
    return scored_df, market, index_bias

def main():
    st.markdown('<div class="main-header">📈 MySignal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">F&O Multi-Factor Signal Dashboard • Price + Volume + Momentum + Index Bias</div>', unsafe_allow_html=True)

    with st.spinner("Loading market data..."):
        scored_df, market, index_bias = load_all_data()

    # Market Overview
    st.subheader("Market Overview")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Nifty 50", f"{market.get('NIFTY 50', 'N/A')}%")
    with col2:
        st.metric("Bank Nifty", f"{market.get('NIFTY BANK', 'N/A')}%")
    with col3:
        st.metric("Fin Services", f"{market.get('NIFTY FINANCIAL SERVICES', 'N/A')}%")
    with col4:
        st.metric("Sensex", f"{market.get('BSE SENSEX', 'N/A')}%")
    with col5:
        st.metric("BANKEX", f"{market.get('BSE BANKEX', 'N/A')}%")
    with col6:
        st.metric("India VIX", f"{market.get('INDIA VIX', 'N/A')
