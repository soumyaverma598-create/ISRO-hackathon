import pandas as pd
import requests
from pathlib import Path

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_noaa_flare_data():
    """
    Downloads NOAA solar flare event data.
    """

    url = (
        "https://services.swpc.noaa.gov/json/goes/"
        "primary/xray-flares-latest.json"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)

    output_file = RAW_DIR / "flare_events.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved flare data -> {output_file}")

    return output_file


if __name__ == "__main__":
    download_noaa_flare_data()