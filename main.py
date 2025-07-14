from rss_parser import fetch_form4_entries
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from telegram import Bot
import os

bot = Bot(token=TELEGRAM_BOT_TOKEN)

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
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"📢 Insider Trades (Form 4):\n\n{summary}")
    else:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="📭 No insider alerts found.")

if __name__ == "__main__":
    run_daily_summary()
