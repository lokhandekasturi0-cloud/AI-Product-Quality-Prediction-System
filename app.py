import streamlit as st
from utils.database import init_db
from utils.authentication import login, signup
from internal_pages.dashboard import render_dashboard
from internal_pages.product_prediction import render_product_prediction
from internal_pages.bulk_prediction import render_bulk_prediction
from internal_pages.history import render_history
from internal_pages.analytics import render_analytics
from internal_pages.reports import render_reports
from internal_pages.profile import render_profile

st.set_page_config(page_title="AI Quality Predictor",page_icon="⚡",layout="wide",initial_sidebar_state="expanded")
init_db()
st.markdown('''<style>
.block-container{max-width:1400px;padding-top:1.7rem}.status{border-radius:10px;padding:1rem;font-weight:700}.pass{background:#dcfce7;color:#166534}.rework{background:#fef3c7;color:#92400e}.reject{background:#fee2e2;color:#991b1b}@media(max-width:650px){.block-container{padding:1rem .75rem}div[data-testid="stHorizontalBlock"]{flex-wrap:wrap}.stButton>button{width:100%;min-height:44px}}</style>''',unsafe_allow_html=True)
def auth_screen():
    st.title("⚡ AI Product Quality Prediction")
    st.caption("AI-assisted early quality prediction and decision support for electronics manufacturing.")
    tab1,tab2=st.tabs(["Sign in","Create account"])
    with tab1:
        with st.form("login"):
            email=st.text_input("Email"); password=st.text_input("Password",type="password"); go=st.form_submit_button("Sign in")
        if go:
            user=login(email,password)
            if user: st.session_state.user=user; st.session_state.user_id=user['id']; st.rerun()
            st.error("Incorrect email or password.") if not user else None
    with tab2:
        with st.form("signup"):
            name=st.text_input("Full name"); email=st.text_input("Email",key="new_email"); password=st.text_input("Password",type="password",key="new_password"); confirm=st.text_input("Confirm password",type="password"); go=st.form_submit_button("Create account")
        if go:
            ok,msg=signup(name,email,password,confirm); (st.success if ok else st.error)(msg)
if "user" not in st.session_state: auth_screen(); st.stop()
user=st.session_state.user
with st.sidebar:
    st.title("⚡ Quality AI"); st.caption(user['name'])
    page=st.radio("Navigation",["🏠 Dashboard","📦 Product Prediction","📁 Bulk Prediction","📊 Analytics","📜 Prediction History","📄 Reports","👤 Profile"],label_visibility="collapsed")
    if st.button("🚪 Logout"): st.session_state.pop("user",None); st.session_state.pop("user_id",None); st.rerun()
renderers={"🏠 Dashboard":render_dashboard,"📦 Product Prediction":render_product_prediction,"📁 Bulk Prediction":render_bulk_prediction,"📊 Analytics":render_analytics,"📜 Prediction History":render_history,"📄 Reports":render_reports,"👤 Profile":render_profile}
renderers[page](st.session_state.user_id)
