from telegram_bot import send_telegram_alert
from rss_parser import parse_form4_rss  # ← this is the correct source now

def main():
    alerts = parse_form4_rss()
    if not alerts:
        send_telegram_alert("📭 No insider alerts found in the past 7 days.")
        return

    for link, buys, sells in alerts:
        message = (
            f"📢 Insider Alert:\n{link}\n"
            f"👤 Buys: {buys} | Sells: {sells}"
        )
        send_telegram_alert(message)

if __name__ == "__main__":
    main()