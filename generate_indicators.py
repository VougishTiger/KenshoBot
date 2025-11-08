import pandas as pd
from indicators import add_all_indicators

df = pd.read_csv("data/SPY_5m.csv")

df.rename(columns={
    "Datetime": "datetime",
    "close_spy": "close",
    "open_spy": "open",
    "high_spy": "high",
    "low_spy": "low",
    "volume_spy": "volume"
}, inplace=True)

df["datetime"] = pd.to_datetime(df["datetime"])

numeric_cols = ['open', 'high', 'low', 'close', 'volume']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
df.dropna(subset=numeric_cols, inplace=True)

df = add_all_indicators(df)
df.to_csv("data/SPY_5m_with_indicators.csv", index=False)

print(f"✅ Generated indicators and saved to data/SPY_5m_with_indicators.csv with {len(df)} rows.")