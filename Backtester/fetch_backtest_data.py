import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "Zjla2_CQEEo5530tKuNIcpXCAkp6uv9p"
TICKER = "SPY"
DAYS = 10

def fetch_backtest_data():
  end_date = datetime.now()
  start_date = end_date - timedelta(days=DAYS)

  url = f"https://api.polygon.io/v2/aggs/ticker/{TICKER}/range/1/minute/{start_date.date()}/{end_date.date()}?adjusted=true&sort=asc&limit=50000&apiKey={API_KEY}"
  response = requests.get(url)

  if response.status_code != 200:
    raise Exception(f"Polygon API error: {response.status_code}")

  data = response.json().get("results", [])

  if not data:
    raise Exception("No data received from Polygon")

  df = pd.DataFrame(data)
  df["datetime"] = pd.to_datetime(df["t"], unit="ms")
  df = df.rename(columns={
    "o": "open",
    "h": "high",
    "l": "low",
    "c": "close",
    "v": "volume"
  })

  df = df[["datetime", "open", "high", "low", "close", "volume"]]
  df["ticker"] = TICKER.lower()

  output_path = "data/SPY_1m_backtest.csv"
  df.to_csv(output_path, index=False)
  print(f"✅ Saved backtest data to {output_path} with {len(df)} rows.")

  return df

if __name__ == "__main__":
  fetch_backtest_data()