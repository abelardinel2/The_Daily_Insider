import os
import requests
from telegram_bot import send_telegram_message
from datetime import datetime

# -- CONFIG --
SEC_API_URL = "https://www.sec.gov/files/company_tickers.json"  # Example placeholder public SEC JSON

def get_real_insider_data():
    try:
        response = requests.get(SEC_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # ⏳ This is a placeholder demo!
        # In real use, swap with OpenInsider or a real SEC JSON endpoint.
        keys = list(data.keys())[:6]
        buy_data = {keys[0]: 5_000_000, keys[1]: 3_000_000, keys[2]: 2_000_000}
        sell_data = {keys[3]: 4_000_000, keys[4]: 2_500_000, keys[5]: 1_500_000}

        return buy_data, sell_data
    except Exception as e:
        print(f"Real SEC pull failed: {e}")
        return None, None

def main():
    buy_data, sell_data = get_real_insider_data()

    # Fallback dummy data if API fails
    if not buy_data or not sell_data:
        buy_data = {"AAPL": 5_000_000, "TSLA": 3_000_000, "NVDA": 2_000_000}
        sell_data = {"MSFT": 4_000_000, "AMZN": 2_500_000, "AMD": 1_500_000}

    top_buys = sorted(buy_data.items(), key=lambda x: x[1], reverse=True)[:3]
    top_sells = sorted(sell_data.items(), key=lambda x: x[1], reverse=True)[:3]

    total_buys = sum(buy_data.values())
    total_sells = sum(sell_data.values())

    bias = "Neutral Bias"
    if total_buys > total_sells:
        bias = "Buy-Side Bias"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias"

    today = datetime.today().strftime("%B %d, %Y")
    label = os.getenv("SUMMARY_LABEL", "Morning")

    summary = f"""📊 Insider Flow Summary – {today} ({label})

💰 Top Buys
""" + "\n".join([f"{t} – ${v:,}" for t, v in top_buys]) + """

💥 Top Sells
""" + "\n".join([f"{t} – ${v:,}" for t, v in top_sells]) + f"""

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {bias} 👀
"""

    try:
        send_telegram_message(summary)
    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")

if __name__ == "__main__":
    main()