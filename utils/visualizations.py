"""
Visualization utilities for Solar Sentinel AI
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_kpi_card(label: str, value: str, unit: str = "", color: str = "#00FF00") -> go.Figure:
    """Create a KPI indicator card"""
    
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value if isinstance(value, (int, float)) else 0,
        title={"text": label, "font": {"size": 16, "color": "#FFFFFF"}},
        number={"font": {"size": 32, "color": color}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=14, color="#FFFFFF"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=150
    )
    
    return fig


def create_gauge_chart(value: float, label: str, color: str = "#00FF00") -> go.Figure:
    """Create a gauge chart for probability or risk"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': label, 'font': {'size': 18, 'color': '#FFFFFF'}},
        delta={'reference': 50, 'increasing': {'color': 'red'}},
        gauge={
            'axis': {'range': [0, 100], 'tickfont': {'color': '#FFFFFF'}},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 25], 'color': '#00FF00'},
                {'range': [25, 50], 'color': '#FFFF00'},
                {'range': [50, 75], 'color': '#FF6600'},
                {'range': [75, 100], 'color': '#FF0000'}
            ],
            'threshold': {
                'line': {'color': '#FFFFFF', 'width': 2},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=12, color="#FFFFFF"),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_timeseries_chart(df: pd.DataFrame, x_col: str, y_col: str, 
                            title: str, y_label: str, color: str = "#00FF00") -> go.Figure:
    """Create a time series line chart"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines',
        name=y_label,
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=color.replace('FF', '44'),  # Semi-transparent
        hovertemplate='<b>%{x}</b><br>' + y_label + ': %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="#FFFFFF")),
        xaxis=dict(
            title='Time',
            showgrid=True,
            gridwidth=1,
            gridcolor='#1f2937',
            color='#FFFFFF'
        ),
        yaxis=dict(
            title=y_label,
            showgrid=True,
            gridwidth=1,
            gridcolor='#1f2937',
            color='#FFFFFF'
        ),
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=12, color="#FFFFFF"),
        height=400,
        hovermode='x unified',
        margin=dict(l=60, r=20, t=50, b=50)
    )
    
    return fig


def create_dual_axis_chart(df: pd.DataFrame, x_col: str, y1_col: str, y2_col: str,
                           title: str, y1_label: str, y2_label: str,
                           color1: str = "#00FF00", color2: str = "#FF6600") -> go.Figure:
    """Create a dual-axis time series chart"""
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=df[x_col], y=df[y1_col], name=y1_label,
                   line=dict(color=color1, width=2),
                   hovertemplate='<b>%{x}</b><br>' + y1_label + ': %{y:.2f}<extra></extra>'),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=df[x_col], y=df[y2_col], name=y2_label,
                   line=dict(color=color2, width=2),
                   hovertemplate='<b>%{x}</b><br>' + y2_label + ': %{y:.2f}<extra></extra>'),
        secondary_y=True
    )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="#FFFFFF")),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#1f2937',
            color='#FFFFFF'
        ),
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=12, color="#FFFFFF"),
        height=400,
        hovermode='x unified',
        margin=dict(l=60, r=60, t=50, b=50)
    )
    
    fig.update_yaxes(title_text=y1_label, secondary_y=False,
                     title_font=dict(color=color1), tickfont=dict(color=color1))
    fig.update_yaxes(title_text=y2_label, secondary_y=True,
                     title_font=dict(color=color2), tickfont=dict(color=color2))
    
    return fig


def create_bar_chart(data: list, labels: list, title: str, 
                     colors: list = None, orientation: str = 'v') -> go.Figure:
    """Create a bar chart"""
    
    if colors is None:
        colors = ['#00FF00'] * len(data)
    
    fig = go.Figure(go.Bar(
        x=labels if orientation == 'v' else data,
        y=data if orientation == 'v' else labels,
        orientation=orientation,
        marker=dict(color=colors),
        text=[f'{v:.1f}%' for v in data],
        textposition='auto',
        hovertemplate='<b>%{x if orientation == "v" else "%{y}"}</b><br>' +
                      'Value: %{y if orientation == "v" else "%{x}":.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#FFFFFF")),
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=12, color="#FFFFFF"),
        showlegend=False,
        height=300,
        xaxis=dict(showgrid=False, color='#FFFFFF'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#1f2937', color='#FFFFFF'),
        margin=dict(l=60, r=20, t=50, b=50)
    )
    
    return fig


def create_heatmap(data: np.ndarray, x_labels: list, y_labels: list, 
                   title: str, colorscale: str = 'RdYlGn') -> go.Figure:
    """Create a heatmap visualization"""
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=x_labels,
        y=y_labels,
        colorscale=colorscale,
        hovertemplate='<b>%{y}</b><br>%{x}<br>Value: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#FFFFFF")),
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=11, color="#FFFFFF"),
        height=400,
        xaxis=dict(color='#FFFFFF'),
        yaxis=dict(color='#FFFFFF'),
        coloraxis=dict(colorbar=dict(tickfont=dict(color='#FFFFFF'))),
        margin=dict(l=100, r=20, t=50, b=80)
    )
    
    return fig


def create_alert_card(message: str, severity: str, timestamp: str, 
                      alert_level: str = "YELLOW") -> dict:
    """Create alert card data structure"""
    
    colors = {
        'GREEN': '#00FF00',
        'YELLOW': '#FFFF00',
        'ORANGE': '#FF6600',
        'RED': '#FF0000'
    }
    
    severity_levels = {
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'CRITICAL': '🚨'
    }
    
    return {
        'message': message,
        'severity': severity,
        'timestamp': timestamp,
        'alert_level': alert_level,
        'color': colors.get(alert_level, '#FFFF00'),
        'icon': severity_levels.get(severity, 'ℹ️')
    }


def create_histogram(data: list, title: str, x_label: str,
                    nbins: int = 30, color: str = "#00FF00") -> go.Figure:
    """Create a histogram"""
    
    fig = go.Figure(data=[
        go.Histogram(
            x=data,
            nbinsx=nbins,
            marker=dict(color=color),
            hovertemplate='<b>%{x:.2f}</b><br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#FFFFFF")),
        xaxis_title=x_label,
        yaxis_title="Frequency",
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=12, color="#FFFFFF"),
        height=350,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#1f2937', color='#FFFFFF'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#1f2937', color='#FFFFFF'),
        margin=dict(l=60, r=20, t=50, b=50)
    )
    
    return fig


def create_scatter_plot(x_data: list, y_data: list, title: str, 
                       x_label: str, y_label: str, color: str = "#00FF00") -> go.Figure:
    """Create a scatter plot"""
    
    fig = go.Figure(data=[
        go.Scatter(
            x=x_data,
            y=y_data,
            mode='markers',
            marker=dict(color=color, size=8, opacity=0.7),
            hovertemplate='<b>%{x:.2f}</b><br>%{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#FFFFFF")),
        xaxis_title=x_label,
        yaxis_title=y_label,
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        font=dict(family="Arial", size=12, color="#FFFFFF"),
        height=350,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#1f2937', color='#FFFFFF'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#1f2937', color='#FFFFFF'),
        margin=dict(l=60, r=20, t=50, b=50)
    )
    
    return fig
