import streamlit as st

from utils.theme import apply_theme


apply_theme()

st.sidebar.empty()

PIN_CODE = "2025"

if st.session_state.get("auth"):
    st.switch_page("pages/2_Executive_Dashboard.py")

st.markdown("<div style='height:6vh'></div>", unsafe_allow_html=True)

center = st.container()
col_a, col_b, col_c = st.columns([1, 1.3, 1])
with col_b:
    st.markdown(
        """
        <div class="glass glow-border animate-pop" style="width: 100%; text-align:center; padding: 28px 30px;">
            <div class="pill" style="background: rgba(27,118,255,0.12);">Secure Access</div>
            <h2 style="margin-bottom: 6px;">Welcome to Lark Executive Suite</h2>
            <p style="color:#9fb0c7; margin-top:0;">Secure Access for Management Only</p>
            <div class="divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("login_form"):
        st.markdown("<div class='glass glass-strong' style='padding: 16px;'>", unsafe_allow_html=True)
        pin_raw = st.text_input("Enter PIN", type="password", placeholder="0000", max_chars=6, help="Digits only")
        pin = "".join(ch for ch in pin_raw if ch.isdigit())
        submitted = st.form_submit_button("Enter Suite")
        if submitted:
            if not pin:
                st.error("Enter the numeric PIN.")
            elif pin == PIN_CODE:
                st.session_state["auth"] = True
                st.success("Access granted. Redirecting to Executive Dashboard...")
                st.switch_page("pages/2_Executive_Dashboard.py")
            else:
                st.error("Incorrect PIN. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)
