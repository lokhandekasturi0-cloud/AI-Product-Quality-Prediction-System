"""Create demonstration data and train the persisted quality model."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from utils.config import FEATURES, RANGES
from ml.evaluation import metrics
def demo_data(n=6000, seed=42):
    """Generate three genuine classes from parameter severity, not random labels."""
    rng=np.random.default_rng(seed); counts={'PASS':int(n*.45),'REWORK':int(n*.35)}; counts['REJECT']=n-counts['PASS']-counts['REWORK']; rows=[]
    def normal(): return {f:rng.normal((lo+hi)/2,(hi-lo)*.12) for f,(lo,hi) in RANGES.items()}
    def outside(row, feature, severity):
        low,high=RANGES[feature]; row[feature]=(low-severity*(high-low)) if rng.choice([-1,1])<0 else (high+severity*(high-low))
    for quality,count in counts.items():
        for _ in range(count):
            row=normal()
            if quality=='REWORK':
                for f in rng.choice(FEATURES,size=int(rng.integers(1,3)),replace=False): outside(row,f,float(rng.uniform(.08,.35)))
            elif quality=='REJECT':
                if rng.random()<.72: outside(row,rng.choice(FEATURES),float(rng.uniform(.65,1.50)))
                else:
                    for f in rng.choice(FEATURES,size=int(rng.integers(3,5)),replace=False): outside(row,f,float(rng.uniform(.30,.60)))
            row['Quality']=quality; rows.append(row)
    df=pd.DataFrame(rows); df.insert(0,'Product_ID',[f'CHG-{i:05d}' for i in range(1,n+1)])
    return df.sample(frac=1,random_state=seed).reset_index(drop=True)
def main():
    raw=ROOT/'data'/'raw'/'manufacturing_data.csv'; raw.parent.mkdir(parents=True,exist_ok=True); (ROOT/'data'/'processed').mkdir(parents=True,exist_ok=True); (ROOT/'models').mkdir(parents=True,exist_ok=True)
    # Regenerate to replace older two-class demo datasets.
    df=demo_data(); df.to_csv(raw,index=False); df.to_csv(ROOT/'data'/'processed'/'cleaned_data.csv',index=False)
    xtr,xte,ytr,yte=train_test_split(df[FEATURES],df.Quality,test_size=.2,stratify=df.Quality,random_state=42)
    choices={'Random Forest':Pipeline([('model',RandomForestClassifier(n_estimators=180,min_samples_leaf=2,class_weight='balanced',random_state=42))]),'Logistic Regression':Pipeline([('scale',StandardScaler()),('model',LogisticRegression(max_iter=1500,class_weight='balanced'))]),'Decision Tree':Pipeline([('model',DecisionTreeClassifier(class_weight='balanced',random_state=42))])}; results={}
    for name,m in choices.items(): m.fit(xtr,ytr); results[name]=metrics(yte,m.predict(xte))
    winner=max(results,key=lambda k:results[k]['f1_score']); model=choices[winner]; joblib.dump(model,ROOT/'models'/'quality_model.pkl')
    distribution={k:int(v) for k,v in df.Quality.value_counts().reindex(['PASS','REWORK','REJECT']).items()}
    # Keep the UI/metadata in the required manufacturing workflow order. sklearn
    # maintains its own alphabetical model.classes_ order, recorded separately.
    meta={'model_name':winner,'training_date':pd.Timestamp.now().isoformat(),'feature_names':FEATURES,'target_classes':['PASS','REWORK','REJECT'],'model_class_order':list(model.classes_),'dataset_size':len(df),'class_distribution':distribution,'metrics':results[winner],'model_comparison':results}; (ROOT/'models'/'model_metadata.json').write_text(json.dumps(meta,indent=2))
    print(f"Class distribution: {distribution}"); print(f"target_classes: {meta['target_classes']}"); print('Model comparison:')
    for name,result in results.items(): print(f"  {name}: accuracy={result['accuracy']:.4f}, precision={result['precision']:.4f}, recall={result['recall']:.4f}, f1={result['f1_score']:.4f}")
    print(f"Selected model: {winner}")
if __name__=='__main__': main()
