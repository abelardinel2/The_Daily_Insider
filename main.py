from rss_parser import parse_form4_rss
from telegram_bot import send_telegram_alert

def main():
    alerts = parse_form4_rss()

    if not alerts:
        send_telegram_alert("🔍 No insider alerts found today.")
        return

    for ticker, cik, link in alerts:
        message = f"🔔 New Form 4 Alert for {ticker}:\n{link}"
        send_telegram_alert(message)

if __name__ == "__main__":
    main()