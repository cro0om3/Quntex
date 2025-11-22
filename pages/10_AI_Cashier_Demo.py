import random
import time
from typing import Dict

import pandas as pd
import streamlit as st

from utils.sidebar import render_sidebar
from utils.theme import apply_theme


def fake_cashier_data() -> Dict[str, Dict[str, float]]:
    moods = ["😊", "🙂", "🔥", "😐"]
    data = {}
    for i in range(1, 4):
        customers = random.randint(8, 30)
        revenue = random.randint(280, 900)
        upsell = random.randint(8, 45)
        speed = round(random.uniform(25, 60), 1)
        mood = random.choice(moods)
        data[f"Cashier {i}"] = {
            "customers": customers,
            "revenue": revenue,
            "upsell": upsell,
            "speed": speed,
            "mood": mood,
        }
    return data


apply_theme()
render_sidebar()

st.title("AI Cashier Analytics (Demo)")
st.caption("Live Monitoring + Estimated Earnings")

# Generate simulated data
cashier_data = fake_cashier_data()

left, right = st.columns([0.65, 0.35], gap="large")

with left:
    st.markdown(
        """
        <div style="position:relative; background: linear-gradient(135deg, rgba(27,118,255,0.08), rgba(12,18,26,0.65)); border:1px solid rgba(255,255,255,0.08); border-radius:18px; height:420px; overflow:hidden;">
            <div style="position:absolute; top:10px; left:10px; padding:6px 10px; background: rgba(224,180,85,0.16); border-radius:12px; color:#ffd78a; font-weight:700;">AI Processing…</div>
            <div style="position:absolute; bottom:16px; left:16px; color:#ffd78a; font-size:14px; line-height:1.4;">
                <div>Cashier Detected</div>
                <div>Customers: {cust}</div>
                <div>Revenue: AED {rev}</div>
                <div>Mood: {mood}</div>
            </div>
        </div>
        """.format(
            cust=sum(d["customers"] for d in cashier_data.values()),
            rev=sum(d["revenue"] for d in cashier_data.values()),
            mood=random.choice(["😊", "🙂", "🔥"]),
        ),
        unsafe_allow_html=True,
    )

    # Event Feed
    events = [
        "Person detected",
        "Queue spike detected",
        "Customer frustration detected",
        "Idle cashier detected",
    ]
    st.markdown(
        "<div class='glass glass-strong animate-pop' style='padding:12px; margin-top:10px;'><strong>Event Feed</strong></div>",
        unsafe_allow_html=True,
    )
    for e in events:
        st.markdown(
            f"<div class='glass animate-pop' style='padding:8px; margin-bottom:6px;'>{e}</div>",
            unsafe_allow_html=True,
        )

    # Heatmap placeholder
    st.markdown(
        """
        <div class="glass glass-strong animate-pop" style="padding:12px; margin-top:10px; height:180px; display:flex; align-items:center; justify-content:center; border:1px dashed rgba(255,255,255,0.2); border-radius:14px;">
            Heatmap — AI Simulation
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown("#### AI Performance Dashboard")
    # Ranking by revenue
    sorted_rev = sorted(cashier_data.items(), key=lambda x: x[1]["revenue"], reverse=True)
    ranks = ["🥇", "🥈", "🥉"]
    for rank, (name, stats) in zip(ranks, sorted_rev):
        st.markdown(
            f"""
            <div class="glass glass-strong animate-pop" style="padding:12px; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><strong>{rank} {name}</strong></div>
                    <div style="color:#E0B455; font-weight:700;">AED {stats['revenue']}</div>
                </div>
                <div style="color:#9fb0c7; font-size:12px;">Customers: {stats['customers']} • Upsell: {stats['upsell']}% • Speed: {stats['speed']}s • Mood: {stats['mood']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    total_rev = sum(v["revenue"] for v in cashier_data.values())
    total_cust = sum(v["customers"] for v in cashier_data.values())
    avg_upsell = round(sum(v["upsell"] for v in cashier_data.values()) / len(cashier_data), 1)
    avg_speed = round(sum(v["speed"] for v in cashier_data.values()) / len(cashier_data), 1)
    st.metric("Estimated Revenue (AED)", f"{total_rev:,.0f}")
    st.metric("Customers Served", f"{total_cust}")
    st.metric("Avg Upsell %", f"{avg_upsell}%")
    st.metric("Avg Service Time (s)", f"{avg_speed}")

    # Section A — Revenue Quality
    st.markdown("##### Revenue Quality")
    rq_arc = round(total_rev / total_cust, 2) if total_cust else 0
    rq_basket = round(random.uniform(25, 75), 2)
    rq_void = random.randint(0, 4)
    rq_disc = random.randint(0, 6)
    rq_leak = random.randint(50, 180)
    rq_trend = [random.randint(200, 500) for _ in range(7)]
    st.markdown(
        f"""
        <div class="glass glass-strong animate-pop" style="padding:12px; margin-bottom:8px;">
            <div>ARC: AED {rq_arc}</div>
            <div>Avg basket: AED {rq_basket}</div>
            <div>Voided orders: {rq_void}</div>
            <div>Discounted orders: {rq_disc}</div>
            <div>Est. revenue leakage: AED {rq_leak}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.line_chart(pd.DataFrame({"Revenue": rq_trend}))

    # Section B — Cashier Behavior AI
    st.markdown("##### Cashier Behavior AI")
    for name in cashier_data.keys():
        friendly = random.randint(70, 98)
        speed = random.randint(70, 98)
        accuracy = random.randint(68, 96)
        attention = random.randint(70, 99)
        summary = "Cashier 2 tends to rush orders between 7–8 PM, accuracy drops by 12%."
        st.markdown(
            f"""
            <div class="glass animate-pop" style="padding:10px; margin-bottom:6px;">
                <strong>{name}</strong><br/>
                Friendliness: {friendly}% • Speed: {speed}% • Accuracy: {accuracy}% • Attention: {attention}%<br/>
                <span style="color:#9fb0c7; font-size:12px;">{summary}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Section C — Queue Intelligence
    st.markdown("##### Queue Intelligence")
    avg_queue = random.uniform(2, 9)
    longest_wait = random.uniform(4, 12)
    fast_hour = "10 AM"
    slow_hour = "4 PM"
    peak_pred = "Peak expected 6:30 PM — deploy extra cashier."
    st.markdown(
        f"""
        <div class="glass glass-strong animate-pop" style="padding:10px; margin-bottom:8px;">
            <div>Avg queue length: {avg_queue:.1f}</div>
            <div>Longest wait today: {longest_wait:.1f} min</div>
            <div>Fastest hour: {fast_hour}</div>
            <div>Slowest hour: {slow_hour}</div>
            <div style="color:#9fb0c7; font-size:12px;">{peak_pred}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
