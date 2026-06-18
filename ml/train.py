import json
from pathlib import Path

import joblib
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


DATA_FILE = Path("data/processed/training_data.csv")
MODEL_FILE = Path("models/flare_model.pkl")
CONFUSION_MATRIX_FILE = Path("models/confusion_matrix.png")
FEATURE_IMPORTANCE_FILE = Path("models/feature_importance.png")
THRESHOLD_FILE = Path("models/decision_threshold.json")

PARAM_GRID = [
    {
        "n_estimators": 150,
        "max_depth": 3,
        "learning_rate": 0.05,
        "min_child_weight": 3,
        "subsample": 0.9,
        "colsample_bytree": 0.9,
        "reg_lambda": 3.0,
    },
    {
        "n_estimators": 200,
        "max_depth": 3,
        "learning_rate": 0.03,
        "min_child_weight": 3,
        "subsample": 0.9,
        "colsample_bytree": 0.9,
        "reg_lambda": 5.0,
    },
    {
        "n_estimators": 200,
        "max_depth": 4,
        "learning_rate": 0.05,
        "min_child_weight": 5,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_lambda": 3.0,
    },
    {
        "n_estimators": 250,
        "max_depth": 4,
        "learning_rate": 0.03,
        "min_child_weight": 5,
        "subsample": 0.8,
        "colsample_bytree": 0.9,
        "reg_lambda": 5.0,
    },
    {
        "n_estimators": 150,
        "max_depth": 5,
        "learning_rate": 0.05,
        "min_child_weight": 3,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_lambda": 5.0,
    },
]


def best_threshold_for_f1(y_true, probabilities):
    precisions, recalls, thresholds = precision_recall_curve(
        y_true,
        probabilities,
    )

    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-12)
    best_index = f1_scores[:-1].argmax()

    return float(thresholds[best_index]), float(f1_scores[best_index])


def train():
    df = pd.read_csv(DATA_FILE)

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train,
        y_train,
        test_size=0.25,
        random_state=42,
        stratify=y_train,
    )

    pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

    best_model = None
    best_params = None
    best_threshold = 0.5
    best_val_f1 = -1.0

    for params in PARAM_GRID:
        model = XGBClassifier(
            **params,
            scale_pos_weight=pos_weight,
            random_state=42,
            eval_metric="logloss",
            n_jobs=1,
        )

        model.fit(X_train, y_train)

        val_probs = model.predict_proba(X_val)[:, 1]
        threshold, val_f1 = best_threshold_for_f1(y_val, val_probs)

        if val_f1 > best_val_f1:
            best_model = model
            best_params = params
            best_threshold = threshold
            best_val_f1 = val_f1

    model = best_model

    probs = model.predict_proba(X_test)[:, 1]
    preds = (probs >= best_threshold).astype(int)

    print("\n=== Metrics ===")
    print("Best Validation F1:", best_val_f1)
    print("Decision Threshold:", best_threshold)
    print("Best Parameters:", best_params)
    print("Accuracy:", accuracy_score(y_test, preds))
    print("Precision:", precision_score(y_test, preds))
    print("Recall:", recall_score(y_test, preds))
    print("F1:", f1_score(y_test, preds))
    print("ROC-AUC:", roc_auc_score(y_test, probs))

    print("\n=== Confusion Matrix ===")
    print(
        pd.DataFrame(
            confusion_matrix(y_test, preds),
            index=["Actual 0", "Actual 1"],
            columns=["Predicted 0", "Predicted 1"],
        )
    )

    print("\n=== Classification Report ===")
    print(classification_report(y_test, preds))

    MODEL_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        preds,
        display_labels=["No flare", "Flare"],
        cmap="Blues",
    )
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_FILE, dpi=300)
    plt.close()

    feature_importance = pd.Series(
        model.feature_importances_,
        index=X.columns,
    ).sort_values(ascending=False)

    feature_importance.head(20).sort_values().plot(kind="barh")
    plt.title("Feature Importance")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_FILE, dpi=300)
    plt.close()

    joblib.dump(
        model,
        MODEL_FILE,
    )

    with open(THRESHOLD_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"decision_threshold": best_threshold},
            f,
            indent=2,
        )

    print(f"\nModel saved -> {MODEL_FILE}")
    print(f"Decision threshold saved -> {THRESHOLD_FILE}")
    print(f"Confusion matrix plot saved -> {CONFUSION_MATRIX_FILE}")
    print(f"Feature importance plot saved -> {FEATURE_IMPORTANCE_FILE}")


if __name__ == "__main__":
    train()