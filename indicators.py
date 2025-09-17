import pandas as pd

def rename_columns(df):
  return df.rename(columns= {
    'close_spy': 'close',
    'open_spy': 'open',
    'high_spy': 'high', 
    'low_spy': 'low',
    'volume_spy': 'volume'
  })

def add_ema(df, periods):
  for p in periods:
    df[f"ema_{p}"]= df['close'].ewm(span=p, adjust=False).mean()

def add_macd(df):
  ema_12= df['close'].ewm(span= 12, adjust= False).mean()
  ema_26= df['close'].ewm(span= 26, adjust= False).mean()
  df['macd']= ema_12- ema_26
  df['macd_signal']= df['macd'].ewm(span= 9, adjust= False).mean()
  df['macd_hist']= df['macd']- df['macd_signal']

def add_rsi(df, period= 14):
  delta= df['close'].diff()
  gain= delta.clip(lower=0)
  loss= -delta.clip(upper= 0)
  avg_gain= gain.rolling(period).mean()
  avg_loss= loss.rolling(period).mean()
  rs= avg_gain/ avg_loss
  df['rsi']= 100-(100/ (1+rs))

def add_vwap(df):
  pv= (df['close']* df['volume']).cumsum()
  vol= df['volume'].cumsum()
  df['vwap']= pv/vol

def add_atr(df, period= 14):
  df['tr']= df[['high', 'low', 'close']].max(axis=1) - df[['high', 'low', 'close']].min(axis=1)
  df['atr']= df['tr'].rolling(period).mean()

def add_indicators(df):
  add_ema(df, [9, 21, 200])
  add_macd(df)
  add_rsi(df)
  add_vwap(df)
  add_atr(df)
  return df
