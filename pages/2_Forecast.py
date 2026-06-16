"""
Forecast Center - Multi-horizon Solar Flare Forecasting
Shows predictions at different time horizons (15min, 1hr, 6hr)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_generator import SolarDataGenerator
from utils.prediction_engine import SolarFlarePredictor
from utils.visualizations import create_gauge_chart, create_bar_chart


def render_forecast():
    """Render the forecast center page"""
    
    st.set_page_config(page_title="Solar Sentinel AI - Forecast Center", layout="wide")
    
    st.markdown("""
        <style>
            body { background-color: #0a0e27; color: #ffffff; }
            .main { background-color: #0a0e27; }
            h1, h2, h3, h4, h5, h6 { color: #00FF00; font-weight: bold; }
            .forecast-card {
                background-color: #1a1f3a;
                padding: 25px;
                border-radius: 10px;
                border-left: 5px solid #00FF00;
                margin-bottom: 20px;
            }
            .forecast-header { color: #00FF00; font-size: 16px; font-weight: bold; }
            .risk-badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>🔮 FORECAST CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Multi-Horizon Solar Flare Predictions</p>", 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Generate data
    gen = SolarDataGenerator()
    current_data = gen.get_latest_data(n_hours=1)
    
    solexs_values = current_data['soft_xray_flux'].values
    helios_values = current_data['hard_xray_counts'].values
    
    predictor = SolarFlarePredictor()
    
    # Three prediction horizons
    horizons = [15, 60, 360]
    horizon_labels = ["15-Minute Forecast", "1-Hour Forecast", "6-Hour Forecast"]
    
    st.markdown("<h2>📊 Forecasting Horizons</h2>", unsafe_allow_html=True)
    
    predictions = {}
    for horizon, label in zip(horizons, horizon_labels):
        predictions[horizon] = predictor.predict_flare(solexs_values, helios_values, horizon)
    
    # Display predictions in columns
    col1, col2, col3 = st.columns(3)
    
    columns = [col1, col2, col3]
    for idx, (horizon, label) in enumerate(zip(horizons, horizon_labels)):
        pred = predictions[horizon]
        
        with columns[idx]:
            risk_colors = {
                'LOW': '#00FF00',
                'MEDIUM': '#FFFF00',
                'HIGH': '#FF6600',
                'CRITICAL': '#FF0000'
            }
            risk_color = risk_colors.get(pred['risk_level'], '#00FF00')
            
            st.markdown(f"""
                <div class="forecast-card">
                    <div class="forecast-header">{label}</div>
                    
                    <p style="color: #888; font-size: 12px; margin-top: 15px;">Flare Probability</p>
                    <p style="color: #00FF00; font-size: 36px; margin: 5px 0; font-weight: bold;">
                        {pred['probability_percent']:.1f}%
                    </p>
                    
                    <p style="color: #888; font-size: 12px; margin-top: 15px;">Predicted Class</p>
                    <p style="color: #FF6600; font-size: 28px; margin: 5px 0; font-weight: bold;">
                        {pred['flare_class']} CLASS
                    </p>
                    
                    <div class="risk-badge" style="background-color: {risk_color}; color: #000;">
                        Risk: {pred['risk_level']}
                    </div>
                    
                    <p style="color: #888; font-size: 11px; margin-top: 15px;">
                        Confidence: {pred['confidence']:.1%}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed Comparison
    st.markdown("<h2>📈 Forecast Comparison</h2>", unsafe_allow_html=True)
    
    # Extract probabilities for comparison
    probs = [predictions[h]['probability_percent'] for h in horizons]
    col1, col2 = st.columns(2)
    
    with col1:
        prob_chart = create_bar_chart(
            probs,
            horizon_labels,
            "Flare Probability by Horizon",
            colors=['#00FF00', '#FFFF00', '#FF6600']
        )
        st.plotly_chart(prob_chart, use_container_width=True)
    
    with col2:
        # Flare class distribution
        flare_classes = [predictions[h]['flare_class'] for h in horizons]
        class_scores = {
            'A': 0, 'B': 20, 'C': 40, 'M': 70, 'X': 100
        }
        class_values = [class_scores[fc] for fc in flare_classes]
        
        class_chart = create_bar_chart(
            class_values,
            [f"{fc} Class" for fc in flare_classes],
            "Predicted Flare Class Severity",
            colors=['#00FF00', '#FFFF00', '#FF6600']
        )
        st.plotly_chart(class_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Risk Assessment Matrix
    st.markdown("<h2>⚠️ Risk Assessment Matrix</h2>", unsafe_allow_html=True)
    
    risk_matrix = pd.DataFrame({
        'Horizon': ['15 Minutes', '1 Hour', '6 Hours'],
        'Probability': [f"{predictions[h]['probability_percent']:.1f}%" for h in horizons],
        'Class': [predictions[h]['flare_class'] for h in horizons],
        'Risk Level': [predictions[h]['risk_level'] for h in horizons],
        'Confidence': [f"{predictions[h]['confidence']:.1%}" for h in horizons]
    })
    
    st.dataframe(risk_matrix, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Forecast Details
    st.markdown("<h2>📋 Detailed Forecast Analysis</h2>", unsafe_allow_html=True)
    
    for horizon, label in zip(horizons, horizon_labels):
        pred = predictions[horizon]
        
        with st.expander(f"🔍 {label} Details"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Probability", f"{pred['probability_percent']:.1f}%")
            
            with col2:
                st.metric("Predicted Class", pred['flare_class'])
            
            with col3:
                st.metric("Risk Level", pred['risk_level'])
            
            st.write("**Analysis:**")
            st.info(pred['explanation'])
            
            st.write("**Key Features:**")
            features = pred['features']
            feature_text = f"""
            - Soft X-ray Flux: {features['soft_xray_flux']:.2f} W/m²
            - Hard X-ray Counts: {features['hard_xray_counts']:.0f} counts/sec
            - Soft X-ray Trend: {features['soft_xray_trend']:+.4f}
            - Hard X-ray Spike: {features['hard_xray_spike']:.2f}
            - Activity Index: {features['activity_index']:.2f}
            """
            st.write(feature_text)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("<h2>💡 Operational Recommendations</h2>", unsafe_allow_html=True)
    
    max_risk_index = np.argmax([predictions[h]['risk_level'] in ['HIGH', 'CRITICAL'] for h in horizons])
    max_prob_horizon = horizons[np.argmax(probs)]
    
    recommendations = []
    
    if predictions[15]['risk_level'] in ['HIGH', 'CRITICAL']:
        recommendations.append("🚨 **IMMEDIATE ALERT**: High flare probability in next 15 minutes. Prepare contingency protocols.")
    
    if predictions[60]['risk_level'] in ['HIGH', 'CRITICAL']:
        recommendations.append("⚠️ **HEIGHTENED ALERT**: Elevated flare activity expected within 1 hour. Monitor closely.")
    
    if predictions[360]['probability_percent'] > 70:
        recommendations.append("📢 **ADVISORY**: Elevated risk persists over 6-hour window. Continue monitoring.")
    
    if not recommendations:
        recommendations.append("✅ **NORMAL**: Solar activity within expected parameters. Continue routine monitoring.")
    
    for rec in recommendations:
        st.info(rec)
    
    st.markdown("---")
    st.markdown("""
        <p style="color: #888; font-size: 12px; text-align: center;">
            Last Update: Now | Next Update: 1 minute
        </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_forecast()
