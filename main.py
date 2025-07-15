from telegram_bot import send_telegram_alert
from your_feed_parser import parse_form4_rss  # (or whatever your actual parser is named)

def main():
    alerts = parse_form4_rss()
    if not alerts:
        send_telegram_alert("🔍 No insider alerts found today.")
        return

    for ticker, cik, link in alerts:
        message = f"📢 Insider Alert: {ticker}\n👤 CIK: {cik}\n🔗 {link}"
        send_telegram_alert(message)

if __name__ == "__main__":
    main()