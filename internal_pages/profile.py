import pandas as pd
import streamlit as st
from utils.database import history, update_name, user_by_id

def render_profile(user_id):
    """Render a freshly queried, user-scoped profile from SQLite."""
    user=user_by_id(user_id)
    if not user:
        st.title("Profile"); st.info("Please log in to view your profile."); return
    # Refresh the sidebar's current-user object from the same persisted account.
    st.session_state.user=user
    st.session_state.user_id=user['id']
    st.title("Profile")
    st.subheader("👤 Account Information")
    st.write(f"**Full Name:** {user['name']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Account Created:** {user['created_at']}")
    name=st.text_input("Full name",value=user['name'])
    if st.button("Update name"):
        if name.strip():
            update_name(user['id'],name.strip()); st.session_state.user=user_by_id(user_id); st.success("Profile updated."); st.rerun()
        else: st.error("Name is required.")
    records=history(user_id)
    st.subheader("Prediction History")
    if not records:
        st.info("No predictions have been made for this account yet.")
        return
    df=pd.DataFrame(records); counts=df['prediction'].value_counts(); cols=st.columns(4)
    for col,label,value in zip(cols,["Total Predictions","PASS","REWORK","REJECT"],[len(df),counts.get('PASS',0),counts.get('REWORK',0),counts.get('REJECT',0)]): col.metric(label,value)
    st.dataframe(df[['prediction_date','product_id','quality_score','prediction','reason','suggested_action']],width="stretch")
