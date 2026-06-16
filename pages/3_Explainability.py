"""
Explainability Dashboard - Feature Contributions and Model Interpretability
SHAP-style feature importance visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_generator import SolarDataGenerator
from utils.prediction_engine import SolarFlarePredictor
from utils.visualizations import create_bar_chart


def render_explainability():
    """Render the explainability page"""
    
    st.set_page_config(page_title="Solar Sentinel AI - Explainability", layout="wide")
    
    st.markdown("""
        <style>
            body { background-color: #0a0e27; color: #ffffff; }
            .main { background-color: #0a0e27; }
            h1, h2, h3, h4, h5, h6 { color: #00FF00; font-weight: bold; }
            .feature-card {
                background-color: #1a1f3a;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #00FF00;
                margin: 15px 0;
            }
            .feature-name { color: #00FF00; font-weight: bold; }
            .feature-value { color: #FF6600; font-size: 18px; font-weight: bold; }
            .explanation-box {
                background-color: #0f1729;
                padding: 15px;
                border-left: 3px solid #00FF00;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>🧠 EXPLAINABILITY DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>AI Model Interpretability & Feature Analysis</p>", 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Generate data
    gen = SolarDataGenerator()
    current_data = gen.get_latest_data(n_hours=1)
    
    solexs_values = current_data['soft_xray_flux'].values
    helios_values = current_data['hard_xray_counts'].values
    
    predictor = SolarFlarePredictor()
    prediction = predictor.predict_flare(solexs_values, helios_values, horizon_minutes=15)
    
    # Feature Contributions
    st.markdown("<h2>📊 Feature Importance</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>SHAP-style feature contribution analysis</p>", 
                unsafe_allow_html=True)
    
    contributions = predictor.generate_feature_contributions(prediction['features'])
    
    # Create visualization
    feature_names = [c[0] for c in contributions]
    feature_values = [c[1] for c in contributions]
    
    importance_chart = create_bar_chart(
        feature_values,
        feature_names,
        "Feature Contributions to Flare Probability",
        colors=['#00FF00', '#FFFF00', '#FF6600', '#FF3333'],
        orientation='h'
    )
    st.plotly_chart(importance_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Feature Breakdown
    st.markdown("<h2>🔍 Detailed Feature Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # SoLEXS Features
    with col1:
        st.markdown("<h3 style='color: #00FF00;'>☀️ SoLEXS Features</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Soft X-ray Flux</div>
                <div class="feature-value">{prediction['features']['soft_xray_flux']:.2f} W/m²</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Current emission level in the soft X-ray spectrum (1-12 Å)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Soft X-ray Trend</div>
                <div class="feature-value">{prediction['features']['soft_xray_trend']:+.4f}</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Rate of change in soft X-ray emissions (positive = increasing)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Soft X-ray Volatility</div>
                <div class="feature-value">{prediction['features']['soft_xray_volatility']:.2f}</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Variability in soft X-ray measurements (σ over 30-minute window)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # HELIOS Features
    with col2:
        st.markdown("<h3 style='color: #FF6600;'>⚡ HELIOS Features</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Hard X-ray Counts</div>
                <div class="feature-value">{prediction['features']['hard_xray_counts']:.0f} counts/sec</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Current count rate in hard X-ray spectrum (4-25 keV)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Hard X-ray Trend</div>
                <div class="feature-value">{prediction['features']['hard_xray_trend']:+.4f}</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Rate of change in hard X-ray count rates (positive = increasing)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Hard X-ray Spike</div>
                <div class="feature-value">{prediction['features']['hard_xray_spike']:.2f}</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Peak-to-valley variation in last 20 minutes (detection of sharp events)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Derived Features
    st.markdown("<h2>🔗 Derived Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Flux-to-Counts Ratio</div>
                <div class="feature-value">{prediction['features']['flux_to_counts_ratio']:.3f}</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Ratio between soft and hard X-ray activity (characterizes flare spectrum)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-name">Activity Index</div>
                <div class="feature-value">{prediction['features']['activity_index']:.2f}</div>
                <p style="color: #888; font-size: 12px; margin-top: 10px;">
                    Combined solar activity metric (normalized 0-10 scale)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Decision Logic
    st.markdown("<h2>🤖 Model Decision Logic</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="explanation-box">
            <h4 style="margin-top: 0; color: #00FF00;">How the AI Predicts Flares</h4>
            <p>
            The Solar Sentinel AI uses a weighted ensemble approach combining multiple features:
            </p>
            <ul>
                <li><b>Soft X-ray Analysis (35% weight):</b> Detects heating in the solar corona</li>
                <li><b>Hard X-ray Analysis (35% weight):</b> Identifies energetic particle acceleration</li>
                <li><b>Temporal Trends (20% weight):</b> Captures rapidly changing conditions</li>
                <li><b>Volatility Index (10% weight):</b> Measures destabilization of solar magnetic fields</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Prediction Score Breakdown
    st.markdown("<h3>📈 Prediction Score Breakdown</h3>", unsafe_allow_html=True)
    
    breakdown_data = pd.DataFrame({
        'Component': ['Soft X-ray', 'Hard X-ray', 'Trend Analysis', 'Volatility'],
        'Weight': ['35%', '35%', '20%', '10%'],
        'Current Contribution': [
            f"{min(prediction['features']['soft_xray_flux'] / 10, 1.0) * 0.35 * 100:.1f}%",
            f"{min(prediction['features']['hard_xray_counts'] / 500, 1.0) * 0.35 * 100:.1f}%",
            f"{min(abs(prediction['features']['soft_xray_trend']) + abs(prediction['features']['hard_xray_trend']), 1.0) * 0.20 * 100:.1f}%",
            f"{min(prediction['features']['soft_xray_volatility'] / 5, 1.0) * 0.10 * 100:.1f}%"
        ]
    })
    
    st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Feature Correlations
    st.markdown("<h2>📊 Feature Correlations</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="explanation-box">
            <p>
            <b>Soft X-ray ↔ Hard X-ray Correlation:</b><br>
            Strong correlation indicates flare activity across energy spectra (typical for large flares)
            </p>
            <p>
            <b>Trend Components:</b><br>
            Positive trends in both channels suggest acceleration phase of flare evolution
            </p>
            <p>
            <b>Volatility Indicators:</b><br>
            High volatility before flares indicates magnetic field restructuring and energy release preparation
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Confidence Explanation
    st.markdown("<h2>🎯 Confidence Score Explanation</h2>", unsafe_allow_html=True)
    
    confidence = prediction['confidence']
    confidence_pct = confidence * 100
    
    if confidence > 0.85:
        confidence_msg = "Very High - Model predictions are highly reliable"
        confidence_color = "#00FF00"
    elif confidence > 0.75:
        confidence_msg = "High - Model predictions are reliable"
        confidence_color = "#FFFF00"
    elif confidence > 0.65:
        confidence_msg = "Medium - Use predictions with caution"
        confidence_color = "#FF6600"
    else:
        confidence_msg = "Low - Predictions highly uncertain"
        confidence_color = "#FF0000"
    
    st.markdown(f"""
        <div style="background-color: #1a1f3a; padding: 20px; border-radius: 10px; 
                    border-left: 5px solid {confidence_color};">
            <h3 style="color: {confidence_color}; margin-top: 0;">Confidence: {confidence_pct:.1f}%</h3>
            <p style="font-size: 16px; margin: 10px 0;">{confidence_msg}</p>
            <p style="color: #888; font-size: 12px;">
                Confidence reflects model uncertainty based on feature signal strength and historical accuracy.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        <p style="color: #888; font-size: 12px; text-align: center;">
            Model: Solar Flare Prediction Engine v1.0 | Last Training: Baseline Model
        </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_explainability()
