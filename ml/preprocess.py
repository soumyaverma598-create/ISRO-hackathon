import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/data.csv")
OUTPUT_FILE = Path("data/processed/training_data.csv")


def preprocess():
    df = pd.read_csv(RAW_FILE)

    df.columns = [c.strip() for c in df.columns]

    # Binary target
    df["target"] = (df["severe flares"] > 0).astype(int)

    X = df.drop(
        columns=[
            "common flares",
            "moderate flares",
            "severe flares"
        ]
    )

    X = pd.get_dummies(X)

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


if __name__ == "__main__":
    preprocess()