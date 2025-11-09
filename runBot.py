import time
from fetch_data import fetch_data
from generate_indicators import generate_indicators
from signal_engine import detect_signals

while True:
  try:
    df = fetch_data()
    df = generate_indicators(df)
    signals_df, confirmed_signals_df = detect_signals(df)

    if confirmed_signals_df.empty:
      print("⏳ No confirmed signals at this time.\n")
    else:
      print(f"🚨 {len(confirmed_signals_df)} confirmed signals found!\n")
      for _, signal in confirmed_signals_df.iterrows():
        print("========== SIGNAL ==========")
        print(f"🕒 Time: {signal['datetime']}")
        print(f"📈 Type: {signal['signal']}")
        print(f"💵 Price: ${signal['price']}")
        print(f"📊 RSI: {signal['rsi']:.2f}")
        print(f"📉 MACD Histogram: {signal['macd_hist']:.4f}")
        print(f"📍 EMA9: {signal['ema_9']:.2f}, EMA21: {signal['ema_21']:.2f}")
        print(f"📊 VWAP: {signal['vwap']:.2f}")
        print(f"📦 Volume: {int(signal['volume'])}, Avg(10): {int(signal['volume_avg_10'])}")
        print(f"📌 Support Zone: {signal['support_zone']:.2f}, Resistance Zone: {signal['resistance_zone']:.2f}")
        print(f"🧠 Setup ID: {signal['setup_id']}")
        print("✅ This is a high-confidence signal based on multiple indicators.\n")

    time.sleep(60)

  except Exception as e:
    print(f"❌ Error: {e}")
    time.sleep(60)