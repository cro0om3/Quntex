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


apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access Qx™ Register.")
    st.switch_page("pages/1_Login.py")

products = load_json("products.json")
for p in products:
    p["category"] = categorize(p["name"])
    p.setdefault("description", "Crafted with premium ingredients, barista-approved.")
    p.setdefault("image", "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=400&q=60")

st.session_state.setdefault("pos_cart", [])
st.session_state.setdefault("pos_modal", None)
st.session_state.setdefault("pos_payment", False)
st.session_state.setdefault("pos_receipt", None)

# Header with Qx hints
st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding:14px 16px; position:relative; overflow:hidden; border-left:4px solid #1B76FF;">
        <div style="position:absolute; inset:0; background: linear-gradient(135deg, rgba(27,118,255,0.08), rgba(12,18,26,0.65)); opacity:0.7;"></div>
        <div style="position:absolute; inset:0; background: linear-gradient(120deg, rgba(255,255,255,0.05), transparent); opacity:0.4;"></div>
        <div style="position:relative; display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div class="pill" style="background: rgba(27,118,255,0.16);">Qx™ Register</div>
                <h2 style="margin: 4px 0 2px;">Fast, smart, and effortless order-taking</h2>
                <p style="color:#cbd7f0; margin:0;">Realtime Mode • AED • Demo</p>
            </div>
            <div style="color:#9fb0c7; font-size:12px; max-width:260px;">
                <div class="glass" style="padding:8px; border-left:3px solid #1B76FF;">
                    Qx™: Peak hour predicted in 12 minutes. Spanish Latte driving 32% of profit. Upsells lift avg ticket by 18%.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Category chips bar
categories = list(dict.fromkeys([p["category"] for p in products]))
active_cat = st.session_state.get("pos_active_cat", categories[0])

st.markdown(
    """
    <style>
    .pos-chip { display:inline-flex; align-items:center; padding: 8px 14px; border-radius: 24px; border:1px solid #E0B455; margin-right: 8px; margin-bottom: 8px; cursor:pointer; transition: all 0.2s ease; }
    .pos-chip-active { background: linear-gradient(120deg, #E0B455, #f7d88a); color:#0B1324; border:none; }
    .pos-chip-inactive { background: rgba(255,255,255,0.04); color:#E8EEF9; }
    .pos-card { transition: transform 0.15s ease, box-shadow 0.2s ease; min-width:180px; }
    .pos-card:hover { transform: translateY(-3px); box-shadow: 0 14px 30px rgba(0,0,0,0.25); }
    </style>
    """,
    unsafe_allow_html=True,
)

chips = ""
icons = {"Coffee": "☕", "Cold Drinks": "❄", "Featured": "⭐"}
for cat in categories:
    active_class = "pos-chip pos-chip-active" if cat == active_cat else "pos-chip pos-chip-inactive"
    icon = icons.get(cat, "🍽")
    chips += f"<span class='{active_class}' onclick=\"window.location.href='#{cat.replace(' ','_')}'\">{icon} {cat}</span>"
st.markdown(chips, unsafe_allow_html=True)

# Product grid and cart layout
left_col, right_col = st.columns([1.7, 1], gap="medium")

with left_col:
    st.markdown("### Menu")
    for cat in categories:
        st.markdown(f"<h5 id='{cat.replace(' ','_')}' style='margin-top:10px;'>{cat}</h5>", unsafe_allow_html=True)
        cat_items = [p for p in products if p["category"] == cat]
        if not cat_items:
            st.markdown("<div style='padding:12px; color:#9fb0c7;'>No items found. Choose another category.</div>", unsafe_allow_html=True)
            continue
        cols = st.columns(3)
        for idx, item in enumerate(cat_items):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="glass pos-card animate-pop" style="padding:12px;">
                        <img src="{item['image']}" style="width:100%; border-radius:12px; height:140px; object-fit:cover;"/>
                        <div style="margin-top:8px; font-weight:700; color:#E8EEF9;">{item['name']}</div>
                        <div style="color:#9fb0c7; font-size:12px;">{item['description']}</div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                            <span style="color:#E0B455; font-weight:700;">AED {item['price']:.2f}</span>
                            <span style="color:#9fb0c7; font-size:12px;">Touch to customize</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Select {item['name']}", key=f"pos_select_{cat}_{idx}", use_container_width=True):
                    st.session_state["pos_modal"] = item

if st.session_state["pos_modal"]:
    item = st.session_state["pos_modal"]
    with st.container():
        st.markdown(
            f"""
            <div class="glass glass-strong glow-border animate-pop" style="padding:16px; margin-top:10px;">
                <img src="{item['image']}" style="width:100%; border-radius:12px; height:200px; object-fit:cover;"/>
                <h4 style="margin:8px 0 4px;">{item['name']}</h4>
                <p style="color:#9fb0c7; margin:0;">AED {item['price']:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        size = st.radio("Size", ["S", "M", "L"], horizontal=True, key="pos_size")
        milk = st.radio("Milk", ["Whole", "Skim", "Oat"], horizontal=True, key="pos_milk")
        ice = st.radio("Ice level", ["Normal", "Less", "None"], horizontal=True, key="pos_ice")
        sweet = st.radio("Sweetness", ["Normal", "Less", "None"], horizontal=True, key="pos_sweet")
        extra = st.checkbox("Extra shot", key="pos_extra")
        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, step=1, key="pos_qty")
        add_col, cancel_col = st.columns(2)
        with add_col:
            if st.button("Add to Cart", use_container_width=True, key="pos_add_modal"):
                st.session_state["pos_cart"].append(
                    {
                        "item": item["name"],
                        "qty": qty,
                        "price": item["price"],
                        "mods": {"size": size, "milk": milk, "ice": ice, "sweet": sweet, "extra": extra},
                    }
                )
                st.session_state["pos_modal"] = None
        with cancel_col:
            if st.button("Cancel", use_container_width=True, key="pos_cancel_modal"):
                st.session_state["pos_modal"] = None

# Cart drawer / payment
with right_col:
    st.markdown("### Current Order")
    for i, line in enumerate(st.session_state["pos_cart"]):
        mods = line.get("mods", {})
        mod_text = ", ".join([f"{k}: {('Yes' if v is True else v)}" for k, v in mods.items()])
        st.markdown(
            f"""
            <div class="glass animate-pop" style="padding:10px; margin-bottom:8px; border-left:3px solid #E0B455;">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <strong>{line['item']}</strong><br/>
                        <span style="color:#9fb0c7; font-size:12px;">{mod_text}</span>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:#E0B455; font-weight:700;">AED {line['qty']*line['price']:.2f}</div>
                        <div style="color:#9fb0c7; font-size:12px;">Qty {line['qty']}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    subtotal = sum(line["qty"] * line["price"] for line in st.session_state["pos_cart"])
    vat = subtotal * 0.05
    service = subtotal * 0.05
    total = subtotal + vat + service
    st.markdown(
        f"""
        <div class="glass glass-strong animate-pop" style="padding:10px; position:sticky; bottom:10px;">
            <div style="display:flex; justify-content:space-between;"><span>Subtotal</span><span>AED {subtotal:.2f}</span></div>
            <div style="display:flex; justify-content:space-between;"><span>VAT 5%</span><span>AED {vat:.2f}</span></div>
            <div style="display:flex; justify-content:space-between;"><span>Service</span><span>AED {service:.2f}</span></div>
            <div style="display:flex; justify-content:space-between; font-weight:700; color:#E0B455; margin-top:6px;"><span>Total</span><span>AED {total:.2f}</span></div>
            <div style="display:flex; justify-content:space-between; margin-top:8px;">
                <a href="#" style="color:#ff8c8c; font-size:12px;" onClick="window.location.reload()">Clear Cart</a>
                <button style="width:60%; border:none; border-radius:12px; padding:10px; background: linear-gradient(120deg, #E0B455, #ffd78a); color:#0B1324; font-weight:700; cursor:pointer;" onClick="window.location.href='#pay'">Proceed to Payment</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<h4 id='pay'>Payment</h4>", unsafe_allow_html=True)

# Payment panel
pay_cols = st.columns(2)
with pay_cols[0]:
    st.markdown("<div class='glass animate-pop' style='padding:10px;'><div class='pill'>Payment Options</div></div>", unsafe_allow_html=True)
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

with pay_cols[1]:
    st.markdown("<div class='glass animate-pop' style='padding:10px;'><div class='pill'>Receipt Preview</div></div>", unsafe_allow_html=True)
    if st.session_state.get("pos_receipt"):
        receipt = st.session_state["pos_receipt"]
        st.markdown(f"Receipt ID: `{receipt['id']}`")
        for line in receipt["items"]:
            st.markdown(f"- {line['qty']} × {line['item']} — AED {line['qty']*line['price']:.2f}")
        st.markdown(f"**Total: AED {receipt['total']:.2f}**")
        st.markdown(f"Method: {receipt['method']}")
        if st.button("New Order", use_container_width=True):
            st.session_state["pos_receipt"] = None
            st.session_state["pos_payment"] = False

# Quick add bar
quick_items = ["Spanish Latte", "Water", "Extra Shot", "Croissant"]
st.markdown(
    """
    <div class="glass animate-pop" style="padding:10px; margin-top:12px; border-left:3px solid #1B76FF;">
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
    """,
    unsafe_allow_html=True,
)
qa_cols = st.columns(len(quick_items))
for col, qi in zip(qa_cols, quick_items):
    with col:
        if st.button(qi, use_container_width=True, key=f"quick_{qi}"):
            # default price lookup
            found = next((p for p in products if p["name"] == qi), None)
            price = found["price"] if found else 5.0
            st.session_state["pos_cart"].append({"item": qi, "qty": 1, "price": price, "mods": {}})
st.markdown("</div></div>", unsafe_allow_html=True)
