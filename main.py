import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
from time import sleep

# === Load secrets ===
load_dotenv()
API_KEY = os.getenv("FMP_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# === Config ===
FMP_URL = f"https://financialmodelingprep.com/api/v4/insider-trading?limit=300&apikey={API_KEY}"
RETRIES = 3
RETRY_DELAY = 3  # seconds

# === Fetch Insider Data ===
def fetch_insider_data():
    for attempt in range(RETRIES):
        try:
            response = requests.get(FMP_URL)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[Retry {attempt+1}] Error fetching data: {e}")
            sleep(RETRY_DELAY)
    return []

# === Format and Summarize ===
def generate_summary(data, time_label):
    today = datetime.now().date()
    buys = {}
    sells = {}
    total_buys = 0
    total_sells = 0

    for trade in data:
        date = datetime.strptime(trade['transactionDate'], "%Y-%m-%d").date()
        if date != today:
            continue

        symbol = trade.get("symbol", "")
        company = trade.get("issuerName", "")
        insider = trade.get("reportingCik", "")
        amount = float(trade.get("securitiesTransacted", 0) or 0) * float(trade.get("price", 0) or 0)
        transaction_type = trade.get("transactionType", "")

        if transaction_type == "Buy":
            buys[symbol] = (buys.get(symbol, (0, ""))[0] + amount, company)
            total_buys += amount
        elif transaction_type == "Sell":
            sells[symbol] = (sells.get(symbol, (0, ""))[0] + amount, company)
            total_sells += amount

    def format_top(dic):
        top = sorted(dic.items(), key=lambda x: x[1][0], reverse=True)[:3]
        return [f"• {symbol} – ${value[0]:,.0f} ({value[1]})" for symbol, value in top]

    summary = f"""📊 Insider Flow Summary – {today.strftime("%B %d, %Y")} ({time_label})

💰 Top Buys
{chr(10).join(format_top(buys)) if buys else "None"}

💥 Top Sells
{chr(10).join(format_top(sells)) if sells else "None"}

🧮 Total Buys: ${total_buys:,.0f} | Total Sells: ${total_sells:,.0f}
📉 Bias: {"HEAVY SELL-SIDE PRESSURE 💣" if total_sells > total_buys * 3 else "Mild Sell–Side Bias 👀" if total_sells > total_buys else "Buy-Side Activity 💚"}
"""
    return summary

# === Run Bot ===
if __name__ == "__main__":
    print("Fetching data...")
    data = fetch_insider_data()
    label = "Morning"
    message = generate_summary(data, label)
    print("Sending message to Telegram...")
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    print("✅ Done.")