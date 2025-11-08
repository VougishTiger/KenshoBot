import pandas as pd

def add_all_indicators(df):
  df["ema_9"] = df["close"].ewm(span=9, adjust=False).mean()
  df["ema_21"] = df["close"].ewm(span=21, adjust=False).mean()
  df["ema_200"] = df["close"].ewm(span=200, adjust=False).mean()

  exp1 = df["close"].ewm(span=12, adjust=False).mean()
  exp2 = df["close"].ewm(span=26, adjust=False).mean()
  df["macd"] = exp1 - exp2
  df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
  df["macd_hist"] = df["macd"] - df["macd_signal"]

  delta = df["close"].diff()
  gain = delta.where(delta > 0, 0)
  loss = -delta.where(delta < 0, 0)
  avg_gain = gain.rolling(window=14).mean()
  avg_loss = loss.rolling(window=14).mean()
  rs = avg_gain / avg_loss
  df["rsi"] = 100 - (100 / (1 + rs))

  df["vwap"] = (
    (df["high"] + df["low"] + df["close"]) / 3 * df["volume"]
  ).cumsum() / df["volume"].cumsum()

  return df