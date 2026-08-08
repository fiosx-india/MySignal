# modules/scoring.py
import pandas as pd
import numpy as np
import config

def normalize(series):
    """Min-Max normalize a series to 0-1 range"""
    return (series - series.min()) / (series.max() - series.min() + 1e-9)

def calculate_scores(df, market_overview, index_bias):
    """
    Calculate multi-factor score for each stock.
    Returns dataframe with Score and Signal columns.
    """
    df = df.copy()

    nifty_chg = market_overview.get("NIFTY 50") or 0

    # Relative Strength (Stock vs Nifty)
    df["rel_strength"] = df["% CHANGE"] - nifty_chg

    # Normalize all factors (0 to 1)
    df["norm_pct"] = normalize(df["% CHANGE"])
    df["norm_value"] = normalize(df["VALUE (Crores)"])
    df["norm_mom"] = normalize(df["30 D %CHNG"])
    df["norm_rel"] = normalize(df["rel_strength"])

    # Final Score (0 to 10)
    df["Score"] = (
        df["norm_pct"] * config.WEIGHT_PCT_CHANGE +
        df["norm_value"] * config.WEIGHT_VALUE +
        df["norm_mom"] * config.WEIGHT_MOMENTUM +
        df["norm_rel"] * config.WEIGHT_REL_STRENGTH +
        index_bias * config.WEIGHT_INDEX_BIAS
    ) * 10

    # Liquidity Penalty
    df.loc[df["VALUE (Crores)"] < config.LOW_LIQUIDITY_PENALTY_1, "Score"] *= 0.75
    df.loc[df["VALUE (Crores)"] < config.LOW_LIQUIDITY_PENALTY_2, "Score"] *= 0.60

    df["Score"] = df["Score"].round(2)

    # Assign Signal Label
    df["Signal"] = df.apply(get_signal_label, axis=1)

    return df

def get_signal_label(row):
    """Return signal label based on score and liquidity"""
    score = row["Score"]
    value = row["VALUE (Crores)"]

    if score >= config.STRONG_BULLISH_SCORE and value >= config.STRONG_BULLISH_MIN_VALUE:
        return "STRONG BULLISH"
    elif score >= config.BULLISH_SCORE:
        return "Bullish"
    elif score <= config.STRONG_BEARISH_SCORE and value >= config.STRONG_BEARISH_MIN_VALUE:
        return "STRONG BEARISH"
    elif score <= config.BEARISH_SCORE:
        return "Bearish"
    else:
        return "Neutral"
