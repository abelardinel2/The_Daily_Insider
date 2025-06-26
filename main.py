import requests
from datetime import datetime

# === Fetch insider data from Financial Modeling Prep ===
def fetch_insider_data():
    api_key = "k6DliYeidMR64Lix5q32uZEtKVsT671B"
    url = f"https://financialmodelingprep.com/api/v4/insider-trading?limit=100&apikey={api_key}"
    
    response = requests.get(url)
    data = response.json()

    trades = []
    for entry in data:
        try:
            price = float(entry.get("price", 0))
            shares = float(entry.get("securitiesTransacted", 0))
            amount = int(price * shares)
            action = entry.get("transactionType", "").lower()

            if amount == 0:
                continue  # Skip zero-value trades

            trades.append({
                "ticker": entry.get("ticker", "N/A"),
                "insider": entry.get("insiderName", "Unknown"),
                "action": action,
                "amount": amount
            })
        except Exception as e:
            print(f"Skipping bad entry: {e}")
            continue

    # Accept a broader set of action names
    buy_actions = {"buy", "purchase"}
    sell_actions = {"sale", "sell"}

    top_buys = sorted([t for t in trades if t["action"] in buy_actions], key=lambda x: -x["amount"])[:3]
    top_sells = sorted([t for t in trades if t["action"] in sell_actions], key=lambda x: -x["amount"])[:3]

    return {
        "top_buys": top_buys,
        "top_sells": top_sells,
        "total_buys": sum(t["amount"] for t in top_buys),
        "total_sells": sum(t["amount"] for t in top_sells)
    }

# === Generate the summary string ===
def generate_summary(time_label="Morning"):
    summary_data = fetch_insider_data()
    now = datetime.now().strftime("%B %d, %Y")

    summary = f"📊 Insider Flow Summary – {now} ({time_label})\n\n"

    summary += "💰 Top Buys\n"
    if summary_data["top_buys"]:
        for t in summary_data["top_buys"]:
            summary += f"- {t['ticker']}: ${t['amount']:,} by {t['insider']}\n"
    else:
        summary += "No significant buys.\n"

    summary += "\n💥 Top Sells\n"
    if summary_data["top_sells"]:
        for t in summary_data["top_sells"]:
            summary += f"- {t['ticker']}: ${t['amount']:,} by {t['insider']}\n"
    else:
        summary += "No significant sells.\n"

    summary += (
        f"\n🧮 Total Buys: ${summary_data['total_buys']:,} | "
        f"Total Sells: ${summary_data['total_sells']:,}"
    )

    if summary_data["total_buys"] > summary_data["total_sells"]:
        summary += "\n📈 Bias: Mild Buy–Side Bias 👀"
    elif summary_data["total_buys"] < summary_data["total_sells"]:
        summary += "\n📉 Bias: Mild Sell–Side Bias 👀"
    else:
        summary += "\n📊 Bias: Neutral 📎"

    return summary

# === Send to Telegram ===
def send_to_telegram(message):
    import os
    from telegram import Bot

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing Telegram credentials.")
        return

    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# === Main Execution ===
if __name__ == "__main__":
    try:
        summary = generate_summary()
        print(summary)
        send_to_telegram(summary)
    except Exception as e:
        print(f"Error: {e}")