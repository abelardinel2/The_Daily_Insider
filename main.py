import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FMP_API_KEY = os.getenv("FMP_API_KEY")
SUMMARY_LABEL = os.getenv("SUMMARY_LABEL", "Daily")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def fetch_insider_data():
    url = f"https://financialmodelingprep.com/api/v4/insider-trading?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching insider data: {e}")
        return []

def generate_summary(label):
    data = fetch_insider_data()

    buys = {}
    sells = {}
    total_buys = 0
    total_sells = 0

    for trade in data:
        symbol = trade.get("symbol")
        transaction_type = trade.get("transactionType")
        cost = float(trade.get("cost", 0.0))
        insider = trade.get("insiderName", "Unknown")

        if transaction_type == "Buy":
            buys.setdefault(symbol, []).append((cost, insider))
            total_buys += cost
        elif transaction_type == "Sell":
            sells.setdefault(symbol, []).append((cost, insider))
            total_sells += cost

    def summarize(trades):
        sorted_trades = sorted(
            ((symbol, sum(c for c, _ in txns), txns[0][1]) for symbol, txns in trades.items()),
            key=lambda x: x[1], reverse=True
        )
        top3 = sorted_trades[:3]
        return [f"• {s} – ${v:,.0f} ({n})" for s, v, n in top3] if top3 else []

    buy_lines = summarize(buys)
    sell_lines = summarize(sells)

    bias = "NEUTRAL ⚖️"
    if total_buys > total_sells * 1.5:
        bias = "STRONG BUY-SIDE SUPPORT 🚀"
    elif total_sells > total_buys * 1.5:
        bias = "HEAVY SELL-SIDE PRESSURE 💣"
    elif total_sells > total_buys:
        bias = "Mild Sell–Side Bias 👀"
    elif total_buys > total_sells:
        bias = "Mild Buy–Side Bias 📈"

    message = f"""📊 Insider Flow Summary – {datetime.now():%B %d, %Y} ({label})

💰 Top Buys
{chr(10).join(buy_lines) if buy_lines else "None"}

💥 Top Sells
{chr(10).join(sell_lines) if sell_lines else "None"}

🧮 Total Buys: ${total_buys:,.0f} | Total Sells: ${total_sells:,.0f}
📉 Bias: {bias}"""

    return message

def main():
    label = SUMMARY_LABEL
    message = generate_summary(label)
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("✅ Message sent.")
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")

if __name__ == "__main__":
    main()