import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_data():
    API_KEY = "Zjla2_CQEEo5530tKuNIcpXCAkp6uv9p"
    TICKER = "SPY"
    MULTIPLIER = 1
    TIMESCALE = "minute"

    end = datetime.utcnow()
    start = end - timedelta(days=1)
    from_date = start.strftime("%Y-%m-%d")
    to_date = end.strftime("%Y-%m-%d")

    url = f"https://api.polygon.io/v2/aggs/ticker/{TICKER}/range/{MULTIPLIER}/{TIMESCALE}/{from_date}/{to_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 1000,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Polygon API error {response.status_code}: {response.text}")

    data = response.json().get("results", [])
    if not data:
        raise Exception("No data received from Polygon")

    df = pd.DataFrame(data)
    df["datetime"] = pd.to_datetime(df["t"], unit="ms")
    df = df[["datetime", "o", "h", "l", "c", "v"]]
    df.columns = ["datetime", "open", "high", "low", "close", "volume"]
    df["ticker"] = TICKER.lower()

    output_file = "data/SPY_1m.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Saved fresh Polygon data to {output_file} with {len(df)} rows.")

    return df

if __name__ == "__main__":
    fetch_data()