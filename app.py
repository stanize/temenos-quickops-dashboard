import streamlit as st
from core import jboss

st.set_page_config(page_title="Temenos QuickOps", layout="centered")

# Init auth state (even if not used yet)
if "auth" not in st.session_state:
    st.session_state["auth"] = {"logged_in": False, "user": None}

SERVICE = "jboss"

# ROUTER
if not jboss.is_active(SERVICE):
    st.switch_page("pages/0_Start_JBoss.py")
else:
    st.switch_page("pages/1_Login.py")

