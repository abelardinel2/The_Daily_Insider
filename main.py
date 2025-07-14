from fetcher import fetch_form4_entries
from form4_summary import summarize_trades
from telegram_bot import send_telegram_message

def run_daily_summary():
    entries = fetch_form4_entries()
    summary = summarize_trades(entries)

    if summary:
        send_telegram_message(summary)
    else:
        send_telegram_message("📭 No insider alerts found today.")

if __name__ == "__main__":
    run_daily_summary()