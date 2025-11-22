import uuid

import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access POS Lite.")
    st.switch_page("pages/1_Login.py")

products = load_json("products.json")

if "pos_cart" not in st.session_state:
    st.session_state["pos_cart"] = []
if "pos_modal" not in st.session_state:
    st.session_state["pos_modal"] = None
if "pos_receipt" not in st.session_state:
    st.session_state["pos_receipt"] = None

st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding: 18px;">
        <div class="pill">POS Lite</div>
        <h2 style="margin: 6px 0;">Modern cashier flow</h2>
        <p style="color:#9fb0c7; margin:0;">Add to cart, quick charge, instant receipt preview — demo mode only.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(3)
for idx, item in enumerate(products):
    with cols[idx % 3]:
        st.markdown(
            f"""
            <div class="glass animate-pop" style="padding: 14px; min-height: 150px;">
                <strong>{item['name']}</strong><br/>
                <span style="color:#9fb0c7;">AED {item['price']:.2f}</span>
                <p style="margin-top: 6px; color:#6fa8ff;">Touch to add</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"Add {item['name']}", key=f"pos_add_{idx}", use_container_width=True):
            st.session_state["pos_modal"] = item

if st.session_state["pos_modal"]:
    item = st.session_state["pos_modal"]
    with st.container():
        st.markdown(
            f"""
            <div class="glass glass-strong glow-border animate-pop" style="padding:16px; margin-top:8px;">
                <div class="pill" style="background: rgba(27,118,255,0.14);">Add Item</div>
                <h4 style="margin:6px 0;">{item['name']}</h4>
                <p style="color:#9fb0c7; margin:0;">AED {item['price']:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, step=1, key="pos_qty")
        add_col, cancel_col = st.columns(2)
        with add_col:
            if st.button("Add to cart", use_container_width=True, key="pos_add_btn"):
                st.session_state["pos_cart"].append({"item": item["name"], "qty": qty, "price": item["price"]})
                st.session_state["pos_modal"] = None
        with cancel_col:
            if st.button("Cancel", use_container_width=True, key="pos_cancel_btn"):
                st.session_state["pos_modal"] = None

st.markdown("### Cart")
total = sum(line["qty"] * line["price"] for line in st.session_state["pos_cart"])
for line in st.session_state["pos_cart"]:
    st.markdown(f"- {line['qty']} × {line['item']} — AED {line['qty']*line['price']:.2f}")
st.markdown(f"**Total: AED {total:.2f}**")

if st.button("Charge (DEMO)", use_container_width=True):
    st.session_state["pos_receipt"] = {
        "id": str(uuid.uuid4())[:8].upper(),
        "total": total,
        "items": list(st.session_state["pos_cart"]),
    }
    st.session_state["pos_cart"] = []
    st.success("Payment accepted — demo success.")

if st.session_state["pos_receipt"]:
    receipt = st.session_state["pos_receipt"]
    st.markdown("### Receipt Preview")
    st.markdown(f"Receipt ID: `{receipt['id']}`")
    for line in receipt["items"]:
        st.markdown(f"- {line['qty']} × {line['item']} — AED {line['qty']*line['price']:.2f}")
    st.markdown(f"**Paid: AED {receipt['total']:.2f}**")
