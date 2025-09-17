import pandas as pd

initial_balance= 5000
position_size= initial_balance
holding_period= 200

df= pd.read_csv("data/SPY_5m_with_indicators.csv")
signals= pd.read_csv("data/confirmed_signals.csv")

df['datetime']= pd.to_datetime(df['datetime'])
signals['datetime']= pd.to_datetime(signals['datetime'])
df.set_index('datetime', inplace= True)

balance= initial_balance
trades= []

for _, signal in signals.iterrows():
  entry_time= signal['datetime']
  entry_price= signal['price']
  signal_type= signal['signal']

  try:
    entry_idx= df.index.get_loc(entry_time)
    exit_price= None

    for offset in range(1, holding_period+ 1):
      if entry_idx+ offset>= len(df):
        break

      future_row= df.iloc[entry_idx + offset]
      ret= (future_row['close'] - entry_price) / entry_price if signal_type == "CALL" else (entry_price - future_row['close'])/ entry_price

      if ret>= 0.05 or ret<= -0.02:
        exit_price= future_row['close']
        break

    if exit_price is None:
      exit_price= df.iloc[min(entry_idx + holding_period, len(df)-1)]['close']

    ret_pct= (exit_price - entry_price) / entry_price if signal_type == "CALL" else (entry_price - exit_price) / entry_price
    profit = round(position_size * ret_pct, 2)
    balance += profit

    trades.append({
      "datetime": entry_time,
      "signal": signal_type,
      "entry_price": entry_price,
      "exit_price": exit_price,
      "return_pct": round(ret_pct * 100, 2),
      "profit": profit,
      "balance": round(balance, 2)
    })

  except KeyError:
    continue

trades_df = pd.DataFrame(trades)
trades_df.to_csv("data/trade_log.csv", index=False)

print(f"📊 Final Balance: ${balance:.2f}")
print(f"💼 Trades Simulated: {len(trades_df)}")
 