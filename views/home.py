import streamlit as st

def render():
    st.subheader("Home")
    st.success(f"Logged in as {st.session_state['auth']['user']}")

    if st.button("Logout", use_container_width=True):
        st.session_state["auth"] = {"logged_in": False, "user": None}
        st.rerun()

    st.info("Next: add authenticated-only JBoss restart.")
