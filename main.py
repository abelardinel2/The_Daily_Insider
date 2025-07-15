from telegram_bot import send_telegram_alert
from form4_summary import parse_form4_rss  # This should match the real parser you're using

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