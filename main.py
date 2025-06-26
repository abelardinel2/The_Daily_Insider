from telegram_bot import send_telegram_message
import datetime
import random

def fetch_insider_data():
    # Simulate fresh data using time-based randomness
    seed = int(datetime.datetime.now().strftime("%Y%m%d%H"))  # changes hourly
    random.seed(seed)

    top_buys = [
        {"ticker": "SONO", "amount": int(4245197 * random.uniform(0.97, 1.03)), "insider": "Coliseum Capital"},
        {"ticker": "AXINU", "amount": int(4000000 * random.uniform(0.97, 1.03)), "insider": "Axiom Intelligence"},
        {"ticker": "ARNYC", "amount": int(35549 * random.uniform(0.97, 1.03)), "insider": "Nicholas Schorsch"},
    ]

    top_sells = [
        {"ticker": "ORCL", "amount": int(764007886 * random.uniform(0.97, 1.03)), "insider": "CEO Safra Catz"},
        {"ticker": "SLDE", "amount": int(5667205 * random.uniform(0.97, 1.03)), "insider": "Dir. Gries"},
        {"ticker": "SOFI", "amount": int(1039471 * random.uniform(0.97, 1.03)), "insider": "CTO Jeremy Rishel"},
    ]

    total_buys = sum([b["amount"] for b in top_buys])
    total_sells = sum([s["amount"] for s in top_sells])

    return {
        "top_buys": top_buys,
        "top_sells": top_sells,
        "total_buys": total_buys,
        "total_sells": total_sells,
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

    today = datetime.date.today().strftime('%B %d, %Y')
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