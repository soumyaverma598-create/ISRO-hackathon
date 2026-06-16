"""
Solar Flare Data Generator - Simulates SoLEXS and HELIOS data
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random


class SolarDataGenerator:
    """Generate realistic simulated solar data from SoLEXS and HELIOS instruments"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
    def generate_solexs_data(self, hours=24, frequency='1min'):
        """
        Generate simulated SoLEXS (Soft X-ray) data
        SoLEXS measures soft X-ray emissions from 1-12 Angstroms
        """
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=hours),
            end=datetime.now(),
            freq=frequency
        )
        
        n_points = len(timestamps)
        
        # Base quiet-time flux (1-2 W/m²)
        base_flux = np.ones(n_points) * np.random.uniform(1.0, 2.0)
        
        # Add realistic noise
        noise = np.random.normal(0, 0.1, n_points)
        
        # Add some gradual trends
        trend = np.linspace(0, np.random.uniform(-0.5, 0.5), n_points)
        
        # Add occasional flare-like events (increase in flux)
        flare_events = np.zeros(n_points)
        num_events = np.random.randint(2, 5)
        buffer = max(10, int(n_points * 0.1))  # 10% of data or minimum 10 points
        if n_points > buffer * 2:  # Only add events if we have enough data
            for _ in range(num_events):
                event_position = np.random.randint(buffer, n_points - buffer)
                event_width = np.random.randint(5, max(6, int(n_points * 0.15)))
                event_magnitude = np.random.uniform(2, 8)
                event_shape = np.exp(-((np.arange(n_points) - event_position) ** 2) / (2 * event_width ** 2))
                flare_events += event_magnitude * event_shape
        
        flux = base_flux + noise + trend + flare_events
        flux = np.maximum(flux, 0.1)  # Ensure no negative values
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'soft_xray_flux': flux,
            'soft_xray_flux_units': 'W/m²'
        })
    
    def generate_helios_data(self, hours=24, frequency='1min'):
        """
        Generate simulated HELIOS (Hard X-ray) data
        HELIOS measures hard X-ray emissions from 4-25 keV
        """
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=hours),
            end=datetime.now(),
            freq=frequency
        )
        
        n_points = len(timestamps)
        
        # Base quiet-time counts (50-100 counts/sec)
        base_counts = np.ones(n_points) * np.random.uniform(50, 100)
        
        # Add realistic noise
        noise = np.random.normal(0, 5, n_points)
        
        # Add gradual trends
        trend = np.linspace(0, np.random.uniform(-20, 20), n_points)
        
        # Add occasional flare-like events with sharper peaks
        flare_events = np.zeros(n_points)
        num_events = np.random.randint(2, 4)
        buffer = max(10, int(n_points * 0.1))  # 10% of data or minimum 10 points
        if n_points > buffer * 2:  # Only add events if we have enough data
            for _ in range(num_events):
                event_position = np.random.randint(buffer, n_points - buffer)
                event_width = np.random.randint(5, max(6, int(n_points * 0.1)))
                event_magnitude = np.random.uniform(100, 500)
                event_shape = np.exp(-((np.arange(n_points) - event_position) ** 2) / (2 * event_width ** 2))
                flare_events += event_magnitude * event_shape
        
        counts = base_counts + noise + trend + flare_events
        counts = np.maximum(counts, 10)  # Ensure minimum counts
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'hard_xray_counts': counts,
            'hard_xray_counts_units': 'counts/sec'
        })
    
    def generate_combined_data(self, hours=24):
        """Generate combined SoLEXS and HELIOS data"""
        solexs = self.generate_solexs_data(hours=hours)
        helios = self.generate_helios_data(hours=hours)
        
        combined = pd.merge(solexs, helios, on='timestamp')
        combined = combined.sort_values('timestamp').reset_index(drop=True)
        
        return combined
    
    def get_latest_data(self, n_hours=1):
        """Get latest simulated data for dashboard"""
        return self.generate_combined_data(hours=n_hours)


def generate_historical_data(days=30):
    """Generate historical data for analytics"""
    gen = SolarDataGenerator()
    
    all_data = []
    for day in range(days):
        data = gen.generate_combined_data(hours=24)
        data['timestamp'] = data['timestamp'] - timedelta(days=days - day - 1)
        all_data.append(data)
    
    return pd.concat(all_data, ignore_index=True).sort_values('timestamp')
