import streamlit as st
from utils.database import history
from utils.pdf_generator import report_pdf
def render_reports(user_id):
    st.title("Reports"); rows=history(user_id)
    if not rows: st.info("Reports become available after predictions are made."); return
    r=rows[0]; lines=[f"Product ID: {r['product_id']}",f"Date: {r['prediction_date']}",f"Quality score: {r['quality_score']:.1f}%",f"Status: {r['prediction']}",f"Reason: {r['reason']}",f"Suggested action: {r['suggested_action']}"]
    st.download_button("Download latest individual report",report_pdf("AI PRODUCT QUALITY REPORT",lines),"latest_quality_report.pdf","application/pdf")
