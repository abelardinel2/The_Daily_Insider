import time
from datetime import datetime
from rss_parser import fetch_form4_entries
from sec_parser import parse_form4_txt
from fetcher import get_rss_feed

def run_daily_summary():
    entries = fetch_form4_entries()
    summary = summarize_trades(entries)

    if summary:
        send_telegram_message(summary)
    else:
        send_telegram_message("📭 No insider alerts found for today.")

if __name__ == "__main__":
    run_daily_summary()
