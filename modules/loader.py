# modules/loader.py
import pandas as pd
from pathlib import Path
import config

def load_fo_stocks():
    """Load and clean F&O stocks data"""
    file_path = config.DATA_DIR / "fo_stocks.csv"
    df = pd.read_csv(file_path)
    
    # Clean column names
    df.columns = [c.strip().replace("\n", " ").replace('"', '') for c in df.columns]
    
    # Convert important columns to numeric
    numeric_cols = ["% CHANGE", "VOLUME (shares)", "VALUE (Crores)", "30 D %CHNG", "LTP"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ""), 
                errors="coerce"
            )
    
    # Drop rows without essential data
    df = df.dropna(subset=["SYMBOL", "% CHANGE", "VALUE (Crores)"])
    
    # Clean SYMBOL
    df["SYMBOL"] = df["SYMBOL"].astype(str).str.strip().str.upper()
    
    return df

def load_nse_indices():
    """Load NSE indices data"""
    file_path = config.DATA_DIR / "nse_indices.csv"
    df = pd.read_csv(file_path)
    
    # Clean column names
    df.columns = [c.strip().replace("\n", " ").replace('"', '') for c in df.columns]
    
    return df

def load_bse_indices():
    """Load BSE indices data"""
    file_path = config.DATA_DIR / "bse_indices.csv"
    df = pd.read_csv(file_path)
    
    return df
