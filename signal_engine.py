import pandas as pd

def detect_signals(df):
  signals= []
  confirmed_signals= []

  df['volume_avg_10']= df['volume'].rolling(10).mean()
  df['macd_cross_up'] = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
  df['macd_cross_down']= (df['macd']< df['macd_signal'])& (df['macd'].shift(1)>= df['macd_signal'].shift(1))
  df['macd_cross_up_recent']= df['macd_cross_up'].rolling(3).max()
  df['macd_cross_down_recent']= df['macd_cross_down'].rolling(3).max()
  df['rsi_diff']= df['rsi'].diff()
  df['ema_9_slope'] = df['ema_9'].diff()
  df['macd_hist_trend'] = df['macd_hist'].diff()

  df['datetime'] = pd.to_datetime(df['datetime'])

  for i in range(len(df)):
    row= df.iloc[i]

    if i< 21:
      continue

    range_ = row['high'] - row['low']
    if range_ < 0.3:  
      continue

    hour = row['datetime'].hour
    if hour < 9 or hour > 15:
      continue

    score = 0

    if (
      row['close']> row['ema_9']> row['ema_21'] and
      row['macd_cross_up_recent'] and
      row['rsi']> 40 and
      row['close']> row['vwap'] and
      row['volume']> row['volume_avg_10']
    ):
      signal= {
        "datetime": row['datetime'],
        "signal": "CALL",
        "price": row['close']
      }
      signals.append(signal)

      if row['rsi_diff']> 0:
        score += 1
      if row['ema_9_slope'] > 0:
        score += 1
      if row['macd_hist_trend'] > 0:
        score += 1
      if row['macd_cross_up']:
        score += 1

      if score >= 3:
        confirmed_signals.append(signal)

    if (
      row['close'] < row['ema_9'] < row['ema_21'] and
      row['macd_cross_down_recent'] and
      row['rsi'] < 60 and
      row['close'] < row['vwap'] and
      row['volume'] > row['volume_avg_10']
    ):
      signal= {
         "datetime": row['datetime'],
         "signal": "PUT",
         "price": row['close']
      }
      signals.append(signal)

      if row['rsi_diff']< 0:
        score += 1
      if row['ema_9_slope'] < 0:
        score += 1
      if row['macd_hist_trend'] < 0:
        score += 1
      if row['macd_cross_down']:
        score += 1

      if score >= 3:
        confirmed_signals.append(signal)

  return pd.DataFrame(signals), pd.DataFrame(confirmed_signals)


if __name__ == "__main__":
  df= pd.read_csv("data/SPY_5m_with_indicators.csv")
  signals_df, confirmed_signals_df= detect_signals(df)

  if signals_df.empty:
    print("⚠️ No signals found.")
  
  else:
    print(f"✅ Found {len(signals_df)} signals:")
    print(signals_df.tail())

    signals_df.to_csv("data/signals.csv", index=False)
    confirmed_signals_df.to_csv("data/confirmed_signals.csv", index= False)
    print("📁 Saved to data/signals.csv and data/confirmed_signals.csv")
