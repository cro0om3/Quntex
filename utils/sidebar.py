from pathlib import Path

import streamlit as st

NAV_ITEMS = [
    ("Executive Dashboard", "pages/2_Executive_Dashboard.py"),
    ("Qx Intelligence", "pages/3_IntaAgent_AI.py"),
    ("Inventory Brain", "pages/4_Inventory_Brain.py"),
    ("Products Cost", "pages/5_Products_Cost.py"),
    ("Executive Reports", "pages/6_Executive_Reports.py"),
    ("POS Lite", "pages/8_POS_Lite.py"),
    ("QR Menu", "pages/7_QR_Menu_Demo.py"),
    ("Settings", "pages/9_Settings.py"),
]


def render_sidebar():
    """Render branded sidebar with navigation buttons."""
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "lark_logo.png"
    st.sidebar.markdown(
        "<div style='padding: 8px 6px; color: #c5d4ec; font-weight: 700; letter-spacing: 0.4px; border: 1px solid rgba(224,180,85,0.45); border-radius: 12px; text-align:center;'>"
        "Lark Executive Suite</div>",
        unsafe_allow_html=True,
    )
    if logo_path.exists():
        try:
            st.sidebar.image(str(logo_path), width=140)
        except Exception:
            st.sidebar.markdown("<div style='color:#9fb0c7;'>Lark Cafe</div>", unsafe_allow_html=True)
    st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.session_state.setdefault("accent_color", "Blue")
    st.sidebar.markdown("**Accent Color**")
    accent = st.sidebar.radio(
        "Pick accent",
        ["Blue", "Gold"],
        index=0 if st.session_state["accent_color"] == "Blue" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state["accent_color"] = accent
    st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    active = st.session_state.get("active_page")
    for label, target in NAV_ITEMS:
        is_active = active == label
        btn_container = st.sidebar.container()
        if btn_container.button(label, use_container_width=True, key=f"nav_{label}"):
            st.session_state["active_page"] = label
            st.switch_page(target)
        if is_active:
            btn_container.markdown("<div style='height:2px; background:#E0B455; border-radius:999px; margin-top:-6px;'></div>", unsafe_allow_html=True)

    st.sidebar.markdown(
        "<div style='margin-top: 28px; font-size: 12px; color: #7c8a9d;'>Powered by Quantex — QX Active</div>",
        unsafe_allow_html=True,
    )
