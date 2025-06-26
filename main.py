import os
from sec_edgar_downloader import Downloader
from telegram_bot import send_telegram_message

def get_summary():
    # Initialize the SEC Downloader with your email from environment
    email = os.getenv("SEC_EMAIL")
    if not email:
        raise ValueError("Missing SEC_EMAIL environment variable")

    dl = Downloader("sec_data", email_address=email)

    # Example: Download recent Form 4 filings for AAPL (replace with your logic)
    dl.get("4", "AAPL", amount=5)

    # Build the summary message
    summary = (
        f"📊 SEC Insider Summary – {os.getenv('SUMMARY_LABEL', '(Time Unknown)')}\n\n"
        f"Downloaded latest Form 4 filings for AAPL.\n"
        f"Data saved to: sec_data/\n"
        f"Additional parsing & summary logic goes here..."
    )

    return summary

if __name__ == "__main__":
    try:
        summary = get_summary()
        send_telegram_message(summary)
    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")
        raise