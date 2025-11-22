from datetime import datetime
from typing import List, Mapping

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.loader import load_json
from utils.sidebar import render_sidebar
from utils.theme import apply_theme


apply_theme()
render_sidebar()

if not st.session_state.get("auth"):
    st.warning("Please login to access Executive Reports.")
    st.switch_page("pages/1_Login.py")

reports = load_json("reports.json")

# Simple AI insight dictionary fallback
ai_insights = {
    "Revenue": "↑ Strong — 12% above weekly average",
    "Gross Profit": "Stable margin",
    "Net Profit": "Healthy net margin at 34%",
}


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf(section: str, rows: List[Mapping]) -> bytes:
    """Create a minimal PDF byte stream with black header and gold accent."""
    header_height = 60
    y = 760
    content_lines = [
        "q",
        "0 0 0 rg",
        f"0 {792 - header_height} 612 {header_height} re f",
        "0.878 0.705 0.333 rg",
        f"0 {792 - header_height} 612 3 re f",
        "Q",
        "BT",
        "1 1 1 rg",
        "/F1 20 Tf",
        f"50 {y} Td",
        f"({pdf_escape('Lark Executive Report')}) Tj",
        "/F1 12 Tf",
        "0 -22 Td",
        f"({pdf_escape('Section: ' + section)}) Tj",
    ]
    y -= 48
    content_lines.extend(["0 0 0 rg"])
    for row in rows:
        parts = []
        for k, v in row.items():
            if isinstance(v, (int, float)):
                parts.append(f"{k}: AED {v:,.2f}")
            else:
                parts.append(f"{k}: {v}")
        line_text = " • " + " — ".join(parts)
        content_lines.extend(["0 -18 Td", f"({pdf_escape(line_text)}) Tj"])
    content_lines.append("ET")
    content = "\n".join(content_lines) + "\n"
    content_bytes = content.encode("latin-1", errors="ignore")

    objects = []
    objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append("2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n")
    objects.append(
        "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
    )
    objects.append("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    objects.append(f"5 0 obj\n<< /Length {len(content_bytes)} >>\nstream\n{content}\nendstream\nendobj\n")

    pdf_header = "%PDF-1.4\n"
    offsets = []
    cursor = len(pdf_header)
    body_parts = [pdf_header]
    for obj in objects:
        offsets.append(cursor)
        body_parts.append(obj)
        cursor += len(obj)

    xref_start = cursor
    xref = f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n"
    trailer = f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF"
    body_parts.append(xref)
    body_parts.append(trailer)
    return "".join(body_parts).encode("latin-1", errors="ignore")


# Header block
st.markdown(
    """
    <div class="glass gold-frame animate-pop" style="padding: 14px 18px; position:relative; overflow:hidden; background: linear-gradient(135deg, rgba(25,44,65,0.6), rgba(12,18,26,0.8));">
        <div style="position:absolute; inset:0; background: linear-gradient(120deg, rgba(255,255,255,0.06), transparent); opacity:0.4;"></div>
        <div style="position:absolute; inset:0; background: radial-gradient(circle at 20% 20%, rgba(224,180,85,0.12), transparent 35%); opacity:0.7;"></div>
        <div style="position:relative; display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div class="pill" style="background: rgba(224,180,85,0.18); color:#ffd78a; border-color: rgba(224,180,85,0.45);">Executive Reports • Powered by IntaAgent™</div>
                <h2 style="margin: 6px 0 2px;">Lark Cafe — Financial Reporting Console</h2>
                <p style="color:#cbd7f0; margin:0;">Premium reporting — AED only, AI-guided insights, export-ready PDFs.</p>
            </div>
            <div style="text-align:right; color:#9fb0c7;">
                <div style="display:flex; align-items:center; gap:6px; justify-content:flex-end;">
                    <span class="pulse-dot" style="background:#1B76FF;"></span>
                    <span style="font-size:12px;">Live Mode (demo)</span>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Report selector tabs
tab_labels = [("💰 Profit Summary", "profit_summary"), ("🗑 Waste Report", "waste_report"), ("📊 Category Performance", "category_performance")]
selected_key = st.session_state.get("report_tab", "profit_summary")
tab_cols = st.columns(3)
for col, (label, key) in zip(tab_cols, tab_labels):
    active = "border:1px solid rgba(224,180,85,0.6); box-shadow:0 8px 20px rgba(224,180,85,0.35);" if selected_key == key else "border:1px solid rgba(255,255,255,0.08);"
    if col.button(label, use_container_width=True, key=f"tab_{key}"):
        selected_key = key
        st.session_state["report_tab"] = key
    col.markdown(
        f"<div style='height:2px; background:{'#E0B455' if selected_key == key else 'transparent'}; margin-top:-6px;'></div>",
        unsafe_allow_html=True,
    )

st.markdown("<p style='color:#9fb0c7; margin-top:6px;'>Select a financial report. All values shown in AED.</p>", unsafe_allow_html=True)

selected = reports.get(selected_key, [])

# Executive snapshot card
ai_sentence = (
    "Your profitability today is healthy. Revenue reached AED 3,450 with solid cost control and strong product mix performance."
)
tiles = [
    ("Trend", "↗ Upward momentum"),
    ("Efficiency", "High margin day"),
    ("Risk", "Milk stock low — monitor closely"),
]
st.markdown(
    """
    <div class="glass glass-strong glow-border animate-pop" style="padding:16px; margin-top:6px;">
        <div class="pill" style="background: rgba(27,118,255,0.14);">Executive Snapshot (AI Summary)</div>
        <p style="color:#cbd7f0; margin:6px 0 10px;">"""
    + ai_sentence
    + """</p>
    </div>
    """,
    unsafe_allow_html=True,
)
tile_cols = st.columns(3)
for col, (title, text) in zip(tile_cols, tiles):
    col.markdown(
        f"""
        <div class="glass animate-pop" style="padding:12px; border:1px solid rgba(27,118,255,0.25);">
            <div class="pill" style="background: rgba(27,118,255,0.12);">{title}</div>
            <div style="margin-top:6px; font-weight:700;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Report table + mini visuals
main_col, side_col = st.columns([1.8, 1], gap="medium")

with main_col:
    if selected:
        df = pd.DataFrame(selected)
        # Add AI insight column
        def insight_for(metric):
            return ai_insights.get(metric, "AI reviewing…")

        df["AI insight"] = df[df.columns[0]].apply(insight_for)

        def format_aed(val):
            return f"AED {val:,.0f}" if isinstance(val, (int, float)) else val

        df[df.columns[1]] = df[df.columns[1]].apply(format_aed)
        df.columns = ["Metric", "Value", "AI insight"]

        st.markdown(
            """
            <div class="glass glass-strong animate-pop" style="padding:12px; border-left: 3px solid rgba(224,180,85,0.6);">
                <div class="pill" style="background: rgba(224,180,85,0.14); color:#ffd78a;">Detailed Report</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(
            df.style.set_properties(
                **{
                    "background-color": "rgba(255,255,255,0.02)",
                    "border-color": "rgba(255,255,255,0.05)",
                    "border-radius": "8px",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No data available in the selected report.")

with side_col:
    # Mini visual 1: Daily profit trend
    if selected_key == "profit_summary":
        profit_vals = [r.get("value", 0) if isinstance(r, dict) else 0 for r in selected][:7]
    else:
        profit_vals = [3450, 3320, 3580, 3600, 3740, 3890, 4010]
    fig_profit = px.line(y=profit_vals, title="Daily Profit Trend", height=180)
    fig_profit.update_traces(line=dict(color="#1B76FF", width=3), marker=dict(size=6, color="#E0B455"))
    fig_profit.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color="#E8EEF9"),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    st.markdown("<div class='glass glass-strong animate-pop' style='padding:8px;'>", unsafe_allow_html=True)
    st.plotly_chart(fig_profit, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Mini visual 2: Category contribution bar
    cat_perf = reports.get("category_performance", [])
    cat_df = pd.DataFrame(cat_perf) if cat_perf else pd.DataFrame(
        [{"category": "Coffee", "value": 48}, {"category": "Cold Drinks", "value": 22}, {"category": "Food", "value": 18}, {"category": "Specialty", "value": 12}]
    )
    fig_cat = px.bar(cat_df, x="category", y="value", title="Category Contribution", height=200, color="value", color_continuous_scale=["#5FB1FF", "#1B76FF"])
    fig_cat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color="#E8EEF9"),
        coloraxis_showscale=False,
    )
    st.markdown("<div class='glass glass-strong animate-pop' style='padding:8px;'>", unsafe_allow_html=True)
    st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Mini visual 3: Expenses vs Revenue (mini pie)
    exp_rev = pd.DataFrame(
        [
            {"label": "Revenue", "value": 3450},
            {"label": "Expenses", "value": 2100},
        ]
    )
    fig_pie = px.pie(exp_rev, values="value", names="label", title="Expenses vs Revenue", hole=0.45, color_discrete_sequence=["#1B76FF", "#E0B455"], height=200)
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(color="#E8EEF9"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15),
    )
    st.markdown("<div class='glass glass-strong animate-pop' style='padding:8px;'>", unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# AI commentary strip
st.markdown(
    """
    <div class="glass animate-pop" style="border-left:4px solid #1B76FF; box-shadow: 0 0 16px rgba(27,118,255,0.25); margin-top:12px;">
        <strong>IntaAgent™: Expect profit uplift during evening peak hours based on product mix and historical demand.</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

# PDF preview panel
today = datetime.now().strftime("%d %b %Y")
st.markdown(
    f"""
    <div class="glass glass-strong animate-pop" style="padding:12px; max-width:420px; margin-top:10px;">
        <div style="font-weight:700;">Lark Cafe — Executive Report</div>
        <div style="color:#9fb0c7;">Date: {today}</div>
        <div style="color:#9fb0c7;">AED values only</div>
    </div>
    """,
    unsafe_allow_html=True,
)

pdf_bytes = build_pdf(selected_key, selected if isinstance(selected, list) else [])
if st.download_button(
    "🖨 Generate PDF",
    data=pdf_bytes,
    file_name="lark_executive_report.pdf",
    mime="application/pdf",
    use_container_width=True,
    help="Download professional-grade PDF",
):
    st.success("Your PDF report is ready.")
