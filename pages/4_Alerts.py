"""
Alert Center - Real-time Solar Flare Alerts and Notifications
Generates and displays alerts based on current predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_generator import SolarDataGenerator
from utils.prediction_engine import SolarFlarePredictor


def generate_alerts(prediction_15, prediction_60, prediction_360):
    """Generate alerts based on predictions"""
    alerts = []
    
    # 15-minute alerts (highest priority)
    if prediction_15['risk_level'] == 'CRITICAL':
        alerts.append({
            'level': 'RED',
            'severity': 'CRITICAL',
            'title': 'CRITICAL SOLAR FLARE ALERT',
            'message': f"X-class or strong M-class flare highly probable in next 15 minutes. Probability: {prediction_15['probability_percent']:.1f}%",
            'timestamp': datetime.now(),
            'icon': '🚨'
        })
    elif prediction_15['risk_level'] == 'HIGH':
        alerts.append({
            'level': 'ORANGE',
            'severity': 'WARNING',
            'title': 'HIGH FLARE RISK ALERT',
            'message': f"Significant flare activity expected within 15 minutes. Class {prediction_15['flare_class']}, Probability: {prediction_15['probability_percent']:.1f}%",
            'timestamp': datetime.now(),
            'icon': '⚠️'
        })
    elif prediction_15['risk_level'] == 'MEDIUM':
        alerts.append({
            'level': 'YELLOW',
            'severity': 'ADVISORY',
            'title': 'MODERATE FLARE ADVISORY',
            'message': f"Elevated solar activity detected. Class {prediction_15['flare_class']}, Probability: {prediction_15['probability_percent']:.1f}%",
            'timestamp': datetime.now(),
            'icon': '⚡'
        })
    
    # 60-minute alerts
    if prediction_60['risk_level'] == 'HIGH':
        alerts.append({
            'level': 'ORANGE',
            'severity': 'WARNING',
            'title': '1-HOUR FORECAST: HIGH RISK',
            'message': f"Elevated flare probability extends into 1-hour window. Class {prediction_60['flare_class']}, Probability: {prediction_60['probability_percent']:.1f}%",
            'timestamp': datetime.now(),
            'icon': '📢'
        })
    
    # 6-hour alerts
    if prediction_360['risk_level'] == 'CRITICAL':
        alerts.append({
            'level': 'RED',
            'severity': 'CRITICAL',
            'title': '6-HOUR FORECAST: CRITICAL RISK',
            'message': f"Critical flare activity possible over next 6 hours. Maintain heightened alert status.",
            'timestamp': datetime.now(),
            'icon': '🚨'
        })
    
    # If no significant alerts, add green status
    if not alerts:
        alerts.append({
            'level': 'GREEN',
            'severity': 'INFO',
            'title': 'NORMAL SOLAR ACTIVITY',
            'message': 'Solar activity within normal parameters. No immediate flare threats detected.',
            'timestamp': datetime.now(),
            'icon': '✅'
        })
    
    return alerts


def render_alerts():
    """Render the alert center page"""
    
    st.set_page_config(page_title="Solar Sentinel AI - Alert Center", layout="wide")
    
    st.markdown("""
        <style>
            body { background-color: #0a0e27; color: #ffffff; }
            .main { background-color: #0a0e27; }
            h1, h2, h3, h4, h5, h6 { color: #00FF00; font-weight: bold; }
            .alert-card {
                padding: 20px;
                border-radius: 10px;
                border-left: 6px solid;
                margin: 15px 0;
                font-weight: 500;
            }
            .alert-red {
                background-color: #3d0000;
                border-left-color: #FF0000;
            }
            .alert-orange {
                background-color: #3d2200;
                border-left-color: #FF6600;
            }
            .alert-yellow {
                background-color: #3d3d00;
                border-left-color: #FFFF00;
            }
            .alert-green {
                background-color: #003d00;
                border-left-color: #00FF00;
            }
            .alert-title { font-size: 18px; font-weight: bold; margin: 0 0 10px 0; }
            .alert-message { font-size: 14px; margin: 5px 0; }
            .alert-time { font-size: 12px; color: #888; margin-top: 10px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>🚨 ALERT CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Real-time Solar Flare Warnings & Notifications</p>", 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Generate current predictions
    gen = SolarDataGenerator()
    current_data = gen.get_latest_data(n_hours=1)
    
    solexs_values = current_data['soft_xray_flux'].values
    helios_values = current_data['hard_xray_counts'].values
    
    predictor = SolarFlarePredictor()
    prediction_15 = predictor.predict_flare(solexs_values, helios_values, 15)
    prediction_60 = predictor.predict_flare(solexs_values, helios_values, 60)
    prediction_360 = predictor.predict_flare(solexs_values, helios_values, 360)
    
    # Generate alerts
    alerts = generate_alerts(prediction_15, prediction_60, prediction_360)
    
    # Alert Summary
    st.markdown("<h2>⚡ Active Alerts</h2>", unsafe_allow_html=True)
    
    alert_count = {
        'RED': sum(1 for a in alerts if a['level'] == 'RED'),
        'ORANGE': sum(1 for a in alerts if a['level'] == 'ORANGE'),
        'YELLOW': sum(1 for a in alerts if a['level'] == 'YELLOW'),
        'GREEN': sum(1 for a in alerts if a['level'] == 'GREEN')
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style="background-color: #3d0000; padding: 15px; border-radius: 10px; 
                        border-left: 4px solid #FF0000; text-align: center;">
                <p style="color: #FF0000; font-size: 28px; margin: 0; font-weight: bold;">{alert_count['RED']}</p>
                <p style="color: #888; font-size: 12px; margin: 5px 0;">Critical Alerts</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background-color: #3d2200; padding: 15px; border-radius: 10px; 
                        border-left: 4px solid #FF6600; text-align: center;">
                <p style="color: #FF6600; font-size: 28px; margin: 0; font-weight: bold;">{alert_count['ORANGE']}</p>
                <p style="color: #888; font-size: 12px; margin: 5px 0;">Warning Alerts</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style="background-color: #3d3d00; padding: 15px; border-radius: 10px; 
                        border-left: 4px solid #FFFF00; text-align: center;">
                <p style="color: #FFFF00; font-size: 28px; margin: 0; font-weight: bold;">{alert_count['YELLOW']}</p>
                <p style="color: #888; font-size: 12px; margin: 5px 0;">Advisory Alerts</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style="background-color: #003d00; padding: 15px; border-radius: 10px; 
                        border-left: 4px solid #00FF00; text-align: center;">
                <p style="color: #00FF00; font-size: 28px; margin: 0; font-weight: bold;">{alert_count['GREEN']}</p>
                <p style="color: #888; font-size: 12px; margin: 5px 0;">Normal Status</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display alerts
    st.markdown("<h2>📋 Alert Messages</h2>", unsafe_allow_html=True)
    
    for alert in alerts:
        alert_class = f"alert-{alert['level'].lower()}"
        color = {
            'RED': '#FF0000',
            'ORANGE': '#FF6600',
            'YELLOW': '#FFFF00',
            'GREEN': '#00FF00'
        }[alert['level']]
        
        st.markdown(f"""
            <div class="alert-card {alert_class}">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 32px;">{alert['icon']}</span>
                    <div style="flex: 1;">
                        <p class="alert-title" style="color: {color};">
                            {alert['title']}
                        </p>
                        <p class="alert-message">
                            {alert['message']}
                        </p>
                        <p class="alert-time">
                            {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Alert History
    st.markdown("<h2>📜 Alert History</h2>", unsafe_allow_html=True)
    
    history_data = []
    for i, alert in enumerate(alerts):
        history_data.append({
            'Level': alert['level'],
            'Title': alert['title'],
            'Severity': alert['severity'],
            'Time': alert['timestamp'].strftime('%H:%M:%S')
        })
    
    if history_data:
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No alerts in history")
    
    st.markdown("---")
    
    # Alert Thresholds
    st.markdown("<h2>⚙️ Alert Configuration</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color: #1a1f3a; padding: 20px; border-radius: 10px;">
            <h4 style="color: #00FF00; margin-top: 0;">Alert Thresholds</h4>
            <table style="width: 100%; color: #FFFFFF;">
                <tr style="border-bottom: 1px solid #333;">
                    <td style="padding: 10px;"><b>CRITICAL (RED)</b></td>
                    <td style="padding: 10px;">Risk Level = CRITICAL or Probability > 80%</td>
                </tr>
                <tr style="border-bottom: 1px solid #333;">
                    <td style="padding: 10px;"><b>WARNING (ORANGE)</b></td>
                    <td style="padding: 10px;">Risk Level = HIGH or Probability > 60%</td>
                </tr>
                <tr style="border-bottom: 1px solid #333;">
                    <td style="padding: 10px;"><b>ADVISORY (YELLOW)</b></td>
                    <td style="padding: 10px;">Risk Level = MEDIUM or Probability > 40%</td>
                </tr>
                <tr>
                    <td style="padding: 10px;"><b>NORMAL (GREEN)</b></td>
                    <td style="padding: 10px;">Risk Level = LOW and Probability < 40%</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("<h2>💡 Operational Recommendations</h2>", unsafe_allow_html=True)
    
    max_risk = alerts[0]['level'] if alerts else 'GREEN'
    
    if max_risk == 'RED':
        st.error("""
        🚨 **CRITICAL ALERT STATUS**
        - Activate emergency protocols
        - Increase monitoring frequency to 1-minute intervals
        - Alert all personnel
        - Prepare contingency systems
        """)
    elif max_risk == 'ORANGE':
        st.warning("""
        ⚠️ **HIGH ALERT STATUS**
        - Increase monitoring frequency to 5-minute intervals
        - Brief operations team
        - Have contingency systems ready
        """)
    elif max_risk == 'YELLOW':
        st.info("""
        ⚡ **ADVISORY STATUS**
        - Maintain normal monitoring schedule
        - Keep systems ready
        - Prepare for escalation
        """)
    else:
        st.success("""
        ✅ **NORMAL STATUS**
        - Continue routine monitoring
        - No immediate threats detected
        - Systems operating normally
        """)
    
    st.markdown("---")
    st.markdown("""
        <p style="color: #888; font-size: 12px; text-align: center;">
            Last Update: Now | Auto-refresh: Enabled (60s intervals)
        </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_alerts()
