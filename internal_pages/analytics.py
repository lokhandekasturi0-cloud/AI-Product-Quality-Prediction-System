import plotly.express as px, streamlit as st
from ml.predict import load_model, metadata
from ml.feature_importance import importance
def render_analytics(user_id):
    st.title("Analytics & Model Performance"); meta=metadata(); st.caption(f"Active model: {meta['model_name']} · trained {meta['training_date'][:10]}")
    cols=st.columns(4)
    for c,(k,v) in zip(cols,meta['metrics'].items()): c.metric(k.replace('_',' ').title(),f"{v*100:.1f}%")
    st.subheader("Model comparison"); st.dataframe(meta['model_comparison'],width="stretch")
    st.subheader("Feature importance"); base=load_model(); model=base.named_steps.get('model',base); imp=importance(model)
    if imp.Importance.sum()==0: st.info("The selected model does not expose feature importance.")
    else: st.plotly_chart(px.bar(imp,x='Importance',y='Feature',orientation='h',title='Most influential manufacturing parameters'),width="stretch")
