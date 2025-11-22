import pandas as pd
import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access Products Cost.")
    st.switch_page("pages/1_Login.py")

products = load_json("products.json")
df = pd.DataFrame(products)
df["margin_pct"] = ((df["price"] - df["cost"]) / df["price"]) * 100


def margin_style(val):
    if val > 40:
        return "background-color: rgba(78,204,163,0.15); color: #c3f3de;"
    if 20 <= val <= 40:
        return "background-color: rgba(224,180,85,0.18); color: #ffd78a;"
    return "background-color: rgba(255,77,77,0.15); color: #ff8c8c;"


styled = (
    df.rename(
        columns={
            "name": "Product",
            "cost": "Cost (AED)",
            "price": "Price (AED)",
            "margin_pct": "Margin %",
        }
    )
    .style.format({"Cost (AED)": "AED {:.2f}", "Price (AED)": "AED {:.2f}", "Margin %": "{:.1f}%"})
    .applymap(margin_style, subset=["Margin %"])
)

st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding: 18px;">
        <div class="pill">Profit Lens</div>
        <h2 style="margin: 6px 0;">Products Cost & Pricing</h2>
        <p style="color:#9fb0c7; margin:0;">See which items make real money — margins highlighted instantly.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.dataframe(styled, use_container_width=True, hide_index=True)
