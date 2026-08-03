import pandas as pd
import numpy as np
from pathlib import Path

# ======================
# SETTINGS (Weights)
# ======================
WEIGHT_PCT_CHANGE = 0.40
WEIGHT_VALUE = 0.30
WEIGHT_MOMENTUM = 0.20
WEIGHT_INDEX_BIAS = 0.10

DATA_DIR = Path("data")

# ======================
# LOAD DATA
# ======================
def load_fo_stocks():
    df = pd.read_csv(DATA_DIR / "fo_stocks.csv")
    # Clean column names
    df.columns = [c.strip().replace("\n", " ").replace('"', '') for c in df.columns]
    
    # Convert important columns to numeric
    for col in ["% CHANGE", "VOLUME (shares)", "VALUE (Crores)", "30 D %CHNG", "LTP"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
    
    df = df.dropna(subset=["SYMBOL", "% CHANGE"])
    return df

def load_nse_indices():
    df = pd.read_csv(DATA_DIR / "nse_indices.csv")
    df.columns = [c.strip().replace("\n", " ").replace('"', '') for c in df.columns]
    return df

def load_bse_indices():
    df = pd.read_csv(DATA_DIR / "bse_indices.csv")
    return df

# ======================
# MARKET OVERVIEW
# ======================
def get_market_overview(nse_df, bse_df):
    overview = {}
    
    # NSE
    for idx in ["NIFTY 50", "NIFTY BANK", "NIFTY FINANCIAL SERVICES", "INDIA VIX"]:
        row = nse_df[nse_df.iloc[:, 0].str.contains(idx, case=False, na=False)]
        if not row.empty:
            try:
                pct = float(str(row.iloc[0, 2]).replace(",", ""))
                overview[idx] = pct
            except:
                overview[idx] = None
    
    # BSE
    for idx in ["BSE SENSEX", "BSE BANKEX"]:
        row = bse_df[bse_df["IndexName"].str.contains(idx.split()[-1], case=False, na=False)]
        if not row.empty:
            try:
                prev = float(row.iloc[0]["PreviousClose"])
                close = float(row.iloc[0]["ClosePrice"])
                overview[idx] = round(((close - prev) / prev) * 100, 2)
            except:
                overview[idx] = None
    
    return overview

# ======================
# SCORING
# ======================
def calculate_scores(df, market_bias=0.5):
    df = df.copy()
    
    # Normalize factors (0 to 1)
    df["norm_pct"] = (df["% CHANGE"] - df["% CHANGE"].min()) / (df["% CHANGE"].max() - df["% CHANGE"].min() + 1e-9)
    df["norm_value"] = (df["VALUE (Crores)"] - df["VALUE (Crores)"].min()) / (df["VALUE (Crores)"].max() - df["VALUE (Crores)"].min() + 1e-9)
    df["norm_mom"] = (df["30 D %CHNG"] - df["30 D %CHNG"].min()) / (df["30 D %CHNG"].max() - df["30 D %CHNG"].min() + 1e-9)
    
    # Final Score
    df["Score"] = (
        df["norm_pct"] * WEIGHT_PCT_CHANGE +
        df["norm_value"] * WEIGHT_VALUE +
        df["norm_mom"] * WEIGHT_MOMENTUM +
        market_bias * WEIGHT_INDEX_BIAS
    )
    
    df["Score"] = (df["Score"] * 10).round(2)  # 0 to 10 scale
    return df

# ======================
# SINGLE STOCK ANALYSIS
# ======================
def analyze_stock(df, symbol, market_overview):
    stock = df[df["SYMBOL"].str.upper() == symbol.upper()]
    if stock.empty:
        return f"{symbol} not found in F&O list."
    
    row = stock.iloc[0]
    score = row["Score"]
    
    if score >= 7.0:
        bias = "Bullish"
    elif score >= 4.5:
        bias = "Neutral"
    else:
        bias = "Bearish"
    
    result = f"""
==============================
{row['SYMBOL']}
==============================
LTP           : {row['LTP']}
% Change      : {row['% CHANGE']}%
Value (Cr)    : {row['VALUE (Crores)']}
30D Momentum  : {row['30 D %CHNG']}%
Score         : {score}/10
Bias          : {bias}

Market Context:
Nifty 50      : {market_overview.get('NIFTY 50')}%
Bank Nifty    : {market_overview.get('NIFTY BANK')}%
Fin Services  : {market_overview.get('NIFTY FINANCIAL SERVICES')}%
India VIX     : {market_overview.get('INDIA VIX')}
Sensex        : {market_overview.get('BSE SENSEX')}%
"""
    return result

# ======================
# MAIN
# ======================
if __name__ == "__main__":
    print("Loading data...")
    fo_df = load_fo_stocks()
    nse_df = load_nse_indices()
    bse_df = load_bse_indices()
    
    market = get_market_overview(nse_df, bse_df)
    
    # Simple market bias (0 to 1)
    nifty_chg = market.get("NIFTY 50") or 0
    market_bias = 0.7 if nifty_chg > 0.3 else (0.4 if nifty_chg < -0.3 else 0.55)
    
    scored_df = calculate_scores(fo_df, market_bias)
    
    print("\n========== MARKET OVERVIEW ==========")
    for k, v in market.items():
        print(f"{k:25}: {v}")
    
    print("\n========== TOP 10 RISING ==========")
    top_rising = scored_df[scored_df["VALUE (Crores)"] > 20].sort_values("Score", ascending=False).head(10)
    print(top_rising[["SYMBOL", "% CHANGE", "VALUE (Crores)", "30 D %CHNG", "Score"]].to_string(index=False))
    
    print("\n========== TOP 10 FALLING ==========")
    top_falling = scored_df[scored_df["VALUE (Crores)"] > 20].sort_values("Score", ascending=True).head(10)
    print(top_falling[["SYMBOL", "% CHANGE", "VALUE (Crores)", "30 D %CHNG", "Score"]].to_string(index=False))
    
    # Example single stock
    print(analyze_stock(scored_df, "BAJFINANCE", market))
