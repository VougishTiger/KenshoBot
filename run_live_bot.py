import time
import pandas as pd
from fetch_data import fetch_data
from indicators import add_all_indicators
from signal_engine import detect_signals

while True:
    fetch_data()

    df = pd.read_csv("data/SPY_5m.csv")

    df.rename(columns={
    "Datetime": "datetime",
    "('open', 'spy')": "open",
    "('high', 'spy')": "high",
    "('low', 'spy')": "low",
    "('close', 'spy')": "close",
    "('volume', 'spy')": "volume"
    }, inplace=True)

    df["datetime"] = pd.to_datetime(df["datetime"])

    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=numeric_cols, inplace=True)

    df = add_all_indicators(df)

    df.to_csv("data/SPY_5m_with_indicators.csv", index=False)

    signals_df, confirmed_signals_df = detect_signals(df)

    if not confirmed_signals_df.empty:
        print("✅ Confirmed Signal(s) Found:")
        print(confirmed_signals_df.tail())
        confirmed_signals_df.to_csv("data/confirmed_signals.csv", index=False)
    else:
        print("⏳ No confirmed signals at this time.")

    time.sleep(300)