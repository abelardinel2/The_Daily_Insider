import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text="✅ Test message from bot.")
