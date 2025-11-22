import streamlit as st


def apply_theme():
    """Apply global dark, glassmorphic theme for Lark Executive Suite."""
    accent_choice = st.session_state.get("accent_color", "Blue")
    primary = "#1B76FF" if accent_choice == "Blue" else "#E0B455"
    st.set_page_config(
        page_title="Lark Executive Suite",
        page_icon="💠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        f"""
        <meta name="viewport" content="width=device-width, initial-scale=0.47, maximum-scale=1.0">
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        :root {{
            --lark-blue: {primary};
            --lark-gold: #E0B455;
            --card: rgba(255, 255, 255, 0.05);
            --card-strong: rgba(255, 255, 255, 0.08);
            --stroke: rgba(255, 255, 255, 0.12);
            --text: #E8EEF9;
        }}
        html {{ font-size: 70%; }}
        * {{ font-family: 'Inter', 'SF Pro Display', system-ui, -apple-system, sans-serif; }}
        body {{ color: var(--text); }}
        .stApp {{
            background: linear-gradient(180deg, #081A2B 0%, #030A14 100%);
            color: var(--text);
        }}
        .block-container {{ padding: 32px 64px 64px 64px; }}
        .glass {{
            background: var(--card);
            border: 1px solid var(--stroke);
            box-shadow: 0 18px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
            border-radius: 16px;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            padding: 18px 20px;
            margin-bottom: 18px;
        }}
        .glass-strong {{ background: var(--card-strong); }}
        .gold-frame {{ border: 1px solid var(--lark-gold); box-shadow: 0 0 24px rgba(224,180,85,0.35); }}
        .pill {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(27,118,255,0.1);
            color: #9fc4ff;
            border: 1px solid rgba(27,118,255,0.3);
            font-size: 12px;
        }}
        h1, h2, h3, h4 {{ color: #F3F6FF; letter-spacing: -0.2px; }}
        .kpi-card {{
            border-radius: 18px;
            padding: 14px 16px;
            background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 12px 30px rgba(0,0,0,0.35);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            animation: fadein 0.6s ease;
        }}
        .kpi-icon {{ font-size: 18px; margin-right: 6px; }}
        .kpi-value {{ font-size: 30px; font-weight: 700; color: #F3F6FF; }}
        .kpi-sub {{ color: #9fb0c7; font-size: 13px; }}
        .glow-gold {{ box-shadow: 0 0 18px rgba(224,180,85,0.45) !important; }}
        .glow-blue {{ box-shadow: 0 0 18px rgba(27,118,255,0.45) !important; }}
        .stButton>button {{
            width: 100%;
            border-radius: 14px;
            color: #0B1324;
            background: linear-gradient(120deg, var(--lark-gold), #ffd78a);
            border: none;
            font-weight: 600;
            padding: 12px 16px;
            box-shadow: 0 10px 30px rgba(224,180,85,0.35);
            transition: transform 0.15s ease, box-shadow 0.2s ease;
        }}
        .stButton>button:hover {{ transform: translateY(-1px); box-shadow: 0 16px 32px rgba(27,118,255,0.22); }}
        .stButton>button:focus {{ outline: 2px solid rgba(27,118,255,0.45); }}
        [data-testid="stSidebar"] {{
            background: rgba(7,11,20,0.85);
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(255,255,255,0.05);
        }}
        [data-testid="stSidebarNav"] {{ display: none !important; }}
        [data-testid="stSidebar"] .stButton>button {{
            background: linear-gradient(130deg, #E0B455, #f7d88a);
            color: #0B1324;
            border: 1px solid rgba(224,180,85,0.6);
            box-shadow: 0 12px 28px rgba(224,180,85,0.35);
        }}
        .nav-active button {{ border-bottom: 2px solid #E0B455 !important; }}
        .divider {{
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, rgba(27,118,255,0), rgba(27,118,255,0.45), rgba(27,118,255,0));
            margin: 14px 0 20px;
        }}
        .futuristic-card {{
            border-radius: 16px;
            padding: 20px;
            background: linear-gradient(135deg, rgba(27,118,255,0.08), rgba(255,255,255,0.03));
            border: 1px solid rgba(27,118,255,0.25);
            position: relative;
            overflow: hidden;
            margin-bottom: 14px;
        }}
        .futuristic-card::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 20% 20%, rgba(224,180,85,0.18), transparent 35%);
            opacity: 0.6;
            pointer-events: none;
        }}
        .glow-border {{
            border: 1px solid rgba(27,118,255,0.4);
            box-shadow: 0 0 18px rgba(27,118,255,0.35), inset 0 0 24px rgba(27,118,255,0.08);
        }}
        .animate-pop {{ animation: pop 0.4s ease; }}
        .fade-in {{ animation: fadein 0.6s ease forwards; }}
        .slide-up {{ animation: slideup 0.5s ease; }}
        .pulse-dot {{
            width: 10px; height: 10px; border-radius: 50%;
            background: var(--lark-blue);
            box-shadow: 0 0 0 0 rgba(27,118,255,0.6);
            animation: pulse 1.5s infinite;
            display: inline-block;
        }}
        .ai-avatar {{
            width: 36px; height: 36px; border-radius: 50%;
            background: linear-gradient(145deg, rgba(27,118,255,0.4), rgba(224,180,85,0.4));
            box-shadow: 0 0 14px rgba(27,118,255,0.4);
            display: inline-flex; align-items: center; justify-content: center;
        }}
        .ripple {{
            position: relative;
            overflow: hidden;
        }}
        .ripple::after {{
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 16px;
            border: 1px solid rgba(27,118,255,0.18);
            animation: ripple 5s infinite;
        }}
        @media (max-width: 768px) {{
            html {{ zoom: 0.47; }}
            .block-container {{ padding: 16px !important; }}
            [data-testid="stSidebar"] {{ display: none; }}
        }}
        @keyframes pop {{ from {{ transform: translateY(6px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
        @keyframes fadein {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @keyframes slideup {{ from {{ transform: translateY(12px); opacity:0; }} to {{ transform: translateY(0); opacity:1; }} }}
        @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(27,118,255,0.6); }} 70% {{ box-shadow: 0 0 0 10px rgba(27,118,255,0); }} 100% {{ box-shadow: 0 0 0 0 rgba(27,118,255,0); }} }}
        @keyframes ripple {{ 0% {{ opacity:0.35; transform: scale(0.98); }} 50% {{ opacity:0.12; transform: scale(1.02); }} 100% {{ opacity:0.35; transform: scale(0.98); }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )
