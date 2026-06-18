from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
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

    pos_weight = len(y[y == 0]) / len(y[y == 1])

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=pos_weight,
        random_state=42,
        eval_metric="logloss",
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    print("\n=== Metrics ===")
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

    print(f"\nModel saved -> {MODEL_FILE}")
    print(f"Confusion matrix plot saved -> {CONFUSION_MATRIX_FILE}")
    print(f"Feature importance plot saved -> {FEATURE_IMPORTANCE_FILE}")


if __name__ == "__main__":
    train()