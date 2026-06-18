import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
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


def load_data():
    return pd.read_csv(DATA_FILE)


def preprocess(df):
    X = df.drop(columns=["target"])
    y = df["target"]

    # Encode categorical columns if any remain
    for col in X.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    return X, y


def train_model(X_train, y_train):

    pos_weight = len(y_train[y_train == 0]) / max(
        len(y_train[y_train == 1]),
        1
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=pos_weight,
        random_state=42,
        eval_metric="logloss",
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    print("\n=== Metrics ===")

    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds, zero_division=0)
    recall = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)
    roc_auc = roc_auc_score(y_test, probs)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
    }


def save_model(model):

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


def main():

    print(f"Loading data from {DATA_FILE}")

    df = load_data()

    X, y = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("Training XGBoost model...")

    model = train_model(
        X_train,
        y_train,
    )

    evaluate_model(
        model,
        X_test,
        y_test,
    )

    save_model(model)


if __name__ == "__main__":
    main()