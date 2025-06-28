
import os
from telegram_bot import send_telegram_message

def get_real_summary():
    return "📊 Insider Flow Summary – Test (Morning)\n\n✅ Example test message."

if __name__ == "__main__":
    summary = get_real_summary()
    print(summary)
    send_telegram_message(summary)
