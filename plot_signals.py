import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_csv("data/SPY_5m_with_indicators.csv")
signals= pd.read_csv("data/confirmed_signals.csv")

df['datetime']= pd.to_datetime(df['datetime'])
signals['datetime']= pd.to_datetime(signals['datetime'])

df['signal']= None
df.set_index('datetime', inplace= True)
for _, row in signals.iterrows():
  dt= row['datetime']
  sig= row['signal']
  if dt in df.index:
    df.at[dt, 'signal']= sig


plt.figure(figsize=(15, 8))

plt.plot(df.index, df['close'], label='Close', color='black', linewidth=1)
plt.plot(df.index, df['ema_9'], label='EMA 9', linestyle='--')
plt.plot(df.index, df['ema_21'], label='EMA 21', linestyle='--')


call_signals= df[df['signal'] == 'CALL']
put_signals = df[df['signal'] == 'PUT']


plt.scatter(call_signals.index, call_signals['close'], label='CALL Signal', marker='^', color='green', s=100)
plt.scatter(put_signals.index, put_signals['close'], label='PUT Signal', marker='v', color='red', s=100)

if 'vwap' in df.columns:
  plt.plot(df.index, df['vwap'], label= 'VWAP', color= 'blue', alpha= 0.3)

plt.title("KenshoBot - Confirmed Signals")
plt.xlabel("Datetime")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("data/confirmed_signals_chart.png")
print("📸 Chart saved to data/confirmed_signals_chart.png")
