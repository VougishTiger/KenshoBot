import pandas as pd 
from indicators import rename_columns, add_indicators

df= pd.read_csv("data/SPY_5m.csv")

df= rename_columns(df)
df= add_indicators(df)

output_path= "data/SPY_5m_with_indicators.csv"
df.to_csv(output_path, index= False)

print(f"✅ Saved data with indicators to {output_path}")