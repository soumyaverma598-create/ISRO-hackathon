"""
Real ML Predictor for Solar Sentinel AI

Loads trained XGBoost model and exposes:
- load_model()
- predict_flare()
- predict_probability()

Compatible with existing dashboard integration.
"""

from pathlib import Path
import pickle
import numpy as np
import pandas as pd


MODEL_PATH = Path("models/flare_model.pkl")


class SolarFlarePredictor:
    """
    Drop-in replacement for the current mock predictor.

    The dashboard can keep importing:
        SolarFlarePredictor()

    while the backend becomes ML-powered.
    """

    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        """
        Load trained model from disk.
        """
        if not MODEL_PATH.exists():
            return None

        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        return model

    def _build_feature_vector(
        self,
        solexs_data: np.ndarray,
        helios_data: np.ndarray,
    ):
        """
        Convert telemetry arrays into ML features.

        Must match training pipeline features.
        """

        solexs = np.asarray(solexs_data, dtype=float)
        helios = np.asarray(helios_data, dtype=float)

        features = {
            "soft_flux_mean": np.mean(solexs),
            "soft_flux_std": np.std(solexs),
            "soft_flux_max": np.max(solexs),
            "soft_flux_min": np.min(solexs),
            "soft_flux_last": solexs[-1],

            "hard_flux_mean": np.mean(helios),
            "hard_flux_std": np.std(helios),
            "hard_flux_max": np.max(helios),
            "hard_flux_min": np.min(helios),
            "hard_flux_last": helios[-1],

            "soft_trend":
                np.polyfit(np.arange(len(solexs)), solexs, 1)[0],

            "hard_trend":
                np.polyfit(np.arange(len(helios)), helios, 1)[0],
        }

        return pd.DataFrame([features])

    def predict_probability(
        self,
        solexs_data,
        helios_data,
    ):
        """
        Returns probability of significant flare.
        """

        if self.model is None:
            return 0.50

        X = self._build_feature_vector(
            solexs_data,
            helios_data,
        )

        probability = self.model.predict_proba(X)[0][1]

        return float(probability)

    def predict_flare(
        self,
        solexs_data,
        helios_data,
    ):
        """
        Binary prediction.
        """

        probability = self.predict_probability(
            solexs_data,
            helios_data,
        )

        return int(probability >= 0.5)

    def classify_flare(
        self,
        probability: float,
        hard_xray_counts: float = 0,
    ):
        """
        Convert probability to GOES-like label.
        """

        if probability < 0.25:
            return "A"

        if probability < 0.50:
            return "C"

        if probability < 0.75:
            return "M"

        return "X"

    def get_risk_level(self, probability):
        if probability < 0.25:
            return "LOW"

        if probability < 0.50:
            return "MEDIUM"

        if probability < 0.75:
            return "HIGH"

        return "CRITICAL"


def load_model():
    predictor = SolarFlarePredictor()
    return predictor.model


def predict_probability(solexs_data, helios_data):
    predictor = SolarFlarePredictor()
    return predictor.predict_probability(
        solexs_data,
        helios_data,
    )


def predict_flare(solexs_data, helios_data):
    predictor = SolarFlarePredictor()
    return predictor.predict_flare(
        solexs_data,
        helios_data,
    )