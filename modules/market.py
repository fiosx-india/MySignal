# modules/market.py
import pandas as pd
import config

def get_market_overview(nse_df, bse_df):
    """
    Extract key index data and calculate overall market bias.
    Returns a dictionary with index % changes and bias score.
    """
    overview = {}

    # ---------- NSE Indices ----------
    nse_map = {
        "NIFTY 50": "NIFTY 50",
        "NIFTY BANK": "NIFTY BANK",
        "NIFTY FINANCIAL SERVICES": "NIFTY FINANCIAL SERVICES",
        "INDIA VIX": "INDIA VIX"
    }

    for key, search_term in nse_map.items():
        try:
            row = nse_df[nse_df.iloc[:, 0].astype(str).str.contains(search_term, case=False, na=False)]
            if not row.empty:
                # %CHNG is usually the 3rd column (index 2)
                pct_str = str(row.iloc[0, 2]).replace(",", "").strip()
                overview[key] = float(pct_str)
            else:
                overview[key] = None
        except Exception:
            overview[key] = None

    # ---------- BSE Indices ----------
    bse_map = {
        "BSE SENSEX": "SENSEX",
        "BSE BANKEX": "BANKEX"
    }

    for key, search_term in bse_map.items():
        try:
            row = bse_df[bse_df["IndexName"].astype(str).str.contains(search_term, case=False, na=False)]
            if not row.empty:
                prev = float(row.iloc[0]["PreviousClose"])
                close = float(row.iloc[0]["ClosePrice"])
                overview[key] = round(((close - prev) / prev) * 100, 2)
            else:
                overview[key] = None
        except Exception:
            overview[key] = None

    return overview

def calculate_index_bias(overview):
    """
    Calculate a single Index Bias score (0 to 1) based on major indices.
    Higher = more bullish market environment.
    """
    nifty = overview.get("NIFTY 50") or 0
    bank = overview.get("NIFTY BANK") or 0
    fin = overview.get("NIFTY FINANCIAL SERVICES") or 0

    avg_change = (nifty + bank + fin) / 3

    if avg_change >= config.INDEX_BIAS_STRONG_POSITIVE:
        return 0.85
    elif avg_change > config.INDEX_BIAS_POSITIVE:
        return 0.65
    elif avg_change > config.INDEX_BIAS_NEGATIVE:
        return 0.45
    else:
        return 0.25
