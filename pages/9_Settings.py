import streamlit as st

from utils.sidebar import render_sidebar
from utils.theme import apply_theme


apply_theme()
render_sidebar()

if "settings" not in st.session_state:
    st.session_state["settings"] = {
        "name": "Lark Cafe",
        "tax": 5.0,
        "service_charge": True,
        "logo": None,
    }
if "experience" not in st.session_state:
    st.session_state["experience"] = {"brightness": 70, "blur": 12, "accent": "Blue"}
st.session_state.setdefault("settings_saved", False)

if not st.session_state.get("auth"):
    st.warning("Please login to access Settings.")
    st.switch_page("pages/1_Login.py")

# Header
st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding: 20px; position: relative; overflow:hidden;">
        <div style="position:absolute; inset:0; background: linear-gradient(135deg, rgba(27,118,255,0.14), transparent); opacity:0.8;"></div>
        <div style="position:relative; z-index:1;">
            <div class="pill" style="background: rgba(27,118,255,0.16);">⚙️ Executive Settings</div>
            <h2 style="margin: 8px 0 4px;">Branding & Experience Control</h2>
            <p style="color:#9fb0c7; margin:0;">Your cafe branding controls how receipts, invoices, reports, and customer-facing screens appear.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.15, 1])

# LEFT COLUMN: Controls
with left:
    st.markdown(
        """
        <div class="glass glass-strong glow-border animate-pop" style="padding:16px;">
            <div class="pill" style="background: rgba(27,118,255,0.14);">Logo</div>
            <h4 style="margin:6px 0;">Upload / Manage</h4>
            <p style="color:#9fb0c7; margin:0 0 10px;">Your logo appears on reports, QR menu, and receipts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_logo = st.file_uploader("Drop your logo (PNG preferred, max 200MB)", type=["png", "jpg", "jpeg"])
    if uploaded_logo:
        if uploaded_logo.size > 200 * 1024 * 1024:
            st.error("File too large. Please upload up to 200MB.")
        else:
            st.session_state["settings"]["logo"] = uploaded_logo.getvalue()
            st.success("Logo captured in session.")
    if st.session_state["settings"]["logo"]:
        logo_cols = st.columns([1, 1])
        with logo_cols[0]:
            st.image(st.session_state["settings"]["logo"], caption="Preview", use_column_width=True)
        with logo_cols[1]:
            if st.button("Reset Logo", use_container_width=True):
                st.session_state["settings"]["logo"] = None
                st.info("Logo cleared (session only).")
    st.markdown("---")

    # Cafe name with validation + live preview hint
    st.markdown(
        "<div class='pill' style='background: rgba(224,180,85,0.14); color:#ffd78a;'>Cafe Identity</div>",
        unsafe_allow_html=True,
    )
    name_val = st.text_input(
        "Cafe Name",
        value=st.session_state["settings"]["name"],
        placeholder="Lark Cafe • Central Branch",
        help="Shown on receipts, reports, and POS.",
        key="name_input",
    )
    st.session_state["settings"]["name"] = name_val
    if len(name_val.strip()) < 3:
        st.warning("Name should be at least 3 characters.")
    st.markdown(f"<p style='color:#9fb0c7;'>Preview: <strong>{name_val or '—'}</strong></p>", unsafe_allow_html=True)

    # Tax slider with bubble
    st.markdown(
        "<div class='pill' style='background: rgba(27,118,255,0.14);'>Tax</div>",
        unsafe_allow_html=True,
    )
    tax_val = st.slider(
        "Tax %",
        0.0,
        20.0,
        value=float(st.session_state["settings"]["tax"]),
        step=0.1,
        help="Applied on receipts and POS totals.",
        key="tax_slider",
    )
    st.session_state["settings"]["tax"] = tax_val
    tax_color = "#1B76FF" if tax_val < 5 else ("#E0B455" if tax_val <= 10 else "#FF6B6B")
    st.markdown(
        f"""
        <div style="margin-top:-6px; margin-bottom:6px;">
            <span style="background:{tax_color}; color:#0b1324; padding:4px 10px; border-radius:12px; font-weight:600;">
                {tax_val:.2f}% Tax (AED calculated automatically)
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Service charge toggle
    st.markdown(
        "<div class='pill' style='background: rgba(27,118,255,0.14); margin-top:6px;'>Service Charge</div>",
        unsafe_allow_html=True,
    )
    svc = st.toggle(
        "Enable Service Charge",
        value=st.session_state["settings"]["service_charge"],
        help="Automatically added to dine-in orders. Not applied to QR or delivery.",
    )
    st.session_state["settings"]["service_charge"] = svc
    icon = "✅" if svc else "❌"
    note_color = "#c3f3de" if svc else "#ff8c8c"
    st.markdown(
        f"<p style='color:{note_color}; margin-top:2px;'>Status: {icon} {'Enabled' if svc else 'Disabled'}</p>",
        unsafe_allow_html=True,
    )

    # Experience options
    st.markdown("---")
    st.markdown(
        "<div class='pill' style='background: rgba(27,118,255,0.14);'>Experience Options</div>",
        unsafe_allow_html=True,
    )
    exp = st.session_state["experience"]
    exp["brightness"] = st.slider("Theme brightness", 0, 100, value=int(exp["brightness"]), step=5)
    exp["blur"] = st.slider("Blur intensity", 0, 20, value=int(exp["blur"]), step=1)
    exp["accent"] = st.selectbox("Accent color", ["Blue", "Purple", "Gold"], index=["Blue", "Purple", "Gold"].index(exp["accent"]))
    st.session_state["experience"] = exp

    if st.button("Apply Changes", use_container_width=True):
        st.session_state["settings_saved"] = True
        st.success("Branding Updated (session only)")
    else:
        st.session_state["settings_saved"] = False
    st.markdown("<p style='color:#9fb0c7; font-size:12px;'>Settings are demo-only and stored in session_state.</p>", unsafe_allow_html=True)

# RIGHT COLUMN: Preview
with right:
    st.markdown(
        """
        <div class="glass glass-strong glow-border animate-pop" style="padding:18px;">
            <div class="pill" style="background: rgba(224,180,85,0.16); color:#ffd78a;">Live Preview</div>
            <h4 style="margin:6px 0;">Executive Display</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='glass glass-strong animate-pop' style='padding:14px;'>", unsafe_allow_html=True)
    st.markdown(f"**Name:** {st.session_state['settings']['name']}")
    st.markdown(f"**Tax:** {st.session_state['settings']['tax']:.2f}%")
    st.markdown(f"**Service Charge:** {'Enabled' if st.session_state['settings']['service_charge'] else 'Disabled'}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass glass-strong glow-border animate-pop" style="padding:16px; margin-top:8px;">
            <div style="font-weight:700; margin-bottom:8px;">Mock Receipt</div>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state["settings"]["logo"]:
        st.image(st.session_state["settings"]["logo"], width=120)
    subtotal = 100.0
    tax_amt = subtotal * st.session_state["settings"]["tax"] / 100
    svc_amt = 5.0 if st.session_state["settings"]["service_charge"] else 0.0
    total = subtotal + tax_amt + svc_amt
    st.markdown(
        f"""
        <div style="color:#E8EEF9; margin-top:6px;">
            <div style="font-weight:700;">{st.session_state['settings']['name']}</div>
            <div style="color:#9fb0c7;">Order #0012 • Dine-in</div>
            <div style="margin-top:8px;">Subtotal ...... AED {subtotal:,.2f}</div>
            <div>Tax ({st.session_state['settings']['tax']:.2f}%) ..... AED {tax_amt:,.2f}</div>
            <div>Service Charge ..... {('AED ' + format(svc_amt, ',.2f')) if svc_amt else 'Not applied'}</div>
            <div style="margin-top:8px; font-weight:700;">Total ........ AED {total:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state["settings_saved"]:
        st.markdown(
            "<div class='glass' style='padding:12px; border:1px solid rgba(78,204,163,0.6); box-shadow:0 0 18px rgba(78,204,163,0.4); color:#c3f3de;'>"
            "✅ Branding Updated</div>",
            unsafe_allow_html=True,
        )
