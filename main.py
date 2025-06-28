import os
import json
from send_telegram import send_telegram_message

def main():
    label = os.getenv("SUMMARY_LABEL", "Morning")

    with open("insider_flow.json") as f:
        data = json.load(f)

    buys = sells = 0
    for t in data:
        buys += data[t]["buys"]
        sells += data[t]["sells"]

    bias = "Neutral Bias"
    if buys > sells:
        bias = "Buy-Side Bias"
    elif sells > buys:
        bias = "Sell-Side Bias"

    msg = f"""📊 Insider Flow Summary – {label}

💰 Top Buys: {buys}
💥 Top Sells: {sells}

🧮 Total Buys: {buys} | Total Sells: {sells}
📉 Bias: {bias} 👀
"""
    send_telegram_message(msg)

if __name__ == "__main__":
    main()