"""The only Streamlit automatic page: a safe persistent account entry point."""
import streamlit as st
from utils.database import init_db
from internal_pages.profile import render_profile

init_db()
if "user_id" not in st.session_state:
    st.title("Profile")
    st.info("Please log in to view your profile.")
else:
    render_profile(st.session_state.user_id)
