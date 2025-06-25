from telegram_bot import send_telegram_message
import datetime

def fetch_insider_data():
    # Placeholder — replace with actual parsing logic
    return {
        "top_buys": [
            {"ticker": "SONO", "amount": 4245197, "insider": "Coliseum Capital"},
            {"ticker": "AXINU", "amount": 4000000, "insider": "Axiom Intelligence"},
            {"ticker": "ARNYC", "amount": 35549, "insider": "Nicholas Schorsch"}
        ],
        "top_sells": [
            {"ticker": "ORCL", "amount": 764007886, "insider": "CEO Safra Catz"},
            {"ticker": "SLDE", "amount": 5667205, "insider": "Dir. Gries"},
            {"ticker": "SOFI", "amount": 1039471, "insider": "CTO Jeremy Rishel"}
        ],
        "total_buys": 8320746,
        "total_sells": 770684562
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
        bias = "Mild Sell-Side Bias 👀"

    today = datetime.date.today().strftime('%B %d, %Y')
    summary = f"📊 Insider Flow Summary – {today} {label}\n\n"

    summary += "💸 Top Buys\n" + "\n".join(
        [f"• {b['ticker']} – ${b['amount']:,} ({b['insider']})" for b in buys]
    ) + "\n\n"

    summary += "💥 Top Sells\n" + "\n".join(
        [f"• {s['ticker']} – ${s['amount']:,} ({s['insider']})" for s in sells]
    ) + "\n\n"

    summary += f"📈 Bias: {bias}"
    return summary

if __name__ == "__main__":
    import os
    time_label = os.getenv("SUMMARY_LABEL", "(Morning)")
    summary = generate_summary(time_label)
    send_telegram_message(summary)
