import uuid

import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


def categorize(name: str) -> str:
    if "Cold" in name:
        return "Cold Drinks"
    if "Latte" in name:
        return "Coffee"
    return "Featured"


@st.cache_data
def get_products():
    try:
        prods = load_json("products.json")
    except Exception:
        prods = [
            {"name": "Latte", "price": 17, "description": "Classic milk coffee", "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=600&q=60"},
            {"name": "Spanish Latte", "price": 22, "description": "Sweet condensed milk latte", "image": "https://images.unsplash.com/photo-1470337458703-46ad1756a187?auto=format&fit=crop&w=600&q=60"},
            {"name": "Cold Brew", "price": 19, "description": "Slow-steeped, smooth", "image": "https://images.unsplash.com/photo-1481391032119-d89fee407e44?auto=format&fit=crop&w=600&q=60"},
        ]
    for p in prods:
        p["category"] = categorize(p["name"])
        p.setdefault("description", "Crafted with premium ingredients, barista-approved.")
        p.setdefault("image", "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=400&q=60")
    return prods


apply_theme()
# Determine mode from query (?mode=menu for customer view, default pos for management)
qp = st.query_params
mode_val = qp.get("mode", "pos")
mode = mode_val[0] if isinstance(mode_val, list) else mode_val

# PIN for management unlock
PIN_CODE = "2025"

if mode == "pos":
    if not st.session_state.get("auth"):
        st.warning("Please login to access Qx Register.")
        st.switch_page("pages/1_Login.py")
    st.session_state.setdefault("pos_admin", False)
    # Floating unlock button
    unlock_col = st.empty()
    with unlock_col:
        if not st.session_state["pos_admin"]:
            if st.button("🔒 Admin", help="Tap to enter PIN and show admin sidebar"):
                st.session_state["pos_unlock"] = True
        else:
            st.markdown("🔓 Admin unlocked")
    if st.session_state.get("pos_unlock"):
        pin_try = st.text_input("Enter admin PIN", type="password", key="pos_admin_pin")
        if st.button("Unlock", key="pos_unlock_btn"):
            if pin_try == PIN_CODE:
                st.session_state["pos_admin"] = True
                st.session_state["pos_unlock"] = False
                st.success("Admin unlocked.")
            else:
                st.error("Incorrect PIN.")
    if st.session_state.get("pos_admin"):
        render_sidebar()
    else:
        # hide sidebar until unlocked
        st.markdown("<style>[data-testid='stSidebar']{display:none !important;}</style>", unsafe_allow_html=True)

else:
    # customer mode: hide sidebar, no admin gating
    st.markdown("<style>[data-testid='stSidebar']{display:none !important;}</style>", unsafe_allow_html=True)

products = get_products()
st.session_state.setdefault("pos_active_cat", products[0]["category"] if products else "Featured")
st.session_state.setdefault("pos_selected", products[0] if products else {})
st.session_state.setdefault("pos_cart", [])
st.session_state.setdefault("pos_pay_method", "Card")

# Layout: allow normal scrolling but give columns 80/20 feel
st.markdown(
    """
    <style>
    .pos-card { transition: transform 0.15s ease, box-shadow 0.2s ease; }
    .pos-card:hover { transform: translateY(-3px); box-shadow: 0 14px 30px rgba(0,0,0,0.25); }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([4, 1], gap="medium")

 # LEFT PANEL
with left:
    categories = [
        "Picks for you 🔥",
        "Banana Pudding Special",
        "Breakfast & All day Breakfa...",
        "Desserts",
        "Coffee",
        "Pasta",
        "French Toast",
        "Fresh Juice & Soft Drink",
        "Mojitos & Mocktails",
        "Appetizers",
        "Sliders And Burgers",
        "Main Course & Rice pots",
        "Soup",
        "Salad",
    ]
    if categories and st.session_state["pos_active_cat"] not in categories:
        st.session_state["pos_active_cat"] = categories[0]
    tabs = st.tabs(categories)
    for tab, cat in zip(tabs, categories):
        with tab:
            st.session_state["pos_active_cat"] = cat
            # For demo, show all products for all categories, or filter if you have mapping
            active_items = [p for p in products if p.get("category", "Featured") == cat] if products else []
            # If no products match, show all as fallback (optional)
            if not active_items:
                active_items = products
            cols = st.columns(4)
            for idx, item in enumerate(active_items):
                with cols[idx % 4]:
                    st.markdown(
                        f"""
                        <div class="glass pos-card animate-pop" style="padding:12px;">
                            <img src="{item['image']}" loading="lazy" style="width:100%; border-radius:12px; height:150px; object-fit:cover;"/>
                            <div style="margin-top:8px; font-weight:700; color:#E8EEF9;">{item['name']}</div>
                            <div style="color:#9fb0c7; font-size:12px;">{item['description']}</div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                                <span style="color:#E0B455; font-weight:700;">AED {item['price']:.2f}</span>
                                <span style="color:#9fb0c7; font-size:12px;">Tap to configure</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(f"Select {item['name']}", key=f"select_{cat}_{idx}", use_container_width=True):
                        st.session_state["pos_selected"] = item
with right:
    selected = st.session_state["pos_selected"]
    if selected:
        st.markdown(
            f"""
            <div class="glass glass-strong animate-pop" style="padding:12px;">
                <div style="display:flex; gap:10px;">
                    <img src="{selected['image']}" loading="lazy" style="width:80px; height:80px; border-radius:10px; object-fit:cover;"/>
                    <div>
                        <div style="font-weight:700;">{selected['name']}</div>
                        <div style="color:#E0B455; font-weight:700;">AED {selected['price']:.2f}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        size = st.radio("Size", ["S", "M", "L"], horizontal=True, key="pos_size")
        milk = st.radio("Milk", ["Whole", "Skim", "Oat"], horizontal=True, key="pos_milk")
        ice = st.radio("Ice", ["Normal", "Less", "None"], horizontal=True, key="pos_ice")
        sweet = st.radio("Sweetness", ["Normal", "Less", "None"], horizontal=True, key="pos_sweet")
        extra = st.checkbox("Extra shot", key="pos_extra")
        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, step=1, key="pos_qty")
        if st.button("Add to Cart", use_container_width=True):
            st.session_state["pos_cart"].append(
                {
                    "item": selected["name"],
                    "qty": qty,
                    "price": selected["price"],
                    "mods": {"size": size, "milk": milk, "ice": ice, "sweet": sweet, "extra": extra},
                }
            )

    st.markdown("### Cart")
    to_remove = []
    for i, line in enumerate(st.session_state["pos_cart"]):
        mods = line.get("mods", {})
        mod_text = ", ".join([f"{k}: {('Yes' if v is True else v)}" for k, v in mods.items()])
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.markdown(f"**{line['item']}**")
            st.markdown(f"<span style='color:#9fb0c7; font-size:12px;'>{mod_text}</span>", unsafe_allow_html=True)
        with c2:
            if st.button("+", key=f"inc_{i}"):
                st.session_state["pos_cart"][i]["qty"] += 1
            if st.button("-", key=f"dec_{i}"):
                st.session_state["pos_cart"][i]["qty"] = max(1, st.session_state["pos_cart"][i]["qty"] - 1)
        with c3:
            st.markdown(f"<div style='color:#E0B455; font-weight:700;'>AED {line['qty']*line['price']:.2f}</div>", unsafe_allow_html=True)
        if st.button("Remove", key=f"rm_{i}"):
            to_remove.append(i)
    for idx in reversed(to_remove):
        st.session_state["pos_cart"].pop(idx)

    subtotal = sum(line["qty"] * line["price"] for line in st.session_state["pos_cart"])
    vat = subtotal * 0.05
    service = subtotal * 0.05
    total = subtotal + vat + service
    st.markdown(
        f"""
        <div class="glass glass-strong animate-pop" style="padding:10px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between;"><span>Subtotal</span><span>AED {subtotal:.2f}</span></div>
            <div style="display:flex; justify-content:space-between;"><span>VAT 5%</span><span>AED {vat:.2f}</span></div>
            <div style="display:flex; justify-content:space-between;"><span>Service</span><span>AED {service:.2f}</span></div>
            <div style="display:flex; justify-content:space-between; font-weight:700; color:#E0B455; margin-top:6px;"><span>Total</span><span>AED {total:.2f}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Payment")
    option = st.radio("Choose method", ["Cash", "Card", "QR Payment (demo)", "Mark as Paid (demo)"], key="pos_pay_method")
    if st.button("Confirm Payment", use_container_width=True):
        st.session_state["pos_payment"] = True
        st.session_state["pos_receipt"] = {
            "id": str(uuid.uuid4())[:8].upper(),
            "items": list(st.session_state["pos_cart"]),
            "total": total,
            "method": option,
        }
        st.session_state["pos_cart"] = []
        st.success("Payment accepted — order completed.")
