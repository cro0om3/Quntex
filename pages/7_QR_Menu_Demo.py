import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access QR Menu demo.")
    st.switch_page("pages/1_Login.py")

products = load_json("products.json")

if "qr_cart" not in st.session_state:
    st.session_state["qr_cart"] = []
if "qr_modal" not in st.session_state:
    st.session_state["qr_modal"] = None


def categorize(name: str) -> str:
    if "Cold" in name:
        return "Cold Drinks"
    if "Latte" in name:
        return "Coffee"
    return "Featured"


for prod in products:
    prod["category"] = categorize(prod["name"])

st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding: 18px;">
        <div class="pill">QR Menu Demo</div>
        <h2 style="margin: 6px 0;">Beautiful mobile-first ordering</h2>
        <p style="color:#9fb0c7; margin:0;">Tap items, add to cart, and trigger demo checkout — all prices in AED.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

categories = sorted(set(prod["category"] for prod in products))
tabs = st.tabs(categories)

for tab, cat in zip(tabs, categories):
    with tab:
        cat_items = [p for p in products if p["category"] == cat]
        cols = st.columns(3)
        for idx, item in enumerate(cat_items):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="glass animate-pop" style="padding: 14px; min-height: 160px;">
                        <div style="width: 100%; height: 90px; border-radius: 12px; background: linear-gradient(135deg, rgba(27,118,255,0.25), rgba(224,180,85,0.25)); margin-bottom: 10px;"></div>
                        <strong>{item['name']}</strong><br/>
                        <span style="color:#9fb0c7;">AED {item['price']:.2f}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Add {item['name']}", key=f"add_{cat}_{idx}", use_container_width=True):
                    st.session_state["qr_modal"] = item

if st.session_state["qr_modal"]:
    item = st.session_state["qr_modal"]
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
        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, step=1, key="qr_qty")
        note = st.text_input("Note to barista (optional)", key="qr_note")
        add_col, cancel_col = st.columns(2)
        with add_col:
            if st.button("Add to cart", use_container_width=True, key="qr_add_btn"):
                st.session_state["qr_cart"].append({"item": item["name"], "qty": qty, "price": item["price"], "note": note})
                st.session_state["qr_modal"] = None
                st.success("Added to cart.")
        with cancel_col:
            if st.button("Cancel", use_container_width=True, key="qr_cancel_btn"):
                st.session_state["qr_modal"] = None

st.markdown("### Cart Preview")
total = sum(line["qty"] * line["price"] for line in st.session_state["qr_cart"])
for line in st.session_state["qr_cart"]:
    st.markdown(f"- {line['qty']} × {line['item']} — AED {line['qty']*line['price']:.2f}")
st.markdown(f"**Total: AED {total:.2f}**")

if st.button("Place order (DEMO MODE)", use_container_width=True):
    st.success("Order placed (DEMO MODE) — this simulates the customer flow.")
    st.session_state["qr_cart"] = []
