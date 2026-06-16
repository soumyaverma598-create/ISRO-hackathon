"""
Analytics Dashboard - Historical Analysis and Trends
Shows historical flare data, risk distribution, and analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_generator import generate_historical_data
from utils.prediction_engine import SolarFlarePredictor
from utils.visualizations import (
    create_timeseries_chart, create_histogram, create_heatmap,
    create_scatter_plot, create_bar_chart
)


def render_analytics():
    """Render the analytics page"""
    
    st.set_page_config(page_title="Solar Sentinel AI - Analytics", layout="wide")
    
    st.markdown("""
        <style>
            body { background-color: #0a0e27; color: #ffffff; }
            .main { background-color: #0a0e27; }
            h1, h2, h3, h4, h5, h6 { color: #00FF00; font-weight: bold; }
            .stat-box {
                background-color: #1a1f3a;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #00FF00;
                margin: 10px 0;
            }
            .stat-value { color: #00FF00; font-size: 32px; font-weight: bold; margin: 10px 0; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>📊 ANALYTICS DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Historical Trends & Statistical Analysis</p>", 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Generate historical data
    historical_data = generate_historical_data(days=30)
    
    # Summary Statistics
    st.markdown("<h2>📈 30-Day Summary Statistics</h2>", unsafe_allow_html=True)
    
    solexs_mean = historical_data['soft_xray_flux'].mean()
    solexs_max = historical_data['soft_xray_flux'].max()
    helios_mean = historical_data['hard_xray_counts'].mean()
    helios_max = historical_data['hard_xray_counts'].max()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <p style="color: #888; font-size: 12px; margin: 0;">Avg Soft X-ray</p>
                <div class="stat-value">{solexs_mean:.2f}</div>
                <p style="color: #888; font-size: 11px; margin: 0;">W/m²</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <p style="color: #888; font-size: 12px; margin: 0;">Peak Soft X-ray</p>
                <div class="stat-value">{solexs_max:.2f}</div>
                <p style="color: #888; font-size: 11px; margin: 0;">W/m²</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-box">
                <p style="color: #888; font-size: 12px; margin: 0;">Avg Hard X-ray</p>
                <div class="stat-value">{helios_mean:.0f}</div>
                <p style="color: #888; font-size: 11px; margin: 0;">counts/sec</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-box">
                <p style="color: #888; font-size: 12px; margin: 0;">Peak Hard X-ray</p>
                <div class="stat-value">{helios_max:.0f}</div>
                <p style="color: #888; font-size: 11px; margin: 0;">counts/sec</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Historical Trends
    st.markdown("<h2>📉 30-Day Trends</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        solexs_chart = create_timeseries_chart(
            historical_data, 'timestamp', 'soft_xray_flux',
            'Soft X-ray Flux Trend (30 Days)',
            'Flux (W/m²)',
            color='#00FF00'
        )
        st.plotly_chart(solexs_chart, use_container_width=True)
    
    with col2:
        helios_chart = create_timeseries_chart(
            historical_data, 'timestamp', 'hard_xray_counts',
            'Hard X-ray Counts Trend (30 Days)',
            'Count Rate (counts/sec)',
            color='#FF6600'
        )
        st.plotly_chart(helios_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Distribution Analysis
    st.markdown("<h2>📊 Distribution Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        solexs_hist = create_histogram(
            historical_data['soft_xray_flux'].tolist(),
            'Soft X-ray Flux Distribution',
            'Flux (W/m²)',
            nbins=40,
            color='#00FF00'
        )
        st.plotly_chart(solexs_hist, use_container_width=True)
    
    with col2:
        helios_hist = create_histogram(
            historical_data['hard_xray_counts'].tolist(),
            'Hard X-ray Counts Distribution',
            'Count Rate (counts/sec)',
            nbins=40,
            color='#FF6600'
        )
        st.plotly_chart(helios_hist, use_container_width=True)
    
    st.markdown("---")
    
    # Correlation Analysis
    st.markdown("<h2>🔗 Feature Correlation</h2>", unsafe_allow_html=True)
    
    scatter = create_scatter_plot(
        historical_data['soft_xray_flux'].tolist(),
        historical_data['hard_xray_counts'].tolist(),
        'Soft X-ray vs Hard X-ray Correlation',
        'Soft X-ray Flux (W/m²)',
        'Hard X-ray Counts (counts/sec)',
        color='#00FF00'
    )
    st.plotly_chart(scatter, use_container_width=True)
    
    correlation = historical_data['soft_xray_flux'].corr(historical_data['hard_xray_counts'])
    st.metric("Correlation Coefficient", f"{correlation:.3f}")
    
    st.markdown("---")
    
    # Daily Activity Heatmap
    st.markdown("<h2>🌡️ Daily Activity Heatmap</h2>", unsafe_allow_html=True)
    
    # Create hourly aggregation
    historical_data['hour'] = historical_data['timestamp'].dt.hour
    historical_data['day'] = historical_data['timestamp'].dt.date
    
    daily_hourly = historical_data.groupby(['day', 'hour'])['soft_xray_flux'].mean().unstack(fill_value=0)
    
    heatmap_data = daily_hourly.values[-7:] if len(daily_hourly) >= 7 else daily_hourly.values
    heatmap_labels = [str(d) for d in daily_hourly.index[-7:]] if len(daily_hourly) >= 7 else [str(d) for d in daily_hourly.index]
    
    heatmap = create_heatmap(
        heatmap_data,
        [f"{h:02d}:00" for h in range(24)],
        heatmap_labels,
        'Hourly Soft X-ray Activity (Last 7 Days)',
        colorscale='YlOrRd'
    )
    st.plotly_chart(heatmap, use_container_width=True)
    
    st.markdown("---")
    
    # Risk Statistics
    st.markdown("<h2>⚠️ Historical Risk Analysis</h2>", unsafe_allow_html=True)
    
    # Simulate risk levels over time
    predictor = SolarFlarePredictor()
    risk_counts = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0}
    
    for i in range(len(historical_data) - 100):
        solexs_window = historical_data['soft_xray_flux'].iloc[i:i+100].values
        helios_window = historical_data['hard_xray_counts'].iloc[i:i+100].values
        pred = predictor.predict_flare(solexs_window, helios_window, 15)
        risk_counts[pred['risk_level']] += 1
    
    total_predictions = sum(risk_counts.values())
    if total_predictions > 0:
        risk_percentages = [
            (risk_counts['LOW'] / total_predictions) * 100,
            (risk_counts['MEDIUM'] / total_predictions) * 100,
            (risk_counts['HIGH'] / total_predictions) * 100,
            (risk_counts['CRITICAL'] / total_predictions) * 100
        ]
    else:
        risk_percentages = [25, 25, 25, 25]
    
    risk_chart = create_bar_chart(
        risk_percentages,
        ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        'Risk Level Distribution (30-Day Historical)',
        colors=['#00FF00', '#FFFF00', '#FF6600', '#FF0000']
    )
    st.plotly_chart(risk_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Statistics Table
    st.markdown("<h3>📋 Detailed Statistics</h3>", unsafe_allow_html=True)
    
    stats_table = pd.DataFrame({
        'Metric': [
            'Mean Soft X-ray Flux',
            'Std Dev Soft X-ray',
            'Min Soft X-ray',
            'Max Soft X-ray',
            'Mean Hard X-ray Counts',
            'Std Dev Hard X-ray',
            'Min Hard X-ray',
            'Max Hard X-ray',
            'Soft-Hard Correlation',
            'Total Data Points'
        ],
        'Value': [
            f"{solexs_mean:.3f} W/m²",
            f"{historical_data['soft_xray_flux'].std():.3f}",
            f"{historical_data['soft_xray_flux'].min():.3f}",
            f"{solexs_max:.3f}",
            f"{helios_mean:.1f} counts/sec",
            f"{historical_data['hard_xray_counts'].std():.1f}",
            f"{historical_data['hard_xray_counts'].min():.0f}",
            f"{helios_max:.0f}",
            f"{correlation:.3f}",
            f"{len(historical_data)}"
        ]
    })
    
    st.dataframe(stats_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("""
        <p style="color: #888; font-size: 12px; text-align: center;">
            Data Range: Last 30 Days | Update Frequency: Real-time
        </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_analytics()
