import pandas as pd
from signal_engine import detect_signals

df = pd.read_csv("data/SPY_1m_backtest_with_indicators.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

signals_df, confirmed_signals_df = detect_signals(df)

trades = []
trade_amount = 100
holding_period = 3

for _, signal in confirmed_signals_df.iterrows():
    entry_time = signal['datetime']
    entry_price = signal['price']
    signal_type = signal['signal']

    entry_idx = df.index[df['datetime'] == entry_time]
    if entry_idx.empty or entry_idx[0] + holding_period >= len(df):
        continue

    exit_price = df.iloc[entry_idx[0] + holding_period]['close']

    win = (exit_price > entry_price) if signal_type == 'CALL' else (exit_price < entry_price)
    pct_change = ((exit_price - entry_price) / entry_price) * (1 if signal_type == 'CALL' else -1)
    pnl = trade_amount * pct_change

    trades.append({
        'datetime': entry_time,
        'signal': signal_type,
        'entry_price': entry_price,
        'exit_price': exit_price,
        'win': win,
        'pct_change': round(pct_change * 100, 2),
        'pnl': round(pnl, 2),
        'setup_id': signal['setup_id']
    })

trades_df = pd.DataFrame(trades)
trades_df.to_csv("data/backtest_trade_results.csv", index=False)

total_trades = len(trades_df)
wins = trades_df['win'].sum()
win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
total_pnl = trades_df['pnl'].sum()

print(f"📊 Total Trades: {total_trades}")
print(f"✅ Wins: {wins}")
print(f"❌ Losses: {total_trades - wins}")
print(f"🎯 Win Rate: {win_rate:.2f}%")
print(f"💰 Net P&L: ${total_pnl:.2f}")
print("📁 Saved trade results to data/backtest_trade_results.csv")