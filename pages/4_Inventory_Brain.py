import re
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


def status_info(row):
    ratio = row["stock"] / row["min"] if row["min"] else 1
    if ratio < 1:
        return "Critical", "rgba(255,77,77,0.35)", "#ff8c8c"
    if ratio == 1:
        return "Low", "rgba(224,180,85,0.35)", "#ffd78a"
    return "OK", "rgba(78,204,163,0.35)", "#c3f3de"


def build_supplier_pdf(rows):
    lines = ["Supplier Reorder List", f"Date: {datetime.now().strftime('%d %b %Y')}", ""]
    for row in rows:
        lines.append(f"{row['item']} — Order {row['amount']} — {row['reason']}")
    return "\n".join(lines).encode("utf-8")


apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access Inventory Brain.")
    st.switch_page("pages/1_Login.py")

inv = load_json("inventory.json")
ai = load_json("ai.json")
items_df = pd.DataFrame(inv["items"])

# Header
st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding:14px 16px; position:relative; overflow:hidden; border-left:4px solid #1B76FF;">
        <div style="position:absolute; inset:0; background: linear-gradient(135deg, rgba(27,118,255,0.08), rgba(12,18,26,0.65)); opacity:0.7;"></div>
        <div style="position:absolute; inset:0; background: linear-gradient(120deg, rgba(255,255,255,0.05), transparent); opacity:0.4;"></div>
        <div style="position:relative;">
            <div class="pill" style="background: rgba(27,118,255,0.16);">Inventory Brain — AI Loss Prevention</div>
            <h2 style="margin:6px 0 2px;">Inventory Brain — AI Loss Prevention</h2>
            <p style="color:#cbd7f0; margin:0;">Smart stock monitoring and predictive insights powered by IntaAgent™</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Inventory cards grid
st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
num_cols = 3
cols = st.columns(num_cols)
for idx, row in items_df.iterrows():
    status, bg, fg = status_info(row)
    pct = int((row["stock"] / row["min"]) * 100) if row["min"] else 100
    pct = max(0, min(pct, 150))
    bar_color = "#1B76FF" if status == "OK" else ("#E0B455" if status == "Low" else "#FF6B6B")
    ai_note = None
    if status != "OK":
        ai_note = ai["alerts"][1] if "milk" in row["name"].lower() else "Demand trending up — reorder suggested."
    with cols[idx % num_cols]:
        st.markdown(
            f"""
            <div class="glass animate-pop" style="padding:12px; border-left:4px solid {bar_color}; min-height:150px; transition: transform 0.2s ease, box-shadow 0.2s ease;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong>{row['name']}</strong>
                    <span style="padding:4px 8px; border-radius:10px; background:{bg}; color:{fg}; font-weight:700;">{status}</span>
                </div>
                <div style="color:#9fb0c7; margin-top:6px;">Stock: {row['stock']} | Min: {row['min']}</div>
                <div style="margin-top:8px; height:8px; border-radius:8px; background:rgba(255,255,255,0.07); overflow:hidden;">
                    <div style="width:{pct}%; height:100%; background:{bar_color};"></div>
                </div>
                <div style="color:#cbd7f0; margin-top:6px; font-size:12px;">Remaining: {pct}%</div>
                {"<div style='color:#ff8c8c; margin-top:6px; font-size:12px;'>"+ai_note+"</div>" if ai_note else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )

# AI Risk Zone
critical = items_df[items_df.apply(lambda r: status_info(r)[0] == "Critical", axis=1)]
low = items_df[items_df.apply(lambda r: status_info(r)[0] == "Low", axis=1)]
if not critical.empty or not low.empty:
    st.markdown(
        """
        <div class="glass glass-strong animate-pop" style="padding:12px; border-left:4px solid #FF6B6B;">
            <div class="pill" style="background: rgba(255,77,77,0.18); color:#ffb3b3;">AI Detected Risks</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    risk_cols = st.columns(2)
    def risk_card(r, tone):
        reason = "will run out within 4.3 hours based on demand rate" if tone == "critical" else "trending upward in usage due to morning rush"
        risk_color = "rgba(255,77,77,0.22)" if tone == "critical" else "rgba(224,180,85,0.22)"
        risk_border = "#FF6B6B" if tone == "critical" else "#E0B455"
        return f"""
            <div class="glass animate-pop" style="padding:10px; border:1px solid {risk_border}; background:{risk_color};">
                <strong>{r['name']}</strong><br/>
                <span style="color:#cbd7f0;">Stock: {r['stock']} | Min: {r['min']}</span><br/>
                <span style="color:{risk_border}; font-size:12px;">{reason}.</span>
            </div>
        """
    for df, tone in [(critical, "critical"), (low, "low")]:
        for idx, row in df.iterrows():
            with risk_cols[idx % 2]:
                st.markdown(risk_card(row, tone), unsafe_allow_html=True)

# Waste & loss analysis
waste_df = pd.DataFrame(inv.get("waste_chart", []))
loss_breakdown = pd.DataFrame(
    [{"label": "Milk", "value": 67}, {"label": "Beans", "value": 22}, {"label": "Other", "value": 11}]
)
chart_cols = st.columns(2)
with chart_cols[0]:
    if not waste_df.empty:
        waste_fig = px.line(
            waste_df,
            x="day",
            y="value",
            title="Waste Trend (units)",
            markers=True,
            template="plotly_dark",
        )
        waste_fig.update_traces(line=dict(color="#1B76FF", width=3), marker=dict(size=8, color="#E0B455"))
        waste_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E8EEF9"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(waste_fig, use_container_width=True)
    st.markdown("<p style='color:#9fb0c7;'>AI Interpretation: Tuesday waste spike due to over-prep of Spanish Latte.</p>", unsafe_allow_html=True)

with chart_cols[1]:
    loss_fig = px.bar(
        loss_breakdown,
        x="label",
        y="value",
        title="Loss Breakdown",
        color="value",
        color_continuous_scale=["#5FB1FF", "#1B76FF"],
        template="plotly_dark",
    )
    loss_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8EEF9"),
        margin=dict(l=20, r=20, t=40, b=20),
        coloraxis_showscale=False,
    )
    st.plotly_chart(loss_fig, use_container_width=True)
    st.markdown("<p style='color:#9fb0c7;'>AI Interpretation: Milk is responsible for 67% of weekly waste.</p>", unsafe_allow_html=True)

# Smart reorder engine
raw_suggestions = inv.get("reorder_suggestions", [])
structured = []
for text in raw_suggestions:
    amount = re.findall(r"Order\\s+(\\d+)", text)
    item_name = re.sub(r"Order\\s+\\d+\\s+of\\s+", "", text, flags=re.IGNORECASE)
    structured.append(
        {
            "item": item_name.strip(),
            "amount": amount[0] if amount else "Check",
            "reason": "Projected to run out by 6 PM due to evening peak.",
        }
    )

st.markdown(
    """
    <div class="glass glass-strong animate-pop" style="padding:14px; border-left:3px solid #E0B455;">
        <div class="pill" style="background: rgba(224,180,85,0.14); color:#ffd78a;">Smart Reorder Suggestions</div>
    </div>
    """,
    unsafe_allow_html=True,
)
for s in structured:
    st.markdown(
        f"""
        <div class="glass animate-pop" style="padding:10px;">
            <strong>{s['item']}</strong> — Order {s['amount']}<br/>
            <span style="color:#9fb0c7;">{s['reason']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

pdf_bytes = build_supplier_pdf(structured)
st.download_button(
    "Generate Supplier PDF",
    data=pdf_bytes,
    file_name="supplier_reorder_list.txt",
    mime="text/plain",
    use_container_width=True,
)

# Daily usage & prediction
forecast = [
    {"item": "Coffee Beans", "amount": "3.1 kg", "trend": "up"},
    {"item": "Milk 2L", "amount": "7 units", "trend": "up"},
    {"item": "Cups", "amount": "420 units", "trend": "stable"},
]
trend_icon = {"up": "⬆", "down": "⬇", "stable": "⟲"}
st.markdown(
    """
    <div class="glass glass-strong animate-pop" style="padding:14px; margin-top:10px;">
        <div class="pill" style="background: rgba(27,118,255,0.14);">Tomorrow's Forecast</div>
    </div>
    """,
    unsafe_allow_html=True,
)
fore_cols = st.columns(3)
for col, entry in zip(fore_cols, forecast):
    col.markdown(
        f"""
        <div class="glass animate-pop" style="padding:10px;">
            <strong>{entry['item']}</strong><br/>
            <span style="color:#cbd7f0;">{entry['amount']}</span><br/>
            <span style="color:#9fb0c7;">{trend_icon[entry['trend']]} {entry['trend'].title()}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Inventory timeline
timeline = [
    {"item": "Coffee Beans", "hours": 4},
    {"item": "Milk", "hours": 9},
    {"item": "Cups", "hours": 72},
]
st.markdown(
    """
    <div class="glass glass-strong animate-pop" style="padding:14px; margin-top:10px;">
        <div class="pill" style="background: rgba(224,180,85,0.14); color:#ffd78a;">Hours until depletion</div>
    </div>
    """,
    unsafe_allow_html=True,
)
for t in timeline:
    bar_width = min(t["hours"], 80)
    color = "#FF6B6B" if t["hours"] < 6 else "#E0B455" if t["hours"] < 24 else "#1B76FF"
    st.markdown(
        f"""
        <div class="glass animate-pop" style="padding:10px; margin-bottom:8px;">
            <strong>{t['item']}</strong> — {t['hours']}h
            <div style="margin-top:6px; height:8px; border-radius:8px; background:rgba(255,255,255,0.07); overflow:hidden;">
                <div style="width:{bar_width}%; height:100%; background:{color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# AI commentary bar
st.markdown(
    """
    <div class="glass animate-pop" style="border-left:4px solid #1B76FF; box-shadow:0 0 16px rgba(27,118,255,0.25); margin-top:12px;">
        <strong>IntaAgent™: Coffee Beans will require restocking by early afternoon. Consider adjusting prep and monitoring morning rush.</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
