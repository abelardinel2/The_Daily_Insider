import json
from send_telegram import send_telegram_message

def main():
    with open("insider_flow.json") as f:
        data = json.load(f)

    top_buys = data["top_buys"]
    top_sells = data["top_sells"]
    total_buys = data["total_buys"]
    total_sells = data["total_sells"]

    bias = "Neutral Bias 👀"
    if total_buys > total_sells:
        bias = "Buy-Side Bias 👀"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias 👀"

    message = f"""
📊 Insider Flow Summary

💰 Top Buys: ${top_buys:,}
💥 Top Sells: ${top_sells:,}

🧮 Total Buys: ${total_buys:,} | Total Sells: ${total_sells:,}
📉 Bias: {bias}
"""

    print(message)
    send_telegram_message(message)

if __name__ == "__main__":
    main()