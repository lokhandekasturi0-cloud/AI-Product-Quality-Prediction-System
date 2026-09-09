import json, joblib, pandas as pd
from pathlib import Path
from utils.config import FEATURES
from utils.explanation import explain
ROOT=Path(__file__).resolve().parents[1]
def load_model():
    path=ROOT/'models'/'quality_model.pkl'
    if not path.exists():
        # First-run convenience: persist a demo model once; ordinary predictions only load it.
        from ml.train_model import main
        main()
    return joblib.load(path)
def predict_frame(df):
    model=load_model(); probs=model.predict_proba(df[FEATURES].astype(float)); labels=model.classes_; idx=probs.argmax(axis=1)
    out=df.copy(); out['Prediction']=[labels[i] for i in idx]
    # The score uses predicted class plus classifier confidence: PASS 70-100,
    # REWORK 40-65, and REJECT 5-35.
    confidence=probs.max(axis=1); base={'PASS':70.0,'REWORK':40.0,'REJECT':5.0}; span={'PASS':30.0,'REWORK':25.0,'REJECT':30.0}
    out['Quality_Score']=[round(base[label]+span[label]*conf,1) for label,conf in zip(out['Prediction'],confidence)]
    info=out.apply(explain,axis=1,result_type='expand'); out['Reason']=info[0]; out['Suggested_Action']=info[1]
    return out
def metadata():
    if not (ROOT/'models'/'model_metadata.json').exists(): load_model()
    with open(ROOT/'models'/'model_metadata.json',encoding='utf8') as f: return json.load(f)
