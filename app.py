import streamlit as st

# Redirect immediately to the main dashboard page
st.set_page_config(initial_sidebar_state="collapsed")
st.switch_page("pages/transact_dashboard.py")
