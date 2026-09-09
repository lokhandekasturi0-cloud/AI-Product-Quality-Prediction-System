from sklearn.preprocessing import StandardScaler
from utils.config import FEATURES
def feature_frame(df): return df[FEATURES].astype(float)
