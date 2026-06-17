import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from xgboost import XGBClassifier


DATA_FILE = Path("data/processed/training_data.csv")
MODEL_FILE = Path("models/flare_model.pkl")


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

    print(
        "Accuracy:",
        accuracy_score(y_test, preds),
    )

    print(
        "Precision:",
        precision_score(y_test, preds),
    )

    print(
        "Recall:",
        recall_score(y_test, preds),
    )

    print(
        "F1:",
        f1_score(y_test, preds),
    )

    print(
        "ROC-AUC:",
        roc_auc_score(y_test, probs),
    )

    MODEL_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_FILE,
    )

    print(
        f"\nModel saved -> {MODEL_FILE}"
    )


if __name__ == "__main__":
    train()