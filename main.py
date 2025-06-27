import os
from telegram_bot import send_telegram_message
from collections import defaultdict
from datetime import datetime

# Dummy fallback data so your message is NEVER empty
buy_data = {"AAPL": 5_000_000, "TSLA": 3_000_000, "NVDA": 2_000_000}
sell_data = {"MSFT": 4_000_000, "AMZN": 2_500_000, "AMD": 1_500_000}

top_buys = sorted(buy_data.items(), key=lambda x: x[1], reverse=True)[:3]
top_sells = sorted(sell_data.items(), key=lambda x: x[1], reverse=True)[:3]

total_buys = sum(buy_data.values())
total_sells = sum(sell_data.values())

bias = "Neutral Bias"
if total_buys > total_sells:
    bias = "Buy-Side Bias"
elif total_sells > total_buys:
    bias = "Sell-Side Bias"

today = datetime.today().strftime("%B %d, %Y")
label = os.getenv("SUMMARY_LABEL", "Morning")

summary = f"""📊 Insider Flow Summary – {today} ({label})

💰 Top Buys
""" + "\n".join([f"{t} – ${v:,}" for t, v in top_buys]) + """

💥 Top Sells
""" + "\n".join([f"{t} – ${v:,}" for t, v in top_sells]) + f"""

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {bias} 👀
"""

try:
    send_telegram_message(summary)
except Exception as e:
    send_telegram_message(f"❌ Bot Error: {e}")