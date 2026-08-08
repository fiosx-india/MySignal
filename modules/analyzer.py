# modules/analyzer.py
import pandas as pd

def analyze_stock(df, symbol, market_overview):
    """
    Generate detailed analysis for a single stock.
    """
    stock = df[df["SYMBOL"].str.upper() == symbol.upper()]
    
    if stock.empty:
        return f"❌ {symbol} not found in F&O list."
    
    row = stock.iloc[0]
    
    result = f"""
==============================
{row['SYMBOL']}  →  {row['Signal']}
==============================
LTP              : {row['LTP']}
% Change         : {row['% CHANGE']}%
Value (Cr)       : {row['VALUE (Crores)']}
30D Momentum     : {row['30 D %CHNG']}%
Relative Strength: {row.get('rel_strength', 0):.2f}
Score            : {row['Score']}/10

Market Context:
Nifty 50         : {market_overview.get('NIFTY 50')}%
Bank Nifty       : {market_overview.get('NIFTY BANK')}%
Fin Services     : {market_overview.get('NIFTY FINANCIAL SERVICES')}%
India VIX        : {market_overview.get('INDIA VIX')}
Sensex           : {market_overview.get('BSE SENSEX')}%
BANKEX           : {market_overview.get('BSE BANKEX')}%
"""
    return result

def print_top_lists(df):
    """
    Print Strong signals and Top Rising / Falling lists.
    """
    print("\n========== STRONG BULLISH ==========")
    strong_up = df[df["Signal"] == "STRONG BULLISH"].sort_values("Score", ascending=False)
    if strong_up.empty:
        print("No Strong Bullish signals today")
    else:
        print(strong_up[["SYMBOL", "% CHANGE", "VALUE (Crores)", "30 D %CHNG", "Score", "Signal"]].to_string(index=False))

    print("\n========== TOP 10 RISING ==========")
    top_rising = df[df["VALUE (Crores)"] > 40].sort_values("Score", ascending=False).head(10)
    print(top_rising[["SYMBOL", "% CHANGE", "VALUE (Crores)", "30 D %CHNG", "Score", "Signal"]].to_string(index=False))

    print("\n========== STRONG BEARISH ==========")
    strong_down = df[df["Signal"] == "STRONG BEARISH"].sort_values("Score", ascending=True)
    if strong_down.empty:
        print("No Strong Bearish signals today")
    else:
        print(strong_down[["SYMBOL", "% CHANGE", "VALUE (Crores)", "30 D %CHNG", "Score", "Signal"]].to_string(index=False))

    print("\n========== TOP 10 FALLING ==========")
    top_falling = df[df["VALUE (Crores)"] > 40].sort_values("Score", ascending=True).head(10)
    print(top_falling[["SYMBOL", "% CHANGE", "VALUE (Crores)", "30 D %CHNG", "Score", "Signal"]].to_string(index=False))
