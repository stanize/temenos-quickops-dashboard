import time
import streamlit as st
from core import jboss

SERVICE = "jboss"
COOLDOWN_SECONDS = 300  # 5 minutes

def render():
    st.subheader("JBoss is DOWN")
    st.warning("JBoss is not running. You can start it without login.")

    if "start_last_ts" not in st.session_state:
        st.session_state["start_last_ts"] = 0.0

    with st.expander("systemctl status"):
        r = jboss.status(SERVICE)
        st.code(r.stdout or r.stderr or "(no output)")

    now = time.time()
    remaining = int(max(0, COOLDOWN_SECONDS - (now - st.session_state["start_last_ts"])))
    disabled = remaining > 0

    if disabled:
        st.info(f"Start cooldown active. Try again in {remaining}s.")

    if st.button("Start JBoss (anonymous)", type="primary", disabled=disabled, use_container_width=True):
        res = jboss.start(SERVICE)
        st.session_state["start_last_ts"] = time.time()

        if res.ok:
            st.success("Start triggered. Reloading...")
        else:
            st.error(f"Start failed (rc={res.returncode}).")

        st.code((res.stdout + "\n" + res.stderr).strip() or "(no output)")
        time.sleep(2)
        st.rerun()
