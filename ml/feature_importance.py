import pandas as pd
from utils.config import FEATURES
def importance(model):
    return pd.DataFrame({'Feature':FEATURES,'Importance':getattr(model,'feature_importances_', [0]*len(FEATURES))}).sort_values('Importance',ascending=False)
