from main import get_today_data

def send_daily_summary():
    summary = get_today_data()
    # Telegram bot logic to send `summary` to the user
    print("Sending to Telegram:", summary)

send_daily_summary()