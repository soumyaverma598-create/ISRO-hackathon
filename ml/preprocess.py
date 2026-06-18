import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/data.csv")
OUTPUT_FILE = Path("data/processed/training_data.csv")


def preprocess():

    df = pd.read_csv(RAW_FILE)

    # Clean column names
    df.columns = [c.strip() for c in df.columns]

    # Target:
    # 1 = Moderate OR Severe flare present
    # 0 = No Moderate/Severe flare
    df["target"] = (
        (df["moderate flares"] > 0) |
        (df["severe flares"] > 0)
    ).astype(int)

    # Remove label columns from features
    X = df.drop(
        columns=[
            "common flares",
            "moderate flares",
            "severe flares"
        ]
    )

    # One-hot encode categorical features
    X = pd.get_dummies(
        X,
        drop_first=True
    )

    # Add target back
    X["target"] = df["target"]

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    X.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Saved processed dataset -> {OUTPUT_FILE}")
    print(f"Shape: {X.shape}")

    print("\nTarget Distribution:")
    print(X["target"].value_counts())

    positive_rate = (
        X["target"].sum() /
        len(X)
    ) * 100

    print(
        f"\nPositive Class Percentage: "
        f"{positive_rate:.2f}%"
    )


if __name__ == "__main__":
    preprocess()