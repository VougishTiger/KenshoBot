import yfinance as yf
import pandas as pd

def fetch_data():
  TICKER = "SPY"
  INTERVAL = "5m"
  PERIOD = "1d"

  data = yf.download(tickers=TICKER, interval=INTERVAL, period=PERIOD, progress=False)

  if isinstance(data, tuple):
    df = data[0]
  else:
    df = data

  if df is None or df.empty:
    print("❌ No data fetched.")
    return

  df.columns = [str(col).lower() for col in df.columns]
  df.reset_index(inplace=True)

  df.rename(columns={
    "datetime": "Datetime",
    "close": "close_spy",
    "open": "open_spy",
    "high": "high_spy",
    "low": "low_spy",
    "volume": "volume_spy"
  }, inplace=True)

  df.to_csv("data/SPY_5m.csv", index=False)
  print(f"✅ Saved fresh data to data/SPY_5m.csv with {len(df)} rows.")