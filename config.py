# config.py
# Settings and Weights for MySignal

from pathlib import Path

# ======================
# PATHS
# ======================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# ======================
# SCORING WEIGHTS (Total = 1.0)
# ======================
WEIGHT_PCT_CHANGE = 0.35
WEIGHT_VALUE = 0.25
WEIGHT_MOMENTUM = 0.20
WEIGHT_REL_STRENGTH = 0.10
WEIGHT_INDEX_BIAS = 0.10

# ======================
# SIGNAL THRESHOLDS
# ======================
STRONG_BULLISH_SCORE = 7.5
STRONG_BULLISH_MIN_VALUE = 100      # Crores

STRONG_BEARISH_SCORE = 2.8
STRONG_BEARISH_MIN_VALUE = 50       # Crores

BULLISH_SCORE = 6.5
BEARISH_SCORE = 4.0

# ======================
# LIQUIDITY FILTER
# ======================
MIN_VALUE_FOR_RANKING = 40          # Crores (for Top lists)
LOW_LIQUIDITY_PENALTY_1 = 30        # Below this → score * 0.75
LOW_LIQUIDITY_PENALTY_2 = 15        # Below this → score * 0.60

# ======================
# INDEX BIAS SETTINGS
# ======================
INDEX_BIAS_STRONG_POSITIVE = 0.40
INDEX_BIAS_POSITIVE = 0.00
INDEX_BIAS_NEGATIVE = -0.40
