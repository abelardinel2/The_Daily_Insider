import os
from telegram_bot import send_telegram_message
from sec_edgar_downloader import Downloader

def get_summary():
    sec_email = os.getenv("SEC_EMAIL")
    if not sec_email:
        raise ValueError("Missing SEC_EMAIL environment variable")

    # Initialize downloader with email and output directory
    dl = Downloader("sec_data", sec_email)

    # Download the 5 latest Form 4 filings for AAPL
    dl.get("4", "AAPL", 5)

    # For now, just send a placeholder message
    summary = "✅ Successfully downloaded latest AAPL Form 4 filings from SEC EDGAR"
    return summary

if __name__ == "__main__":
    try:
        summary = get_summary()
        send_telegram_message(summary)
    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")