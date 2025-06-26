from telegram_bot import send_telegram_message
import requests
from datetime import datetime

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

            if amount == 0:
                continue

            trades.append({
                "ticker": entry.get("ticker", "N/A"),
                "insider": entry.get("insiderName", "Unknown"),
                "action": entry.get("transactionType", "Unknown"),
                "amount": amount
            })
        except:
            continue

    top_buys = sorted([t for t in trades if t["action"] == "Buy"], key=lambda x: -x["amount"])[:3]
    top_sells = sorted([t for t in trades if t["action"] == "Sale"], key=lambda x: -x["amount"])[:3]

    return {
        "top_buys": top_buys,
        "top_sells": top_sells,
        "total_buys": sum(t["amount"] for t in top_buys),
        "total_sells": sum(t["amount"] for t in top_sells)
    }

def generate_summary(label=""):
    data = fetch_insider_data()
    buys = data["top_buys"]
    sells = data["top_sells"]
    total_buys = data["total_buys"]
    total_sells = data["total_sells"]

    if total_buys > total_sells:
        bias = "BUY-SIDE BIAS 📈"
    elif total_sells > total_buys * 5:
        bias = "HEAVY SELL-SIDE PRESSURE 💣"
    else:
        bias = "Mild Sell–Side Bias 👀"

    today = datetime.now().strftime('%B %d, %Y')
    summary = f"📊 Insider Flow Summary – {today} {label}\n\n"

    summary += "💰 Top Buys\n"
    for b in buys:
        summary += f"• {b['ticker']} – ${b['amount']:,} ({b['insider']})\n"

    summary += "\n💥 Top Sells\n"
    for s in sells:
        summary += f"• {s['ticker']} – ${s['amount']:,} ({s['insider']})\n"

    summary += f"\n🧮 Total Buys: ${total_buys:,} | Total Sells: ${total_sells:,}\n"
    summary += f"📉 Bias: {bias}"
    return summary

if __name__ == "__main__":
    import os
    label = os.getenv("SUMMARY_LABEL", "(Morning)")
    message = generate_summary(label)
    send_telegram_message(message)