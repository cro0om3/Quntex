import streamlit as st

from utils.theme import apply_theme


apply_theme()

st.sidebar.empty()

PIN_CODE = "2025"

if st.session_state.get("auth"):
    st.switch_page("pages/2_Executive_Dashboard.py")

st.markdown(    
    """
    <style>
    body, .stApp { background: radial-gradient(circle at 50% 20%, rgba(27,118,255,0.18), rgba(8,17,35,0.92)), #0b1324; }
    .login-card { width:480px; margin:0 auto; border-radius:22px; padding:32px; border:1px solid rgba(224,180,85,0.35); box-shadow: 0 18px 40px rgba(0,0,0,0.35); background: rgba(15,24,41,0.85); backdrop-filter: blur(18px); }
    .shake { animation: shake 0.3s linear; }
    @keyframes shake { 0% { transform: translateX(0);} 25% { transform: translateX(-6px);} 50% { transform: translateX(6px);} 75% { transform: translateX(-4px);} 100% { transform: translateX(0);} }
    .input-helper { color:#9fb0c7; font-size:12px; text-align:right; margin-top:-6px; }
    .pin-dots { letter-spacing: 8px; font-family: monospace; text-align:center; color:#e0b455; }
    .pin-input input { text-align:center; font-family: monospace; letter-spacing: 2px; }
    </style>
    """,
    unsafe_allow_html=True,
)

logo_path = "assets/qx/qx_icon.svg"
st.markdown(
    f"""
    <div style="text-align:center; margin-top:12px;">
        <img src="{logo_path}" width="86" style="filter: drop-shadow(0 4px 12px rgba(27,118,255,0.5));" />
        <h2 style="margin:8px 0 2px;">Welcome to Qx Suite</h2>
        <p style="color: rgba(255,255,255,0.7); margin:0;">Your café’s command center</p>
    </div>
    """,
    unsafe_allow_html=True,
)

form_error = False
wrong_pin = False
pin_error = False
name_error = False

with st.form("login_form"):
    st.markdown("<div class='login-card glow-border animate-pop'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:12px;">
            <h3 style="margin:4px 0;">Staff Authentication</h3>
            <div style="color: rgba(255,255,255,0.75); font-size:13px;">Enter your 4-digit PIN to access Qx Suite.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    pin = st.text_input(
        "PIN",
        type="password",
        placeholder="••••",
        max_chars=4,
        help="4-digit staff PIN",
        key="login_pin",
        label_visibility="collapsed",
    )
    st.markdown(f"<div class='input-helper'>4-digit staff PIN</div>", unsafe_allow_html=True)

    dots = "•" * len(pin)
    dots_display = (dots + " " * 4)[:4]
    st.markdown(f"<div class='pin-dots'>{dots_display}</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("Enter Suite", use_container_width=True)
    auto_submit = len(pin) == 4 and not submitted
    if submitted or auto_submit:
        if len(pin) < 4:
            form_error = True
            pin_error = True
        else:
            if pin == PIN_CODE:
                st.session_state["auth"] = True
                st.success("Access granted. Redirecting to Executive Dashboard...")
                st.switch_page("pages/2_Executive_Dashboard.py")
            else:
                form_error = True
                wrong_pin = True

    st.markdown(
        """
        <div style="margin-top:12px; text-align:center; font-size:12px; color:#9fb0c7;">
            Your session is secured and stored locally only.
        </div>
        """,
        unsafe_allow_html=True,
    )
    qr_open = st.form_submit_button("Scan to Login (Demo)")
    if qr_open:
        with st.container():
            st.markdown(
                """
                <div class="glass glass-strong" style="padding:12px; text-align:center; margin-top:8px;">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=QX_LOGIN_DEMO" />
                    <p style="color:#9fb0c7; margin:6px 0;">Scan this QR to auto-fill your credentials (demo).</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    if name_error:
        st.error("Name is required")
    if pin_error:
        st.error("Enter 4 digits")
    if wrong_pin:
        st.error("Incorrect PIN")
    st.markdown("</div>", unsafe_allow_html=True)
