import pandas as pd

def alert_user(signal):
  time = signal['datetime']
  signal_type = signal['signal']
  price = signal['price']
  setup_id = signal.get('setup_id', 'N/A')
  avg_return = signal.get('confidence_avg_return', 'N/A')
  win_rate = signal.get('confidence_win_rate', 'N/A')

  print("🔔 NEW TRADE ALERT")
  print(f"📅 Time: {time}")
  print(f"📈 Type: {signal_type}")
  print(f"💵 Price: {price}")
  print(f"⚙️ Strategy: {setup_id}")
  print(f"📊 Avg Return: {round(avg_return, 2)}%" if avg_return != 'N/A' else "📊 Avg Return: N/A")
  print(f"🏆 Win Rate: {round(win_rate, 2)}%" if win_rate != 'N/A' else "🏆 Win Rate: N/A")
  print("-" * 30)

if __name__ == "__main__":
  signals_df = pd.read_csv("data/confirmed_signals.csv")
  for _, signal in signals_df.iterrows():
    alert_user(signal)