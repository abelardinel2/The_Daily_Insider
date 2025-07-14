from rss_parser import fetch_form4_entries
from sec_parser import parse_form4_txt
from fetcher import get_rss_feed
import telegram
import os

# Load environment variables (for local testing)
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

def summarize_trades(entries):
    if not entries:
        return None

    summary_lines = []
    for entry in entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        updated = entry.get("updated", "")
        summary_lines.append(f"📄 {title}\n🔗 {link}\n🕒 {updated}\n")

    return "\n".join(summary_lines)

def run_daily_summary():
    entries = fetch_form4_entries()
    summary = summarize_trades(entries)

    if summary:
        bot.send_message(chat_id=CHAT_ID, text=f"📢 Insider Trades (Form 4):\n\n{summary}")
    else:
        bot.send_message(chat_id=CHAT_ID, text="📭 No insider alerts found.")

if __name__ == "__main__":
    run_daily_summary()