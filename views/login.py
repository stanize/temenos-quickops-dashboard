import streamlit as st
import yaml

from core.ofs_client import enquiry_dates_list

def _load_cfg():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def render():
    st.subheader("Login")

    cfg = _load_cfg()
    endpoint = cfg["auth"]["ofs"]["endpoint"]
    timeout = int(cfg["auth"]["ofs"].get("timeout_seconds", 10))
    enquiry_name = cfg["auth"]["ofs"].get("enquiry_dates_list", "DATES.LIST")

    # secret (not in repo)
    basic_auth_b64 = st.secrets["ofs_basic_auth_b64"]

    with st.form("login_form"):
        username = st.text_input("Username").strip().upper()
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not username or not password:
            st.error("Enter username and password.")
            return

        # DO NOT log/display password anywhere
        res = enquiry_dates_list(
            endpoint=endpoint,
            basic_auth_b64=basic_auth_b64,
            user=username,
            password=password,
            enquiry_name=enquiry_name,
            timeout_seconds=timeout,
        )

        if res.ok:
            st.session_state["auth"] = {"logged_in": True, "user": username}
            st.session_state["transact_date"] = res.transact_date  # optional
            st.success(f"Login OK. Transact date: {res.transact_date or 'N/A'}")
            st.rerun()
        else:
            # Helpful but safe error display
            msg = res.error or "Login failed."
            st.error(msg)

            # Optional: show status code + truncated response for troubleshooting
            with st.expander("Debug"):
                st.write("status_code:", res.status_code)
                st.code((res.ofs_response or "")[:1500])
