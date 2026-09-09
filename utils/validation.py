import pandas as pd
from utils.config import REQUIRED_COLUMNS, FEATURES
def validate_frame(df):
    missing=[c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing: return False, f"Missing required columns: {', '.join(missing)}"
    if df.empty: return False, "The uploaded file contains no rows."
    clean=df[REQUIRED_COLUMNS].copy()
    for f in FEATURES: clean[f]=pd.to_numeric(clean[f], errors="coerce")
    if clean[FEATURES].isna().any().any() or clean["Product_ID"].isna().any(): return False, "Product ID and all measurement fields must be present and numeric."
    if (clean[FEATURES]<0).any().any(): return False, "Negative measurements are not accepted."
    return True, clean
