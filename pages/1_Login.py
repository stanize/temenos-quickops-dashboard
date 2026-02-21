import streamlit as st
from core.auth import dummy_validate

st.set_page_config(page_title="Login - Temenos QuickOps", layout="centered")

st.title("Temenos QuickOps")
st.subheader("Login (dummy)")

# Initialize session auth state
if "auth" not in st.session_state:
    st.session_state["auth"] = {"logged_in": False, "user": None}

# If already logged in, go to home
if st.session_state["auth"]["logged_in"]:
    st.success(f"Already logged in as {st.session_state['auth']['user']}")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

with st.form("login_form"):
    username = st.text_input("Username", placeholder="e.g. IGNATIUS")
    password = st.text_input("Password", type="password", placeholder="demo123")
    submitted = st.form_submit_button("Login")

if submitted:
    res = dummy_validate(username, password)
    if res.ok:
        st.session_state["auth"] = {"logged_in": True, "user": username.strip().upper()}
        st.success(res.message)
        st.switch_page("app.py")
    else:
        st.error(res.message)
