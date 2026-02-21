import streamlit as st
from core.auth import dummy_validate

def render():
    st.subheader("Login (dummy)")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        res = dummy_validate(username, password)
        if res.ok:
            st.session_state["auth"] = {"logged_in": True, "user": username.strip().upper()}
            st.success("Login successful. Reloading...")
            st.rerun()
        else:
            st.error(res.message)
