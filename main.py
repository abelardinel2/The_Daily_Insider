import os
from telegram_bot import send_telegram_message
from db import save_snapshot, load_snapshot

SUMMARY_LABEL = os.getenv("SUMMARY_LABEL", "Morning")

def main():
    try:
        buys = 10_000_000
        sells = 8_000_000
        bias = "Buy-Side Bias"

        snapshot = {
            "label": SUMMARY_LABEL,
            "buys": buys,
            "sells": sells,
            "bias": bias
        }

        save_snapshot(snapshot)
        previous = load_snapshot()

        message = f"""📊 Insider Flow Summary – Test ({SUMMARY_LABEL})

💰 Top Buys: ${buys:,}
💥 Top Sells: ${sells:,}

🧮 Total Buys: ${buys/1e6:.1f}M | Total Sells: ${sells/1e6:.1f}M
📉 Bias: {bias} 👀
"""
        send_telegram_message(message)

    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")

if __name__ == "__main__":
    main()