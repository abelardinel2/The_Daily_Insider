import os
from datetime import datetime, timedelta
from parse_form4 import get_recent_form4_amounts
from telegram_bot import send_telegram_message

today = datetime.today()
yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
label = os.getenv("SUMMARY_LABEL", "Morning")

tickers = ["GETY", "HOVR", "MCW"]

email = os.getenv("SEC_EMAIL")
if not email:
    raise ValueError("SEC_EMAIL must be set!")

total_buys = 0
total_sells = 0

for ticker in tickers:
    try:
        amounts = get_recent_form4_amounts(ticker, email)
        total_buys += amounts["buys"]
        total_sells += amounts["sells"]
    except Exception as e:
        send_telegram_message(f"❌ Bot Error for {ticker}: {e}")

bias = "Neutral Bias"
if total_buys > total_sells:
    bias = "Buy-Side Bias"
elif total_sells > total_buys:
    bias = "Sell-Side Bias"

summary = f"""📊 Insider Flow Summary – {yesterday} ({label})

💰 Top Buys: ${total_buys}
💥 Top Sells: ${total_sells}

🧮 Total Buys: ${total_buys:.1f} | Total Sells: ${total_sells:.1f}
📉 Bias: {bias} 👀
"""

send_telegram_message(summary)