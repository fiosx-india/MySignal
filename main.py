# main.py
from modules.loader import load_fo_stocks, load_nse_indices, load_bse_indices
from modules.market import get_market_overview, calculate_index_bias
from modules.scoring import calculate_scores
from modules.analyzer import analyze_stock, print_top_lists
from modules.signals import get_strong_signals
import config

def main():
    print("Loading data...")
    
    # 1. Load all data
    fo_df = load_fo_stocks()
    nse_df = load_nse_indices()
    bse_df = load_bse_indices()
    
    # 2. Market Overview + Index Bias
    market = get_market_overview(nse_df, bse_df)
    index_bias = calculate_index_bias(market)
    
    # 3. Calculate Scores
    scored_df = calculate_scores(fo_df, market, index_bias)
    
    # 4. Print Market Overview
    print("\n========== MARKET OVERVIEW ==========")
    for k, v in market.items():
        print(f"{k:25}: {v}")
    print(f"Index Bias Score         : {index_bias:.2f}")
    
    # 5. Print Strong Signals + Top Lists
    print_top_lists(scored_df)
    
    # 6. Example Single Stock Analysis
    print(analyze_stock(scored_df, "BAJFINANCE", market))
    
    # Optional: Uncomment below to analyze any stock
    # symbol = input("\nEnter stock symbol to analyze: ").strip().upper()
    # if symbol:
    #     print(analyze_stock(scored_df, symbol, market))

if __name__ == "__main__":
    main()
