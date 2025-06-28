import json

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

    print(f"""📊 Insider Flow Summary

💰 Top Buys: ${top_buys:,}
💥 Top Sells: ${top_sells:,}

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {bias}
""")

if __name__ == "__main__":
    main()