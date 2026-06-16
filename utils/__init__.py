"""
Solar Sentinel AI - Utility Package
Provides data generation, prediction, and visualization utilities
"""

from .data_generator import SolarDataGenerator, generate_historical_data
from .prediction_engine import SolarFlarePredictor, make_prediction
from .visualizations import (
    create_timeseries_chart,
    create_gauge_chart,
    create_dual_axis_chart,
    create_bar_chart,
    create_heatmap,
    create_alert_card,
    create_histogram,
    create_scatter_plot,
    create_kpi_card
)

__version__ = "1.0.0"
__author__ = "ISRO Hackathon Team"
__description__ = "AI-Powered Solar Flare Forecasting Platform"

__all__ = [
    'SolarDataGenerator',
    'generate_historical_data',
    'SolarFlarePredictor',
    'make_prediction',
    'create_timeseries_chart',
    'create_gauge_chart',
    'create_dual_axis_chart',
    'create_bar_chart',
    'create_heatmap',
    'create_alert_card',
    'create_histogram',
    'create_scatter_plot',
    'create_kpi_card'
]
