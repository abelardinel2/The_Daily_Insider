import os
from fetcher import fetch_all_form4s
from notifier import send_summary

def main():
    buys, sells = fetch_all_form4s(days=5)

    bias = "Neutral Bias 👀"
    if buys > sells:
        bias = "Buy-Side Bias 👀"
    elif sells > buys:
        bias = "Sell-Side Bias 👀"

    summary = f"""
📊 Insider Flow Summary

💰 Top Buys: {buys}
💥 Top Sells: {sells}

🧮 Total Buys: {buys} | Total Sells: {sells}
📉 Bias: {bias}
"""
    print(summary)
    send_summary(summary)

if __name__ == "__main__":
    main()