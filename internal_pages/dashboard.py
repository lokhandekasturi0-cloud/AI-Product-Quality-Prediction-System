import pandas as pd, plotly.express as px, streamlit as st
from utils.database import history
def render_dashboard(user_id):
    st.title("Quality Operations Dashboard"); rows=history(user_id)
    if not rows: st.info("No prediction data available yet. Start by making your first product quality prediction."); return
    df=pd.DataFrame(rows); df.prediction_date=pd.to_datetime(df.prediction_date); counts=df.prediction.value_counts(); cols=st.columns(6)
    values=[("Total Predictions",len(df)),("PASS Products",counts.get('PASS',0)),("REWORK Products",counts.get('REWORK',0)),("REJECT Products",counts.get('REJECT',0)),("Average Score",f"{df.quality_score.mean():.1f}%"),("Pass Rate",f"{counts.get('PASS',0)/len(df)*100:.1f}%")]
    for c,(label,value) in zip(cols,values): c.metric(label,value)
    left,right=st.columns(2); left.plotly_chart(px.pie(df,names='prediction',title='Prediction distribution',hole=.45),width="stretch"); right.plotly_chart(px.histogram(df,x='quality_score',nbins=20,title='Quality-score distribution'),width="stretch")
    trend=df.groupby(df.prediction_date.dt.date).size().reset_index(name='Predictions'); st.plotly_chart(px.line(trend,x='prediction_date',y='Predictions',markers=True,title='Predictions over time'),width="stretch")
