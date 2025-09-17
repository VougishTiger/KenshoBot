import pandas as pd

backtest_df= pd.read_csv("data/backtest_results.csv")
signal_df= pd.read_csv("data/confirmed_signals.csv")

backtest_df['datetime']= pd.to_datetime(backtest_df['datetime'])
signal_df['datetime']= pd.to_datetime(signal_df['datetime'])

grouped= backtest_df.groupby("type")

metrics= {}
for signal_type, group in grouped:
  win_rate= (group['return_pct'] > 0).mean() * 100
  avg_return= group['return_pct'].mean()
  metrics[signal_type]= {
    "win_rate": round(win_rate, 2),
    "avg_return": round(avg_return, 2)
  }

print("🔔 Signal Alerts:\n")

for _, row in signal_df.iterrows():
  sig_type= row['signal']
  sig_time= row['datetime']
  sig_price= row['price']

  if sig_type in metrics:
    win_rate= metrics[sig_type]['win_rate']
    avg_return= metrics[sig_type]['avg_return']
  else:
    win_rate= "N/A"
    avg_return= "N/A"

  print(f"📈 New Signal: {sig_type}")
  print(f"⏰ Time: {sig_time}")
  print(f"💵 Entry Price: ${sig_price:.2f}")
  print(f"📊 Historical Win Rate: {win_rate}%")
  print(f"📉 Historical Avg Return: {avg_return}%")
  print("-" * 40)