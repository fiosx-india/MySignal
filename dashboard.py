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
        st.metric("India VIX", f"{market.get('INDIA VIX', 'N/A')}")

    if index_bias >= 0.65:
        bias_label = "🟢 Bullish"
    elif index_bias <= 0.35:
        bias_label = "🔴 Bearish"
    else:
        bias_label = "🟡 Neutral"

    st.info(f"**Index Bias Score:** `{index_bias:.2f}`  →  **{bias_label}**")
    st.divider()

    # Sidebar
    with st.sidebar:
        st.title("MySignal")
        st.markdown("---")
        st.subheader("⚙️ Filters")
        min_value = st.slider("Min Value (₹ Cr)", 0, 500, 40, 10)
        signal_filter = st.multiselect(
            "Signal Type",
            options=["STRONG BULLISH", "Bullish", "Neutral", "Bearish", "STRONG BEARISH"],
            default=["STRONG BULLISH", "STRONG BEARISH", "Bullish"]
        )
        st.markdown("---")
        st.subheader("🔍 Stock Search")
        symbol_input = st.text_input("Symbol", placeholder="e.g. RELIANCE").strip().upper()
        st.markdown("---")
        st.caption("Personal use only")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Strong Signals", "📈 Top Rising", "📉 Top Falling", "🔎 Stock Detail"])

    filtered = scored_df[scored_df["VALUE (Crores)"] >= min_value]
    if signal_filter:
        filtered = filtered[filtered["Signal"].isin(signal_filter)]

    display_cols = ["SYMBOL", "% CHANGE", "VALUE (Crores)", "30 D %CHNG", "Score", "Signal"]

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🟢 Strong Bullish")
            strong_up = scored_df[scored_df["Signal"] == "STRONG BULLISH"].sort_values("Score", ascending=False)
            if strong_up.empty:
                st.warning("No Strong Bullish signals")
            else:
                st.dataframe(strong_up[display_cols], use_container_width=True, hide_index=True)
        with col_b:
            st.markdown("#### 🔴 Strong Bearish")
            strong_down = scored_df[scored_df["Signal"] == "STRONG BEARISH"].sort_values("Score", ascending=True)
            if strong_down.empty:
                st.warning("No Strong Bearish signals")
            else:
                st.dataframe(strong_down[display_cols].head(15), use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("#### Top 15 Rising (by Score)")
        top_up = filtered.sort_values("Score", ascending=False).head(15)
        st.dataframe(top_up[display_cols], use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("#### Top 15 Falling (by Score)")
        top_down = filtered.sort_values("Score", ascending=True).head(15)
        st.dataframe(top_down[display_cols], use_container_width=True, hide_index=True)

    with tab4:
        if symbol_input:
            stock = scored_df[scored_df["SYMBOL"] == symbol_input]
            if stock.empty:
                st.error(f"❌ **{symbol_input}** not found in F&O list")
            else:
                row = stock.iloc[0]
                signal = row["Signal"]
                if "STRONG BULLISH" in signal:
                    badge = f'<span class="signal-strong-bull">{signal}</span>'
                elif "Bullish" in signal:
                    badge = f'<span class="signal-bull">{signal}</span>'
                elif "STRONG BEARISH" in signal:
                    badge = f'<span class="signal-strong-bear">{signal}</span>'
                elif "Bearish" in signal:
                    badge = f'<span class="signal-bear">{signal}</span>'
                else:
                    badge = f'<span class="signal-neutral">{signal}</span>'

                st.markdown(f"### {row['SYMBOL']} &nbsp; {badge}", unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("LTP", f"₹ {row['LTP']}")
                c2.metric("% Change", f"{row['% CHANGE']}%")
                c3.metric("Value", f"₹ {row['VALUE (Crores)']} Cr")
                c4.metric("Score", f"{row['Score']} / 10")

                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | 30D Momentum | {row['30 D %CHNG']}% |
                | Relative Strength | {row.get('rel_strength', 0):.2f} |
                | Nifty 50 | {market.get('NIFTY 50')}% |
                | Bank Nifty | {market.get('NIFTY BANK')}% |
                | Fin Services | {market.get('NIFTY FINANCIAL SERVICES')}% |
                | India VIX | {market.get('INDIA VIX')} |
                """)
        else:
            st.info("👈 Type a stock symbol in the sidebar (e.g. RELIANCE, TCS, SBIN)")

    st.divider()
    st.caption("MySignal • Personal F&O Signal System • Data from your CSVs")

if __name__ == "__main__":
    main()
