import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


def get_products():
    data = load_json("products.json")
    # Add placeholder metadata
    for p in data:
        p.setdefault("description", "Signature Lark Café drink crafted with premium beans.")
        p.setdefault("badge", "Qx Recommended" if "Latte" in p["name"] else "Best Seller")
        p.setdefault("image", "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=600&q=60")
    return data


apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access QR Menu demo.")
    st.switch_page("pages/1_Login.py")

st.session_state.setdefault("qr_cart", [])
st.session_state.setdefault("qr_modal", None)
st.session_state.setdefault("qr_lang", "EN")

products = get_products()


# Light mode for QR menu only
st.markdown(
    """
    <style>
    body, .stApp { background: #f8f7f4 !important; color: #2b2b2b !important; }
    .light-card { background: #ffffff; border-radius: 18px; box-shadow: 0 12px 28px rgba(0,0,0,0.08); padding: 14px; }
    .chip { display:inline-flex; align-items:center; padding: 8px 14px; border-radius: 24px; border:1px solid #E0B455; margin-right: 8px; margin-bottom: 8px; cursor:pointer; transition: all 0.2s ease; }
    .chip-active { background: linear-gradient(120deg, #E0B455, #f7d88a); color:#2b2b2b; border:none; }
    .chip-inactive { background: #fff; color:#2b2b2b; }
    .product-card { transition: transform 0.15s ease, box-shadow 0.2s ease; }
    .product-card:hover { transform: translateY(-3px); box-shadow: 0 14px 30px rgba(0,0,0,0.12); }
    .badge { padding:4px 10px; border-radius:12px; background: rgba(224,180,85,0.16); color:#8a6b1f; font-size:12px; }
    .floating-cart { position: fixed; bottom: 24px; right: 24px; width: 58px; height: 58px; border-radius: 50%; background: linear-gradient(135deg, #E0B455, #f7d88a); box-shadow: 0 12px 24px rgba(224,180,85,0.35); display:flex; align-items:center; justify-content:center; cursor:pointer; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div style="text-align:center; padding: 10px 0 12px;">
        <img src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=180&q=60" style="width:120px; border-radius:20px; box-shadow:0 8px 20px rgba(0,0,0,0.15);" />
        <h2 style="margin:10px 0 2px; font-family:'Inter', 'Playfair Display', serif; color:#2b2b2b;">Lark Café</h2>
        <div style="color:#777; margin-bottom:4px;">Scan • Browse • Enjoy</div>
        <div style="color:#777; font-size:12px;">Powered by Qx™ Menu Engine</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Language toggle
lang_col1, lang_col2 = st.columns([6, 1])
with lang_col2:
    st.radio("Language", ["EN", "AR"], horizontal=True, label_visibility="collapsed", key="qr_lang")
lang = st.session_state.get("qr_lang", "EN")

# Categories
def categorize(name: str) -> str:
    if "Cold" in name:
        return "Cold Drinks"
    if "Latte" in name:
        return "Coffee"
    return "Featured"


for p in products:
    p["category"] = categorize(p["name"])

categories = list(dict.fromkeys([p["category"] for p in products]))
active_cat = st.session_state.get("qr_active_cat", categories[0])

chip_bar = ""
for cat in categories:
    active_class = "chip chip-active" if cat == active_cat else "chip chip-inactive"
    chip_bar += f"<span class='{active_class}' onclick=\"window.location.href='#{cat.replace(' ','_')}'\">{cat}</span>"
st.markdown(chip_bar, unsafe_allow_html=True)

# Recommended section
st.markdown("### Recommended Today")
rec_items = products[:3]
rec_cols = st.columns(3)
for col, item in zip(rec_cols, rec_items):
    col.markdown(
        f"""
        <div class="light-card product-card">
            <img src="{item['image']}" style="width:100%; border-radius:14px; height:160px; object-fit:cover;"/>
            <div style="margin-top:8px; font-weight:700;">{item['name']}</div>
            <div style="color:#777; font-size:12px;">{item['description']}</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                <span style="color:#8a6b1f; font-weight:700;">AED {item['price']:.2f}</span>
                <span class="badge">{item['badge']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Menu")

for cat in categories:
    st.markdown(f"<h4 id='{cat.replace(' ','_')}' style='margin-top:12px;'>{cat}</h4>", unsafe_allow_html=True)
    cat_items = [p for p in products if p["category"] == cat]
    if not cat_items:
        st.markdown(
            """
            <div style="text-align:center; color:#777; padding:20px;">
                ☕ No items found. Please choose another category.
            </div>
            """,
            unsafe_allow_html=True,
        )
        continue
    cols = st.columns(3)
    for idx, item in enumerate(cat_items):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="light-card product-card">
                    <img src="{item['image']}" style="width:100%; border-radius:14px; height:150px; object-fit:cover;"/>
                    <div style="margin-top:8px; font-weight:700;">{item['name']}</div>
                    <div style="color:#777; font-size:12px;">{item['description']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                        <span style="color:#8a6b1f; font-weight:700;">AED {item['price']:.2f}</span>
                        <span class="badge">{item['badge']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"View {item['name']}", key=f"view_{cat}_{idx}", use_container_width=True):
                st.session_state["qr_modal"] = item

# Modal
if st.session_state["qr_modal"]:
    item = st.session_state["qr_modal"]
    with st.container():
        st.markdown(
            f"""
            <div class="light-card" style="padding:16px; margin-top:10px;">
                <img src="{item['image']}" style="width:100%; border-radius:16px; height:240px; object-fit:cover;"/>
                <h4 style="margin:8px 0 4px;">{item['name']}</h4>
                <p style="color:#555;">{item['description']}</p>
                <div style="color:#8a6b1f; font-weight:700;">AED {item['price']:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        size = st.radio("Size", ["Small", "Medium", "Large"], horizontal=True, key="qr_size")
        sugar = st.radio("Sugar level", ["Normal", "Less", "None"], horizontal=True, key="qr_sugar")
        milk = st.radio("Milk type", ["Whole", "Skim", "Oat"], horizontal=True, key="qr_milk")
        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, step=1, key="qr_qty_modal")
        add_col, cancel_col = st.columns(2)
        with add_col:
            if st.button("Add to cart", use_container_width=True, key="qr_add_modal"):
                st.session_state["qr_cart"].append(
                    {
                        "item": item["name"],
                        "qty": qty,
                        "price": item["price"],
                        "options": {"size": size, "sugar": sugar, "milk": milk},
                    }
                )
                st.session_state["qr_modal"] = None
                st.success("Added to cart.")
        with cancel_col:
            if st.button("Cancel", use_container_width=True, key="qr_cancel_modal"):
                st.session_state["qr_modal"] = None

# Floating cart
cart_count = sum(line["qty"] for line in st.session_state["qr_cart"])
st.markdown(
    f"""
    <div class="floating-cart" onclick="window.location.href='#cart'">
        🛍
        <div style="position:absolute; top:6px; right:6px; background:#2b2b2b; color:#fff; width:18px; height:18px; border-radius:50%; font-size:12px; display:flex; align-items:center; justify-content:center;">{cart_count}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Cart drawer (simple anchor section)
st.markdown("<h3 id='cart'>Cart Summary</h3>", unsafe_allow_html=True)
total = sum(line["qty"] * line["price"] for line in st.session_state["qr_cart"])
for line in st.session_state["qr_cart"]:
    st.markdown(f"- {line['qty']} × {line['item']} — AED {line['qty']*line['price']:.2f}")
st.markdown(f"**Total: AED {total:.2f}**")
cart_cols = st.columns([1, 1])
with cart_cols[0]:
    if st.button("Order Now", use_container_width=True):
        st.success("Order placed (DEMO MODE)")
        st.session_state["qr_cart"] = []
with cart_cols[1]:
    if st.button("Clear Cart", use_container_width=True):
        st.session_state["qr_cart"] = []
