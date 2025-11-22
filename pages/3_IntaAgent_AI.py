import time

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


def qx_card(title: str, body: str, severity: str | None = None) -> str:
    colors = {
        "critical": ("rgba(255,77,77,0.22)", "#ff8c8c"),
        "warning": ("rgba(224,180,85,0.18)", "#ffd78a"),
        "info": ("rgba(27,118,255,0.18)", "#9fc4ff"),
        None: ("rgba(255,255,255,0.05)", "#cbd7f0"),
    }
    bg, fg = colors.get(severity, colors[None])
    return (
        f"<div class='glass animate-pop' style='padding:12px; border:1px solid rgba(255,255,255,0.08); "
        f"background:{bg}; color:{fg};'>{body}</div>"
    )


st.session_state["active_page"] = "Qx Intelligence"
apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access Qx™ Intelligence.")
    st.switch_page("pages/1_Login.py")

ai = load_json("ai.json")

# Header
st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding:14px 16px; position:relative; overflow:hidden; border-left:4px solid #1B76FF;">
        <div style="position:absolute; inset:0; background: linear-gradient(135deg, rgba(27,118,255,0.08), rgba(12,18,26,0.65)); opacity:0.7;"></div>
        <div style="position:absolute; inset:0; background: linear-gradient(120deg, rgba(255,255,255,0.05), transparent); opacity:0.4;"></div>
        <div style="position:relative; display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:42px; height:42px; border-radius:50%; background: radial-gradient(circle, rgba(27,118,255,0.6), rgba(27,118,255,0.05)); border:1px solid rgba(224,180,85,0.65); box-shadow:0 0 14px rgba(27,118,255,0.5); display:flex; align-items:center; justify-content:center; animation: pulse 1.5s infinite;">
                    <img src="../assets/qx/qx_icon.svg" width="26" height="26" />
                </div>
                <div>
                    <div class="pill" style="background: rgba(27,118,255,0.16);">Powered by Qx Neural Engine v1.0 (demo)</div>
                    <h2 style="margin: 4px 0 2px;">Qx™ Intelligence — Operational Brain</h2>
                    <p style="color:#cbd7f0; margin:0;">AI-driven performance analysis, demand prediction, and risk detection.</p>
                </div>
            </div>
            <div style="color:#9fb0c7; font-size:12px;">Live Mode • Demo</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Smart Alerts
severity_map = []
for a in ai.get("alerts", []):
    lower = a.lower()
    if any(k in lower for k in ["low", "down", "below", "risk"]):
        severity_map.append(("critical", "⚠️", a))
    elif any(k in lower for k in ["increase", "spike", "up"]):
        severity_map.append(("warning", "⚡", a))
    elif any(k in lower for k in ["good", "strong", "healthy"]):
        severity_map.append(("info", "✅", a))
    else:
        severity_map.append((None, "ℹ️", a))

st.markdown(
    """
    <div class="glass glass-strong animate-pop" style="padding:12px; margin-top:8px;">
        <div class="pill" style="background: rgba(27,118,255,0.14);">Qx™ Smart Alerts</div>
    </div>
    """,
    unsafe_allow_html=True,
)
alert_cols = st.columns(3)
for idx, (sev, icon, text) in enumerate(severity_map):
    with alert_cols[idx % 3]:
        st.markdown(
            f"""
            <div class="glass animate-pop" style="padding:12px; border:1px solid rgba(255,255,255,0.08); background: {'rgba(255,77,77,0.22)' if sev=='critical' else 'rgba(224,180,85,0.18)' if sev=='warning' else 'rgba(27,118,255,0.16)'};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong>{icon} {text}</strong>
                    <span style="color:#9fb0c7; font-size:11px;">Analyzed 2 mins ago (demo)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Profit Drivers
drivers = ai.get("profit_drivers", [])[:3]
st.markdown(
    """
    <div class="glass glass-strong animate-pop" style="padding:12px; margin-top:8px;">
        <div class="pill" style="background: rgba(224,180,85,0.16); color:#ffd78a;">Profit Drivers Identified by Qx™</div>
    </div>
    """,
    unsafe_allow_html=True,
)
driver_cols = st.columns(3)
for col, d in zip(driver_cols, drivers):
    spark = px.line(y=[d["margin"] * 0.7, d["margin"] * 0.9, d["margin"]], height=100)
    spark.update_traces(line=dict(color="#E0B455", width=3), marker=dict(size=4, color="#1B76FF"))
    spark.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    col.markdown(
        f"""
        <div class="glass animate-pop" style="padding:12px; min-height:140px;">
            <strong>{d['item']}</strong><br/>
            <span style="color:#cbd7f0;">Margin: {d['margin']*100:.0f}%</span><br/>
            <span style="color:#9fb0c7; font-size:12px;">High margin — recommended for evening upsells.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col.plotly_chart(spark, use_container_width=True, config={"displayModeBar": False})

# Fast vs Slow movers
fast_movers = ai.get("fast_movers", [])
slow_movers = ai.get("slow_movers", [])
fm_col, sm_col = st.columns(2)
with fm_col:
    st.markdown(
        """
        <div class="glass glass-strong animate-pop" style="padding:12px;">
            <div class="pill" style="background: rgba(27,118,255,0.14);">Fast Movers</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for f in fast_movers:
        st.markdown(
            f"""
            <div class="glass animate-pop" style="padding:10px; border-left:4px solid #1B76FF;">
                <strong>{f['item']}</strong><br/>
                <span style="color:#cbd7f0;">{f.get('rate','3x faster than average')}</span>
                <div style="margin-top:6px; height:8px; border-radius:8px; background:rgba(255,255,255,0.07); overflow:hidden;">
                    <div style="width:90%; height:100%; background:#1B76FF;"></div>
                </div>
                <span style="color:#9fb0c7; font-size:12px;">Trend: ↑ accelerating</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
with sm_col:
    st.markdown(
        """
        <div class="glass glass-strong animate-pop" style="padding:12px;">
            <div class="pill" style="background: rgba(224,180,85,0.16); color:#ffd78a;">Slow Movers</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for s in slow_movers:
        st.markdown(
            f"""
            <div class="glass animate-pop" style="padding:10px; border-left:4px solid #E0B455;">
                <strong>{s['item']}</strong><br/>
                <span style="color:#cbd7f0;">{s['days_no_sale']} days without sale</span>
                <div style="margin-top:6px; height:8px; border-radius:8px; background:rgba(255,255,255,0.07); overflow:hidden;">
                    <div style="width:30%; height:100%; background:#E0B455;"></div>
                </div>
                <span style="color:#9fb0c7; font-size:12px;">Trend: ↓ needs promo</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.markdown("<div style='color:#9fb0c7; font-size:12px; margin-top:4px;'>Insights refreshed continuously by Qx™.</div>", unsafe_allow_html=True)

# Demand prediction engine
prediction = ai.get("prediction", {})
heatmap = prediction.get("heatmap", [])
pred_cols = st.columns([1, 1, 1.4])
with pred_cols[0]:
    st.markdown(
        f"""
        <div class="glass animate-pop" style="padding:12px; border:1px solid rgba(27,118,255,0.4);">
            <div class="pill" style="background: rgba(27,118,255,0.14);">Next Busy Hour</div>
            <h4 style="margin:6px 0;">{prediction.get('next_busy_hour','N/A')}</h4>
            <span style="color:#9fb0c7; font-size:12px;">⏱ Clock-synced</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with pred_cols[1]:
    st.markdown(
        f"""
        <div class="glass animate-pop" style="padding:12px; background: linear-gradient(135deg, rgba(27,118,255,0.22), rgba(224,180,85,0.18));">
            <div class="pill" style="background: rgba(224,180,85,0.14); color:#ffd78a;">Expected Orders</div>
            <h3 style="margin:6px 0;">{prediction.get('expected_orders','—')}</h3>
            <span style="color:#9fb0c7; font-size:12px;">Projected volume</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with pred_cols[2]:
    if heatmap:
        fig_heat = px.imshow(
            heatmap,
            color_continuous_scale=["#0b1a2f", "#1B76FF", "#E0B455"],
            labels={"color": "Demand Index"},
            title="Qx™ Heatmap",
        )
        fig_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(color="#E8EEF9"),
        )
        st.plotly_chart(fig_heat, use_container_width=True)
st.markdown("<p style='color:#9fb0c7; font-size:12px;'>Forecast produced using historical patterns + real-time signals (demo).</p>", unsafe_allow_html=True)

# Qx Operational Feed
feed = [
    "Evening surge expected — recommend prepping +12% milk stock.",
    "Spanish Latte continues to dominate profit share.",
    "Flat White sales declining — consider promotional adjustment.",
    "High volatility detected in morning rush (07:00–09:30).",
    "Staff alignment advised for 8 PM peak hour.",
]
idx = int(time.time() // 6) % len(feed)
st.markdown(
    f"""
    <div class="glass animate-pop" style="border-left:4px solid #1B76FF; box-shadow:0 0 16px rgba(27,118,255,0.25); margin-top:10px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="width:10px; height:10px; border-radius:50%; background:#1B76FF; box-shadow:0 0 12px rgba(27,118,255,0.6);"></span>
            <strong>Qx™ Operational Feed</strong>
        </div>
        <div style="color:#cbd7f0; margin-top:6px;">{feed[idx]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
