import pandas as pd

df= pd.read_csv("data/SPY_5m_with_indicators.csv")
signals= pd.read_csv("data/confirmed_signals.csv")

df['datetime']= pd.to_datetime(df['datetime'])
signals['datetime']= pd.to_datetime(signals['datetime'])

df.set_index('datetime', inplace= True)

holding_period= 50
results= []

for _, signal in signals.iterrows():
  entry_time= signal['datetime']
  entry_price= signal['price']
  signal_type= signal['signal']

  try:

    entry_idx= df.index.get_loc(entry_time)

    exit_idx= entry_idx + holding_period
    if exit_idx >= len(df):
      continue

    exit_row= df.iloc[exit_idx]
    exit_price= exit_row['close']

    if signal_type == "CALL":
      ret= (exit_price - entry_price)/ entry_price
    elif signal_type == "PUT":
      ret= (entry_price - exit_price)/ entry_price
    else:
      continue

    results.append({
      "datetime": entry_time,
      "type": signal_type,
      "entry_price": entry_price,
      "exit_price": exit_price,
      "return_pct": round(ret* 100, 2)
    })

  except KeyError:
    continue 

results_df= pd.DataFrame(results)
results_df['cumulative_return'] = (1 + results_df['return_pct'] / 100).cumprod()
results_df['drawdown'] = results_df['cumulative_return'] / results_df['cumulative_return'].cummax() - 1

results_df.to_csv("data/backtest_results.csv", index= False)

if results_df.empty:
  print("⚠️ No valid trades for backtest.")

else: 
  win_rate= (results_df['return_pct']> 0). mean()* 100
  avg_return= results_df['return_pct'].mean()
  total_return= results_df['return_pct'].sum()
  max_drawdown = results_df['drawdown'].min() * 100

  print("✅ Backtest Complete!")
  print(f"📈 Trades Analyzed: {len(results_df)}")
  print(f"🏆 Win Rate: {win_rate:.2f}%")
  print(f"📊 Average Return: {avg_return:.2f}%")
  print(f"💰 Total Return: {total_return:.2f}%")
  print(f"📉 Max Drawdown: {max_drawdown:.2f}%")
