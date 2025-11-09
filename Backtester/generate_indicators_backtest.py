import pandas as pd
from indicators import add_all_indicators

df = pd.read_csv("data/SPY_1m_backtest.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

numeric_cols = ["open", "high", "low", "close", "volume"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df.dropna(subset=numeric_cols, inplace=True)

df = add_all_indicators(df)
df.to_csv("data/SPY_1m_backtest_with_indicators.csv", index=False)

print(f"✅ Saved to data/SPY_1m_backtest_with_indicators.csv with {len(df)} rows.")