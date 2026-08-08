# modules/signals.py
import pandas as pd
import config

def get_strong_signals(df):
    """
    Return only Strong Bullish and Strong Bearish stocks.
    """
    strong_bullish = df[df["Signal"] == "STRONG BULLISH"].sort_values("Score", ascending=False)
    strong_bearish = df[df["Signal"] == "STRONG BEARISH"].sort_values("Score", ascending=True)
    
    return strong_bullish, strong_bearish

def filter_by_signal(df, signal_type="STRONG BULLISH"):
    """
    Filter stocks by specific signal type.
    Options: "STRONG BULLISH", "Bullish", "Neutral", "Bearish", "STRONG BEARISH"
    """
    return df[df["Signal"] == signal_type].sort_values("Score", ascending=False)

def get_top_movers(df, n=10, direction="up"):
    """
    Get top N rising or falling stocks with minimum liquidity.
    direction = "up" or "down"
    """
    filtered = df[df["VALUE (Crores)"] >= config.MIN_VALUE_FOR_RANKING]
    
    if direction == "up":
        return filtered.sort_values("Score", ascending=False).head(n)
    else:
        return filtered.sort_values("Score", ascending=True).head(n)
