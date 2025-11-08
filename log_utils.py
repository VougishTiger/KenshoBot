import datetime
import os

def log_bot_run(trades, win_rate, avg_return, total_return, max_drawdown):
  log_dir = "logs"
  os.makedirs(log_dir, exist_ok=True)
  log_file = os.path.join(log_dir, "bot_run_log.txt")
  
  with open(log_file, "a") as f:
    f.write(f"--- Run at {datetime.datetime.now()} ---\n")
    f.write(f"Trades: {trades}\n")
    f.write(f"Win Rate: {win_rate:.2f}%\n")
    f.write(f"Average Return: {avg_return:.2f}%\n")
    f.write(f"Total Return: {total_return:.2f}%\n")
    f.write(f"Max Drawdown: {max_drawdown:.2f}%\n")
    f.write("\n")