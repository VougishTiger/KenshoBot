import csv
import os
from datetime import datetime

def log_bot_run(trades, win_rate, avg_return, total_return, max_drawdown):
  log_file= "logs/bot_log.csv"
  os.makedirs("logs", exist_ok= True)

  file_exists= os.path.isfile(log_file)

  with open(log_file, mode= "a", newline="") as file:
    writer= csv.writer(file)
    if not file_exists:
      writer.writerow([
        "timestamp", "trades_analyzed", "win_rate", 
        "avg_return", "total_return", "max_drawdown"
      ])

      writer.writerow([
        datetime.now().isoformat(),
        trades,
        round(win_rate, 2),
        round(avg_return, 2),
        round(total_return, 2),
        round(max_drawdown, 2)
      ])