import pandas as pd

df= pd.read_csv("data/SPY_5m.csv")

print("🧪 Columns:", df.columns.tolist())
date_col= next((col for col in df.columns if "date" in col.lower()), None)
if not date_col:
  raise Exception("❌ Could not find a datetime column. Please check CSV column names.")

print("✅ Rows:", len(df))
print("📅 Date range:", df[date_col].iloc[0], "→", df[date_col].iloc[-1])
print("\n🧠 First 5 rows:")
print(df.head())

print("\n🔍 Missing values:")
print(df.isnull().sum())