# main.py  – Daily Insider entry-point
# -----------------------------------
# 1) Change `rss_parser` below if your parser file is named differently
#    (e.g., from rss_parser import parse_form4_rss)
# 2) Keep the telegram import exactly as shown.

from rss_parser import parse_form4_rss      # <-- adjust if your file name differs
from telegram_bot import send_telegram_alert


def main() -> None:
    """Fetch recent Form 4 / 4-A insider filings and push Telegram alerts."""
    alerts = parse_form4_rss()

    # Nothing found
    if not alerts:
        send_telegram_alert("🔍 No insider alerts found today.")
        return

    # Send an alert for each match
    for ticker, cik, link in alerts:
        message = (
            f"📢 Insider Alert for {ticker}\n"
            f"👤 CIK: {cik}\n"
            f"🔗 {link}"
        )
        send_telegram_alert(message)


if __name__ == "__main__":
    main()