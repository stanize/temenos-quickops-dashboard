import time
import streamlit as st
from core import jboss

st.set_page_config(page_title="Start JBoss", layout="centered")

SERVICE = "jboss"
COOLDOWN_SECONDS = 300  # 5 min

if "start_last_ts" not in st.session_state:
    st.session_state["start_last_ts"] = 0.0

active = jboss.is_active(SERVICE)

# Dynamic title
st.title("JBoss is RUNNING" if active else "JBoss is DOWN")

######

if active:
    st.success("JBoss is running now.")
    st.button("Continue", type="primary", on_click=lambda: st.switch_page("pages/1_Login.py"))
    st.stop()

st.warning("JBoss is not running. You can start it without login.")

with st.expander("systemctl status"):
    r = jboss.status(SERVICE)
    st.code(r.stdout or r.stderr or "(no output)")

now = time.time()
remaining = int(max(0, COOLDOWN_SECONDS - (now - st.session_state["start_last_ts"])))
disabled = remaining > 0

if disabled:
    st.info(f"Start cooldown active. Try again in {remaining}s.")

if st.button("Start JBoss (anonymous)", disabled=disabled, type="primary", use_container_width=True):
    res = jboss.start(SERVICE)
    st.session_state["start_last_ts"] = time.time()

    if res.ok:
        st.success("Start triggered. Checking status...")
    else:
        st.error(f"Start failed (rc={res.returncode}).")

    st.code((res.stdout + "\n" + res.stderr).strip() or "(no output)")
    st.rerun()

