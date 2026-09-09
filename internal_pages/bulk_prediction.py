import pandas as pd, streamlit as st
from utils.validation import validate_frame
from ml.predict import predict_frame
from utils.database import add_prediction
from utils.pdf_generator import report_pdf
def render_bulk_prediction(user_id):
    st.title("Bulk Product Prediction"); upload=st.file_uploader("Upload Manufacturing Dataset",type=["csv","xlsx","xls"])
    if not upload: st.info("Expected: Product_ID, Temperature, Voltage, Current, Weight, Pressure, Humidity, Machine_Speed."); return
    try: df=pd.read_csv(upload) if upload.name.lower().endswith('.csv') else pd.read_excel(upload)
    except Exception: st.error("Could not read that file. Upload a valid CSV or Excel workbook."); return
    ok,data=validate_frame(df)
    if not ok: st.error(data); return
    st.success(f"Validated {len(data):,} products.")
    if st.button("Run batch prediction"):
        with st.spinner("Processing the complete dataset..."):
            result=predict_frame(data)
            for _,row in result.iterrows(): add_prediction(user_id,row,row)
        st.session_state.bulk_result=result
    result=st.session_state.get('bulk_result')
    if result is not None:
        counts=result.Prediction.value_counts(); cols=st.columns(5)
        for c,(label,value) in zip(cols,[("Total",len(result)),("PASS",counts.get('PASS',0)),("REWORK",counts.get('REWORK',0)),("REJECT",counts.get('REJECT',0)),("Avg. score",f"{result.Quality_Score.mean():.1f}%")]): c.metric(label,value)
        st.dataframe(result[["Product_ID","Quality_Score","Prediction","Reason","Suggested_Action"]],use_container_width=True,height=420)
        st.download_button("Download results as CSV",result.to_csv(index=False).encode(),"quality_predictions.csv","text/csv")
        lines=[f"Total products: {len(result)}",f"PASS: {counts.get('PASS',0)}",f"REWORK: {counts.get('REWORK',0)}",f"REJECT: {counts.get('REJECT',0)}",f"Pass rate: {counts.get('PASS',0)/len(result)*100:.1f}%",f"Average quality score: {result.Quality_Score.mean():.1f}%"]
        st.download_button("Download summary PDF",report_pdf("AI PRODUCT QUALITY BULK SUMMARY",lines),"bulk_quality_summary.pdf","application/pdf")
