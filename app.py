"""
Solar Sentinel AI - Mission control landing dashboard.
"""

from datetime import datetime

import plotly.graph_objects as go
import streamlit as st

from utils.data_generator import SolarDataGenerator
from utils.prediction_engine import SolarFlarePredictor


st.set_page_config(
    page_title="Solar Sentinel AI | Mission Control",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Solar Sentinel AI mission-control interface",
    },
)

st.markdown(
    """
    <style>
        :root {
            --bg: #050816;
            --panel: rgba(15, 23, 42, 0.76);
            --line: rgba(103, 232, 249, 0.16);
            --cyan: #67e8f9;
            --green: #22c55e;
            --yellow: #facc15;
            --orange: #fb923c;
            --red: #ef4444;
            --text: #e5eefb;
            --muted: #8aa0c2;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top left, rgba(34, 197, 94, 0.12), transparent 25%),
                radial-gradient(circle at top right, rgba(103, 232, 249, 0.12), transparent 24%),
                linear-gradient(180deg, #030712 0%, #050816 45%, #02040c 100%);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(2, 6, 23, 0.96), rgba(15, 23, 42, 0.92));
            border-right: 1px solid rgba(103, 232, 249, 0.14);
        }

        .hero {
            padding: 1.2rem 1.4rem;
            border: 1px solid var(--line);
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.88), rgba(3, 7, 18, 0.78));
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(18px);
        }

        .eyebrow { letter-spacing: 0.22em; text-transform: uppercase; color: var(--cyan); font-size: 0.72rem; margin-bottom: 0.3rem; }
        .title { font-size: 3.1rem; line-height: 1.0; margin: 0; font-weight: 800; background: linear-gradient(90deg, #f8fafc 0%, #67e8f9 28%, #22c55e 70%, #facc15 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: var(--muted); font-size: 0.98rem; margin-top: 0.65rem; }
        .glass-card { border: 1px solid rgba(103, 232, 249, 0.14); border-radius: 22px; padding: 1rem 1.1rem; background: linear-gradient(180deg, rgba(15, 23, 42, 0.85), rgba(2, 6, 23, 0.8)); box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 12px 40px rgba(0, 0, 0, 0.24); }
        .metric-label { color: var(--muted); font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 0.5rem; }
        .metric-value { font-size: 2rem; font-weight: 800; margin: 0; color: var(--text); }
        .metric-note { color: var(--muted); font-size: 0.82rem; margin-top: 0.25rem; }
        .status-pulse { display: inline-flex; align-items: center; gap: 0.45rem; padding: 0.45rem 0.8rem; border-radius: 999px; background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.3); color: #bbf7d0; font-size: 0.82rem; font-weight: 700; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.6); animation: pulse 1.8s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.5); } 70% { box-shadow: 0 0 0 12px rgba(34, 197, 94, 0); } 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); } }
        .section-title { margin: 0.5rem 0 0.8rem; font-size: 1.05rem; color: #dbeafe; letter-spacing: 0.08em; text-transform: uppercase; }
        .sidebar-title { font-size: 1.15rem; font-weight: 800; letter-spacing: 0.12em; }
        .nav-chip { display: inline-block; margin: 0.18rem 0.3rem 0 0; padding: 0.4rem 0.7rem; border-radius: 999px; border: 1px solid rgba(103, 232, 249, 0.18); background: rgba(103, 232, 249, 0.08); color: var(--text); font-size: 0.78rem; }
        .footer-line { color: var(--muted); font-size: 0.82rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

generator = SolarDataGenerator()
predictor = SolarFlarePredictor()
current_data = generator.get_latest_data(n_hours=1)
prediction = predictor.predict_flare(current_data["soft_xray_flux"].values, current_data["hard_xray_counts"].values, 15)
prediction_60 = predictor.predict_flare(current_data["soft_xray_flux"].values, current_data["hard_xray_counts"].values, 60)

risk_palette = {"LOW": "#22c55e", "MEDIUM": "#facc15", "HIGH": "#fb923c", "CRITICAL": "#ef4444"}
status_color = risk_palette.get(prediction["risk_level"], "#22c55e")
active_alerts = 1 if prediction["risk_level"] in {"HIGH", "CRITICAL"} else 2 if prediction_60["risk_level"] == "HIGH" else 0

with st.sidebar:
    st.markdown("<div class='sidebar-title'>☀️ SOLAR SENTINEL AI</div>", unsafe_allow_html=True)
    st.caption("Mission-control solar flare intelligence")
    st.markdown("<span class='nav-chip'>SoLEXS</span><span class='nav-chip'>HELIOS</span><span class='nav-chip'>Aditya-L1</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navigation**")
    st.page_link("app.py", label="Home Mission Control", icon="🛰️")
    st.page_link("pages/1_Dashboard.py", label="Telemetry Dashboard", icon="📡")
    st.page_link("pages/2_Forecast.py", label="Forecast Center", icon="🔮")
    st.page_link("pages/3_Explainability.py", label="Explainability", icon="🧠")
    st.page_link("pages/4_Alerts.py", label="Alert Center", icon="🚨")
    st.page_link("pages/5_Analytics.py", label="Analytics", icon="📈")
    st.markdown("---")
    st.markdown("**System Health**")
    st.markdown("<div class='status-pulse'><span class='status-dot'></span>Operational</div>", unsafe_allow_html=True)
    st.progress(0.96)
    st.caption("Instrument link, AI engine, and alert pipeline healthy")
    st.markdown("---")
    st.metric("Active Alerts", active_alerts)
    st.metric("Risk Level", prediction["risk_level"].title())
    st.caption(f"Last sync: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}")

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Mission Control / Aditya-L1 / Solar Flare Forecasting</div>
        <h1 class="title">Solar Sentinel AI</h1>
        <div class="subtitle">Premium forecasting and early-warning command surface for SoLEXS and HELIOS telemetry. Built for operational clarity, rapid triage, and future real-data integration.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

left, right = st.columns([1.1, 0.9], gap="large")
with left:
    st.markdown("<div class='glass-card'><div class='section-title'>Mission Summary</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-label'>Flare Probability</div><div class='metric-value' style='color:{status_color};'>{prediction['probability_percent']:.1f}%</div><div class='metric-note'>15-minute nowcast</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-label'>Predicted Class</div><div class='metric-value' style='color:#67e8f9;'>{prediction['flare_class']}</div><div class='metric-note'>GOES classification</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-label'>Risk Level</div><div class='metric-value' style='color:{status_color};'>{prediction['risk_level']}</div><div class='metric-note'>Operational status</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='footer-line'>Last update: {datetime.now().strftime('%d %b %Y · %H:%M:%S')}</div></div>", unsafe_allow_html=True)

with right:
    st.metric("System Health", "96%")
    st.metric("Active Alerts", active_alerts)
    st.metric("Mission Mode", "WATCH")
    st.metric("Confidence", f"{prediction['confidence'] * 100:.0f}%")

st.write("")

st.markdown("<div class='glass-card'><div class='section-title'>Live Mission Control</div></div>", unsafe_allow_html=True)
feature_contribs = predictor.generate_feature_contributions(prediction["features"])
feature_chart = go.Figure(go.Bar(
    x=[value for _, value in feature_contribs][::-1],
    y=[name for name, _ in feature_contribs][::-1],
    orientation="h",
    marker={
        "color": [value for _, value in feature_contribs][::-1],
        "colorscale": [[0, "#22c55e"], [0.5, "#67e8f9"], [1, "#fb923c"]],
        "line": {"color": "rgba(255,255,255,0.18)", "width": 1},
    },
    text=[f"{value:.0f}%" for _, value in feature_contribs][::-1],
    textposition="outside",
    hovertemplate="%{y}<br>Contribution: %{x:.1f}%<extra></extra>",
))
feature_chart.update_layout(
    height=320,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin={"l": 20, "r": 20, "t": 10, "b": 10},
    xaxis={"visible": False, "range": [0, max([value for _, value in feature_contribs]) * 1.18]},
    yaxis={"tickfont": {"color": "#e5eefb"}},
    showlegend=False,
)
st.plotly_chart(feature_chart, use_container_width=True, config={"displayModeBar": False})

