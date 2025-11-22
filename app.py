
import streamlit as st

# Set mobile zoom to 47% (must be at the very top)
st.markdown(
    """
    <head>
        <meta name='viewport' content='width=device-width, initial-scale=0.47, maximum-scale=1.0, user-scalable=yes'>
    </head>
    """,
    unsafe_allow_html=True,
)

from utils.loader import load_json
from utils.theme import apply_theme



# Set mobile zoom to 47%
st.markdown(
    """
    <meta name='viewport' content='width=device-width, initial-scale=0.47, maximum-scale=1.0, user-scalable=yes'>
    """,
    unsafe_allow_html=True,
)
apply_theme()

if "auth" not in st.session_state:
    st.session_state["auth"] = False

sales = load_json("sales.json")

st.markdown(
    """
    <div class="glass glass-strong animate-pop" style="padding: 26px; margin-bottom: 18px;">
        <div class="pill">Executive Preview</div>
        <h2 style="margin: 6px 0 4px;">Larc Cafe — Intelligent Control Room</h2>
        <p style="color:#9fb0c7; margin-top: 0;">AI-first oversight, instant profit clarity, and a premium Apple-style experience.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Today Revenue (AED)", f"{sales['today_sales']:,.0f}")
with col2:
    st.metric("Orders Today", f"{sales['orders_today']:,}")
with col3:
    st.metric("Avg Ticket (AED)", f"{sales['avg_ticket']:,.2f}")
with col4:
    st.metric("Profit Margin (%)", f"{sales['profit_margin']*100:.1f}%")

cta_col, info_col = st.columns([1.3, 1])
with cta_col:
    st.markdown(
        """
        <div class="glass animate-pop" style="margin-top: 18px; padding: 22px;">
            <h3 style="margin-top:0;">Experience the Executive Suite</h3>
            <p style="color:#9fb0c7;">Secure login unlocks AI-driven insights, inventory brain, QR menu, and POS Lite demos.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    action_label = "Go to Dashboard" if st.session_state["auth"] else "Proceed to Secure Login"
    if st.button(action_label, use_container_width=True):
        target = "pages/2_Executive_Dashboard.py" if st.session_state["auth"] else "pages/1_Login.py"
        st.switch_page(target)

with info_col:
    st.markdown(
        """
        <div class="glass animate-pop" style="margin-top: 18px;">
            <div class="pill" style="background: rgba(224,180,85,0.12); color: #ffd78a; border-color: rgba(224,180,85,0.5);">Demo Mode</div>
            <ul style="color:#9fb0c7; margin-top: 10px;">
                <li>All figures in AED</li>
                <li>Data loaded from local JSON — no backend</li>
                <li>AI previews from IntaAgent™ engine</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
