from telegram_bot import send_telegram_message
import requests
from datetime import datetime

def fetch_insider_data():
    # ✅ Replace with your actual API key if not using .env
    api_key = "k6DliYeidMR64Lix5q32uZEtKVsT671B"
    url = f"https://financialmodelingprep.com/api/v4/insider-trading?apikey={api_key}"
    
    response = requests.get(url)
    data = response.json()

    trades = []
    for entry in data:
        try:
            trades.append({
                "ticker": entry.get("ticker"),
                "insider": entry.get("insiderName", "Unknown"),
                "action": entry.get("transactionType", "Unknown"),
                "amount": int(float(entry.get("price", 0)) * float(entry.get("securitiesTransacted", 0)))
            })
        except:
            continue

    # Get top 3 largest buys and sells
    buys = sorted([t for t in trades if t["action"] == "Buy"], key=lambda x: -x["amount"])[:3]
    sells = sorted([t for t in trades if t["action"] == "Sale"], key=lambda x: -x["amount"])[:3]

    return {
        "top_buys": buys,
        "top_sells": sells,
        "total_buys": sum(t["amount"] for t in buys),
        "total_sells": sum(t["amount"] for t in sells)
    }

def generate_summary(label=""):
    data = fetch_insider_data()
    buys = data["top_buys"]
    sells = data["top_sells"]
    total_buys = data["total_buys"]
    total_sells = data["total_sells"]

    # Bias logic
    if total_buys > total_sells:
        bias = "BUY-SIDE BIAS 📈"
    elif total_sells > total_buys * 5:
        bias = "HEAVY SELL-SIDE PRESSURE 💣"
    else:
        bias = "Mild Sell–Side Bias 👀"

    today = datetime.now().strftime('%B %d, %Y')
    summary = f"📊 Insider Flow Summary – {today} {label}\n\n"

    summary += "💰 Top Buys\n" + "\n".join(
        [f"• {b['ticker']} – ${b['amount']:,} ({b['insider']})" for b in buys]
    ) + "\n\n"

    summary += "💥 Top Sells\n" + "\n".join(
        [f"• {s['ticker']} – ${s['amount']:,} ({s['insider']})" for s in sells]
    ) + "\n\n"

    summary += f"🧮 Total Buys: ${total_buys:,} | Total Sells: ${total_sells:,}\n"
    summary += f"📉 Bias: {bias}"
    return summary

if __name__ == "__main__":
    import os
    time_label = os.getenv("SUMMARY_LABEL", "(Morning)")
    summary = generate_summary(time_label)
    send_telegram_message(summary)