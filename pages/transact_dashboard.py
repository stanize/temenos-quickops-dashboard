import streamlit as st
from core import jboss
from views import start_jboss, login, home

st.set_page_config(page_title="Temenos QuickOps", layout="centered")
st.title("Temenos QuickOps")

SERVICE = "jboss"

# Session initialization
if "auth" not in st.session_state:
    st.session_state["auth"] = {"logged_in": False, "user": None}

# Evaluate platform state
active = jboss.is_active(SERVICE)

st.metric("JBoss", "RUNNING" if active else "DOWN")
st.divider()

# ROUTER FLOW:
# 1) If JBoss DOWN -> show anonymous start view
# 2) If JBoss UP but not logged in -> show login view
# 3) If logged in -> show home view
if not active:
    start_jboss.render()
elif not st.session_state["auth"]["logged_in"]:
    login.render()
else:
    home.render()

