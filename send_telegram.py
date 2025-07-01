import os
import json
import requests

# Get environment variables
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
summary_label = os.getenv("SUMMARY_LABEL", "Insider Flow")
company_name = os.getenv("COMPANY_NAME", "Analytics")

# Load data from insider_flow.json
try:
    with open("insider_flow.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    message = "📊 Error: insider_flow.json not found"
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text": message})
    exit(1)

# Format the message
message = f"📊 {summary_label} Summary ({company_name}) (June 26, 2025–July 01, 2025)\n\n"
message += f"💰 Top Buys: ${data['top_buys']:,.2f}\n"
message += f"💥 Top Sells: ${data['top_sells']:,.2f}\n\n"
message += f"🧮 Total Buys: ${data['total_buys']:,.2f} | Total Sells: ${data['total_sells']:,.2f}\n"
total_trades = data['total_buys'] + data['total_sells']
bias = "Overwhelming Sell Dominance" if data['total_sells'] > data['total_buys'] else "Balanced Market"
message += f"📉 {bias} ({(data['total_buys'] / total_trades * 100 if total_trades else 0):.2f}% buy, {(data['total_sells'] / total_trades * 100 if total_trades else 0):.2f}% sell) 👀"

# Send the message
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
response = requests.post(url, data={"chat_id": chat_id, "text": message})
if response.status_code != 200:
    print(f"Failed to send message: {response.text}")
else:
    print("Telegram message sent successfully")