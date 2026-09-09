import pandas as pd, streamlit as st
from utils.config import FEATURES, RANGES
from utils.database import add_prediction
from ml.predict import predict_frame
from utils.pdf_generator import report_pdf
def render_product_prediction(user_id):
    st.title("Product Quality Prediction"); st.caption("Enter measured parameters. The score is model-derived PASS probability, not a certified measurement.")
    with st.form("single_prediction"):
        product_id=st.text_input("Product ID",placeholder="CHG-001"); values={}; cols=st.columns(2)
        for i,f in enumerate(FEATURES):
            lo,hi=RANGES[f]; values[f]=cols[i%2].number_input(f.replace('_',' '),min_value=0.0,value=float((lo+hi)/2),step=0.01,help=f"Configured reference range: {lo}–{hi}")
        submit=st.form_submit_button("PREDICT PRODUCT QUALITY")
    if submit:
        if not product_id.strip(): st.error("Product ID is required."); return
        df=pd.DataFrame([{"Product_ID":product_id.strip(),**values}]); result=predict_frame(df).iloc[0].to_dict(); add_prediction(user_id,df.iloc[0],result)
        status=result['Prediction'].lower(); st.markdown(f'<div class="status {status}">{result["Prediction"]} · Quality score: {result["Quality_Score"]:.1f}%</div>',unsafe_allow_html=True)
        st.progress(int(result['Quality_Score'])); a,b=st.columns(2); a.metric("Product ID",product_id); b.metric("Status",result['Prediction']); st.subheader("Reason"); st.write(result['Reason']); st.subheader("Suggested action"); st.write(result['Suggested_Action'])
        lines=[f"Product ID: {product_id}",f"Prediction: {result['Prediction']}",f"Quality score: {result['Quality_Score']:.1f}%","","Input parameters:"]+[f"{f}: {values[f]}" for f in FEATURES]+["",f"Reason: {result['Reason']}",f"Suggested Action: {result['Suggested_Action']}"]
        st.download_button("Download individual PDF report",report_pdf("AI PRODUCT QUALITY REPORT",lines),file_name=f"{product_id}_quality_report.pdf",mime="application/pdf")
