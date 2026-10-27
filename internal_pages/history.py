import pandas as pd, streamlit as st
from utils.database import history
def render_history(user_id):
    st.title("Prediction History"); df=pd.DataFrame(history(user_id))
    if df.empty: st.info("No saved predictions yet."); return
    statuses=st.multiselect("Status",sorted(df.prediction.unique()),default=sorted(df.prediction.unique())); search=st.text_input("Product ID contains")
    filtered=df[df.prediction.isin(statuses) & df.product_id.astype(str).str.contains(search,case=False,na=False)]
    st.dataframe(filtered[['prediction_date','product_id','quality_score','prediction','reason','suggested_action']],width="stretch")
    st.download_button("Export history as CSV",filtered.to_csv(index=False).encode(),"prediction_history.csv","text/csv")
