from telegram_bot import send_telegram_message
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_insider_data():
    url = "https://openinsider.com/latest-insider-trading"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "tinytable"})

    rows = table.find_all("tr")[1:]  # skip header
    trades = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 10:
            continue

        ticker = cols[1].text.strip()
        insider = cols[5].text.strip()
        action = cols[6].text.strip()
        amount_str = cols[9].text.strip().replace("$", "").replace(",", "")
        try:
            amount = int(float(amount_str))
        except:
            continue

        trades.append({
            "ticker": ticker,
            "insider": insider,
            "action": action,
            "amount": amount
        })

    buys = sorted([t for t in trades if "Buy" in t["action"]], key=lambda x: -x["amount"])[:3]
    sells = sorted([t for t in trades if "Sale" in t["action"]], key=lambda x: -x["amount"])[:3]

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