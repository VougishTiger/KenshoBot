import pandas as pd

def detect_signals(df):
  signals= []

  df['volume_avg_10']= df['volume'].rolling(10).mean()

  df['macd_cross_up'] = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
  df['macd_cross_down']= (df['macd']< df['macd_signal'])& (df['macd'].shift(1)>= df['macd_signal'].shift(1))
  df['macd_cross_up_recent']= df['macd_cross_up'].rolling(3).max()
  df['macd_cross_down_recent']= df['macd_cross_down'].rolling(3).max()

  for i in range(len(df)):
    row= df.iloc[i]

    if i< 21:
      continue

    if (
      row['close']> row['ema_9']> row['ema_21'] and
      row['macd_cross_up_recent'] and
      row['rsi']> 40 and
      row['close']> row['vwap'] and
      row['volume']> row['volume_avg_10']
    ):
      signals.append({
        "datetime": row['datetime'],
        "signal": "CALL",
        "price": row['close']
      })

    if (
      row['close'] < row['ema_9'] < row['ema_21'] and
      row['macd_cross_down_recent'] and
      row['rsi'] < 60 and
      row['close'] < row['vwap'] and
      row['volume'] > row['volume_avg_10']
    ):
      signals.append({
        "datetime": row['datetime'],
        "signal": "PUT",
        "price": row['close']
      })

  return pd.DataFrame(signals)


if __name__ == "__main__":
  df= pd.read_csv("data/SPY_5m_with_indicators.csv")
  signals_df= detect_signals(df)

  if signals_df.empty:
    print("⚠️ No signals found.")
  
  else:
    print(f"✅ Found {len(signals_df)} signals:")
    print(signals_df.tail())

    signals_df.to_csv("data/signals.csv", index=False)
    print("📁 Saved to data/signals.csv")
