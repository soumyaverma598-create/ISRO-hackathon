"""
Mock Solar Flare Prediction Engine
Uses simulated SoLEXS and HELIOS data to generate realistic predictions
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class SolarFlarePredictor:
    """Mock prediction engine that generates realistic flare forecasts"""
    
    # Flare classification (GOES Scale)
    FLARE_CLASSES = ['A', 'B', 'C', 'M', 'X']
    
    # Risk levels
    RISK_LEVELS = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    # Color mapping
    RISK_COLORS = {
        'LOW': '#00FF00',
        'MEDIUM': '#FFFF00',
        'HIGH': '#FF6600',
        'CRITICAL': '#FF0000'
    }
    
    ALERT_COLORS = {
        'GREEN': '#00FF00',
        'YELLOW': '#FFFF00',
        'ORANGE': '#FF6600',
        'RED': '#FF0000'
    }
    
    def __init__(self, seed=42):
        np.random.seed(seed)
    
    def calculate_features(self, solexs_data: np.ndarray, helios_data: np.ndarray) -> Dict[str, float]:
        """
        Calculate features from SoLEXS and HELIOS data
        
        Args:
            solexs_data: Array of soft X-ray flux values
            helios_data: Array of hard X-ray count rates
            
        Returns:
            Dictionary of calculated features
        """
        features = {}
        
        # SoLEXS features
        features['soft_xray_flux'] = float(solexs_data[-1]) if len(solexs_data) > 0 else 1.0
        features['soft_xray_trend'] = float(np.nanmean(np.diff(solexs_data[-10:]))) if len(solexs_data) > 1 else 0.0
        features['soft_xray_volatility'] = float(np.nanstd(solexs_data[-30:]) if len(solexs_data) > 30 else np.nanstd(solexs_data)) if len(solexs_data) > 0 else 0.0
        
        # HELIOS features
        features['hard_xray_counts'] = float(helios_data[-1]) if len(helios_data) > 0 else 50.0
        features['hard_xray_trend'] = float(np.nanmean(np.diff(helios_data[-10:]))) if len(helios_data) > 1 else 0.0
        features['hard_xray_spike'] = float(np.nanmax(helios_data[-20:]) - np.nanmin(helios_data[-20:])) if len(helios_data) > 20 else 0.0
        
        # Derived features
        features['flux_to_counts_ratio'] = features['soft_xray_flux'] / (features['hard_xray_counts'] + 1)
        features['activity_index'] = (features['soft_xray_flux'] + features['hard_xray_counts'] / 100) / 2
        
        # Sanitize: Replace any NaN with defaults
        for key in features:
            if np.isnan(features[key]):
                features[key] = 0.0
        
        return features
    
    def predict_flare_probability(self, features: Dict[str, float]) -> float:
        """
        Calculate flare probability based on features
        
        Args:
            features: Dictionary of calculated features
            
        Returns:
            Probability between 0 and 1
        """
        # Simple weighted combination of features
        soft_xray_contribution = min(features['soft_xray_flux'] / 10, 1.0) * 0.35
        hard_xray_contribution = min(features['hard_xray_counts'] / 500, 1.0) * 0.35
        trend_contribution = min(abs(features['soft_xray_trend']) + abs(features['hard_xray_trend']), 1.0) * 0.20
        volatility_contribution = min(features['soft_xray_volatility'] / 5, 1.0) * 0.10
        
        probability = (soft_xray_contribution + hard_xray_contribution + 
                      trend_contribution + volatility_contribution)
        
        # Add random variation for realism
        probability += np.random.normal(0, 0.05)
        probability = np.clip(probability, 0, 1)
        
        # Ensure probability is not NaN
        if np.isnan(probability):
            probability = 0.3  # Default to moderate probability if NaN
        
        return float(probability)
    
    def classify_flare(self, probability: float, hard_xray_counts: float) -> str:
        """
        Classify flare based on probability and activity level
        
        Args:
            probability: Flare probability (0-1)
            hard_xray_counts: Hard X-ray count rate
            
        Returns:
            Flare class (A, B, C, M, X)
        """
        if probability < 0.2:
            return 'A'
        elif probability < 0.4:
            return 'B' if hard_xray_counts < 150 else 'C'
        elif probability < 0.6:
            return 'C' if hard_xray_counts < 250 else 'M'
        elif probability < 0.8:
            return 'M' if hard_xray_counts < 400 else 'X'
        else:
            return 'X'
    
    def calculate_risk_level(self, probability: float, flare_class: str) -> str:
        """
        Determine risk level based on probability and flare class
        
        Args:
            probability: Flare probability (0-1)
            flare_class: Flare classification
            
        Returns:
            Risk level (LOW, MEDIUM, HIGH, CRITICAL)
        """
        class_weights = {'A': 0, 'B': 0.2, 'C': 0.4, 'M': 0.7, 'X': 1.0}
        combined_score = (probability * 0.6 + class_weights[flare_class] * 0.4)
        
        if combined_score < 0.25:
            return 'LOW'
        elif combined_score < 0.5:
            return 'MEDIUM'
        elif combined_score < 0.75:
            return 'HIGH'
        else:
            return 'CRITICAL'
    
    def predict_flare(self, solexs_data: np.ndarray, helios_data: np.ndarray,
                     horizon_minutes: int = 15) -> Dict:
        """
        Main prediction function
        
        Args:
            solexs_data: Soft X-ray flux array
            helios_data: Hard X-ray count rate array
            horizon_minutes: Prediction horizon (15, 60, 360)
            
        Returns:
            Dictionary with prediction results
        """
        # Calculate features
        features = self.calculate_features(solexs_data, helios_data)
        
        # Apply horizon-specific adjustments
        horizon_factor = 1.0 + (horizon_minutes / 360)  # Uncertainty increases with horizon
        probability = self.predict_flare_probability(features) * horizon_factor
        probability = np.clip(probability, 0, 1)
        
        # Classify flare
        flare_class = self.classify_flare(probability, features['hard_xray_counts'])
        
        # Calculate risk
        risk_level = self.calculate_risk_level(probability, flare_class)
        
        # Generate explanation
        explanation = self._generate_explanation(features, probability, flare_class)
        
        return {
            'timestamp': datetime.now(),
            'probability': probability,
            'probability_percent': round(probability * 100, 1),
            'flare_class': flare_class,
            'risk_level': risk_level,
            'horizon_minutes': horizon_minutes,
            'features': features,
            'explanation': explanation,
            'confidence': self._calculate_confidence(probability, flare_class)
        }
    
    def _generate_explanation(self, features: Dict[str, float], 
                             probability: float, flare_class: str) -> str:
        """Generate human-readable explanation for prediction"""
        
        explanations = []
        
        if features['soft_xray_flux'] > 5:
            explanations.append(f"Elevated soft X-ray flux ({features['soft_xray_flux']:.2f} W/m²)")
        
        if features['hard_xray_counts'] > 200:
            explanations.append(f"High hard X-ray activity ({features['hard_xray_counts']:.0f} counts/sec)")
        
        if features['soft_xray_trend'] > 0.1:
            explanations.append("Rapid increase in soft X-ray emissions")
        
        if features['hard_xray_spike'] > 100:
            explanations.append("Notable hard X-ray spike detected")
        
        if features['soft_xray_volatility'] > 1.0:
            explanations.append("Increased solar atmosphere volatility")
        
        if not explanations:
            explanations.append("Baseline solar activity detected")
        
        return "; ".join(explanations)
    
    def _calculate_confidence(self, probability: float, flare_class: str) -> float:
        """Calculate confidence score for prediction"""
        # Confidence is higher for extreme probabilities
        confidence = 0.7 + abs(probability - 0.5) * 0.6
        return np.clip(confidence, 0.6, 0.95)
    
    def generate_feature_contributions(self, features: Dict[str, float]) -> List[Tuple[str, float]]:
        """
        Generate feature importance for explainability
        
        Returns:
            List of (feature_name, contribution_percent)
        """
        contributions = [
            ('Soft X-ray Trend', min(abs(features['soft_xray_trend']) * 20, 50)),
            ('Hard X-ray Spike', min(features['hard_xray_spike'] / 5, 40)),
            ('Soft X-ray Volatility', min(features['soft_xray_volatility'] * 8, 35)),
            ('Background Activity', min(features['activity_index'] * 10, 25)),
        ]
        
        # Normalize to sum to 100
        total = sum(c[1] for c in contributions)
        if total > 0:
            contributions = [(name, (value / total) * 100) for name, value in contributions]
        
        return sorted(contributions, key=lambda x: x[1], reverse=True)


def make_prediction(solexs_data: np.ndarray, helios_data: np.ndarray, 
                   horizon_minutes: int = 15) -> Dict:
    """
    Convenience function to make a prediction
    
    Args:
        solexs_data: Soft X-ray flux array
        helios_data: Hard X-ray count rate array
        horizon_minutes: Prediction horizon
        
    Returns:
        Prediction dictionary
    """
    predictor = SolarFlarePredictor()
    return predictor.predict_flare(solexs_data, helios_data, horizon_minutes)
