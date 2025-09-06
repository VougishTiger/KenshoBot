import yfinance as yf
import pandas as pd
import os

def fetch_and_save(ticker: str, interval= "5m", period= "60d"):
  print(f"📥 Fetching {ticker} - {interval} candles for {period}...")

  df= yf.download(tickers=ticker, interval= interval, period= period)

  if df.empty:
    print("❌ No data fetched.")
    return
  
  df.reset_index(inplace=True)
  
  if isinstance(df.columns, pd.MultiIndex):
    df.columns= ['_'.join([str(i) for i in col if i]) for col in df.columns]
  
  df.columns= [str(col).strip().lower().replace(" ","_") for col in df.columns]

  os.makedirs("data", exist_ok=True)
  filename= f"data/{ticker.upper()}_{interval}.csv"
  df.to_csv(filename, index= False)
  print(f"✅ Saved {len(df)} rows to {filename}")

if __name__=="__main__":
  fetch_and_save("SPY")