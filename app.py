import streamlit as st

st.set_page_config(page_title="Temenos QuickOps", layout="centered")

# Initialize session auth state
if "auth" not in st.session_state:
    st.session_state["auth"] = {"logged_in": False, "user": None}

# Guard: must be logged in
if not st.session_state["auth"]["logged_in"]:
    st.switch_page("pages/1_Login.py")

st.title("Temenos QuickOps")
st.write(f"✅ Logged in as: **{st.session_state['auth']['user']}**")

if st.button("Logout"):
    st.session_state["auth"] = {"logged_in": False, "user": None}
    st.switch_page("pages/1_Login.py")

st.info("Next: add JBoss status + restart page.")
