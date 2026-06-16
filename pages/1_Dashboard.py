"""
Dashboard - Premium mission-control solar telemetry.
"""

from datetime import datetime

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.data_generator import SolarDataGenerator
from utils.prediction_engine import SolarFlarePredictor
from utils.visualizations import create_dual_axis_chart, create_gauge_chart, create_histogram, create_timeseries_chart


st.set_page_config(page_title="Solar Sentinel AI - Dashboard", layout="wide")

st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top left, rgba(34, 197, 94, 0.10), transparent 24%),
                radial-gradient(circle at top right, rgba(103, 232, 249, 0.10), transparent 24%),
                linear-gradient(180deg, #030712 0%, #050816 48%, #02040c 100%);
            color: #e5eefb;
        }
        .glass { border: 1px solid rgba(103, 232, 249, 0.14); border-radius: 22px; background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(3, 7, 18, 0.78)); box-shadow: 0 18px 50px rgba(0,0,0,.28); backdrop-filter: blur(18px); padding: 1rem 1.1rem; }
        .hero-title { font-size: clamp(2.3rem, 4vw, 4.2rem); line-height: 1; margin: 0; font-weight: 800; background: linear-gradient(90deg, #f8fafc 0%, #67e8f9 28%, #22c55e 70%, #facc15 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .eyebrow { letter-spacing: .24em; text-transform: uppercase; color: #67e8f9; font-size: .72rem; margin-bottom: .3rem; }
        .subtitle { color: #8aa0c2; font-size: .98rem; margin-top: .65rem; max-width: 980px; }
        .metric-label { color: #8aa0c2; font-size: .72rem; letter-spacing: .18em; text-transform: uppercase; margin-bottom: .45rem; }
        .metric-value { font-size: 2rem; font-weight: 800; margin: 0; }
        .metric-note { color: #8aa0c2; font-size: .82rem; margin-top: .25rem; }
        .section-title { margin: .5rem 0 .8rem; font-size: 1.05rem; color: #dbeafe; letter-spacing: .08em; text-transform: uppercase; }
        .pulse { display:inline-flex; align-items:center; gap:.45rem; padding:.45rem .8rem; border-radius:999px; background: rgba(34,197,94,.12); border: 1px solid rgba(34,197,94,.3); color:#bbf7d0; font-size:.82rem; font-weight:700; }
        .dot { width:10px; height:10px; border-radius:50%; background:#22c55e; box-shadow: 0 0 0 0 rgba(34,197,94,.6); animation: pulse 1.8s infinite; }
        @keyframes pulse { 0% { box-shadow:0 0 0 0 rgba(34,197,94,.5);} 70% { box-shadow:0 0 0 12px rgba(34,197,94,0);} 100% { box-shadow:0 0 0 0 rgba(34,197,94,0);} }
        .chip { display:inline-block; padding:.4rem .7rem; border-radius:999px; border:1px solid rgba(103,232,249,.18); background: rgba(103,232,249,.08); color:#e5eefb; font-size:.78rem; margin:.2rem .25rem 0 0; }
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

st.markdown(
    f"""
    <div class="glass">
        <div class="eyebrow">Mission Control / Aditya-L1 / Solar Flare Forecasting</div>
        <h1 class="hero-title">Solar Sentinel AI Dashboard</h1>
        <div class="subtitle">Premium mission-control dashboard for solar flare monitoring, forecasting, and response operations. Designed for scientific clarity and operational speed.</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px;">
            <span class="pulse"><span class="dot"></span>System Health 96%</span>
            <span class="pulse" style="background:rgba(250,204,21,.12); border-color:rgba(250,204,21,.28); color:#fef08a;"><span class="dot" style="background:#facc15; box-shadow:0 0 0 0 rgba(250,204,21,.6);"></span>Risk {prediction['risk_level']}</span>
            <span class="pulse" style="background:rgba(103,232,249,.12); border-color:rgba(103,232,249,.28); color:#cffafe;">Last Update {datetime.now().strftime('%H:%M:%S')}</span>
            <span class="pulse" style="background:rgba(251,146,60,.12); border-color:rgba(251,146,60,.28); color:#ffedd5;">Active Alerts {active_alerts}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

kpi_cols = st.columns(4, gap="large")
kpi_data = [
    ("Flare Probability", f"{prediction['probability_percent']:.1f}%", "15-minute nowcast", status_color),
    ("Predicted Class", prediction["flare_class"], "GOES classification", "#67e8f9"),
    ("Risk Level", prediction["risk_level"], "Operational severity", status_color),
    ("Active Alerts", str(active_alerts), "Auto-generated", "#fb923c"),
]

for col, (label, value, note, color) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(f"<div class='glass'><div class='metric-label'>{label}</div><div class='metric-value' style='color:{color};'>{value}</div><div class='metric-note'>{note}</div></div>", unsafe_allow_html=True)

st.write("")

left, middle, right = st.columns([1.1, 1.1, 0.9], gap="large")

with left:
    st.markdown("<div class='glass'><div class='section-title'>Live SoLEXS Telemetry</div></div>", unsafe_allow_html=True)
    solexs_chart = create_timeseries_chart(current_data, "timestamp", "soft_xray_flux", "Soft X-ray Flux", "Flux (W/m²)", color="#67e8f9")
    solexs_chart.update_traces(fill="tozeroy", fillcolor="rgba(103, 232, 249, 0.16)")
    st.plotly_chart(solexs_chart, use_container_width=True, config={"displayModeBar": False})

with middle:
    st.markdown("<div class='glass'><div class='section-title'>Live HELIOS Telemetry</div></div>", unsafe_allow_html=True)
    helios_chart = create_timeseries_chart(current_data, "timestamp", "hard_xray_counts", "Hard X-ray Counts", "Counts/sec", color="#fb923c")
    helios_chart.update_traces(fill="tozeroy", fillcolor="rgba(251, 146, 60, 0.16)")
    st.plotly_chart(helios_chart, use_container_width=True, config={"displayModeBar": False})

with right:
    st.markdown("<div class='glass'><div class='section-title'>Mission Control Panel</div></div>", unsafe_allow_html=True)
    st.metric("Prediction Horizon", "15 min")
    st.metric("Forecast Class", prediction["flare_class"])
    st.metric("Alert State", prediction["risk_level"])
    st.progress(min(prediction["probability_percent"] / 100, 1.0))
    st.caption("Live triage panel for operators and mission planners.")

st.write("")

panel_left, panel_right = st.columns([1.15, 0.85], gap="large")

with panel_left:
    st.markdown("<div class='glass'><div class='section-title'>Solar Fusion Timeline</div></div>", unsafe_allow_html=True)
    fusion_chart = create_dual_axis_chart(current_data, "timestamp", "soft_xray_flux", "hard_xray_counts", "SoLEXS / HELIOS Fusion", "Soft X-ray", "Hard X-ray", "#67e8f9", "#fb923c")
    fusion_chart.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fusion_chart, use_container_width=True, config={"displayModeBar": False})

with panel_right:
    st.markdown("<div class='glass'><div class='section-title'>AI Explainability</div></div>", unsafe_allow_html=True)
    contributions = predictor.generate_feature_contributions(prediction["features"])
    for name, value in contributions:
        st.markdown(f"<div class='glass' style='margin-top:.65rem;'><div class='metric-label'>{name}</div><div class='metric-value' style='font-size:1.35rem;'>{value:.0f}%</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass' style='margin-top:.65rem;'><div class='metric-label'>Reasoning</div><div class='metric-value' style='font-size:1.05rem;'>{prediction['explanation']}</div></div>", unsafe_allow_html=True)

st.write("")

alert_col, explain_col = st.columns([1, 1], gap="large")
with alert_col:
    st.markdown("<div class='glass'><div class='section-title'>Alert Center</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass' style='border-left:4px solid {status_color};'><div class='metric-label'>Latest Alert</div><div class='metric-value' style='font-size:1.5rem;color:{status_color};'>{prediction['risk_level']} WATCH</div><div class='metric-note'>{prediction['explanation']}</div></div>", unsafe_allow_html=True)

with explain_col:
    st.markdown("<div class='glass'><div class='section-title'>Explainability Snapshot</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass'><div class='metric-label'>Top Driver</div><div class='metric-value' style='font-size:1.4rem;'>{contributions[0][0]}</div><div class='metric-note'>{contributions[0][1]:.0f}% contribution to current risk</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='glass' style='margin-top:.65rem;'><div class='metric-label'>Signal Summary</div><div class='metric-value' style='font-size:1.05rem;'>Soft X-ray trend + hard X-ray spike</div></div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<div style='text-align:center;color:#8aa0c2;font-size:.85rem;'>Solar Sentinel AI mission control is operating in simulated mode for hackathon demo purposes · Updated {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    st.write("")
