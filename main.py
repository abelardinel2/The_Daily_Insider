import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime

def fetch_openinsider_data(limit=10):
    url = "http://openinsider.com/latest-insider-trading"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', class_='tinytable')
    rows = table.find_all('tr')[1:]

    results = []
    for row in rows[:limit]:
        cols = row.find_all('td')
        if len(cols) > 7:
            data = {
                'ticker': cols[0].text.strip(),
                'owner': cols[1].text.strip(),
                'relationship': cols[2].text.strip(),
                'date': cols[3].text.strip(),
                'transaction': cols[5].text.strip(),
                'shares': cols[6].text.strip(),
                'price': cols[7].text.strip()
            }
            results.append(data)
    return results

def summarize_trades(data):
    buys, sells = [], []
    for trade in data:
        if 'buy' in trade['transaction'].lower():
            buys.append(trade)
        elif 'sell' in trade['transaction'].lower():
            sells.append(trade)
    return buys, sells

def format_message(buys, sells, label):
    msg = f"📊 Insider Flow Summary – {datetime.now().strftime('%B %d, %Y')} ({label})\n\n"
    msg += "💰 Top Buys\n"
    if buys:
        for b in buys:
            msg += f"- {b['ticker']}: {b['shares']} @ ${b['price']} by {b['owner']}\n"
    else:
        msg += "None\n\n"

    msg += "💥 Top Sells\n"
    if sells:
        for s in sells:
            msg += f"- {s['ticker']}: {s['shares']} @ ${s['price']} by {s['owner']}\n"
    else:
        msg += "None\n\n"

    msg += f"🧮 Total Buys: {len(buys)} | Total Sells: {len(sells)}\n"
    if len(buys) > len(sells):
        msg += "📈 Bias: Accumulation 💚"
    elif len(sells) > len(buys):
        msg += "📉 Bias: Distribution 💔"
    else:
        msg += "⚖️ Bias: Neutral ⚖️"
    return msg

def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    label = os.getenv("SUMMARY_LABEL", "Morning")

    bot = Bot(token=bot_token)
    data = fetch_openinsider_data()
    buys, sells = summarize_trades(data)
    message = format_message(buys, sells, label)
    bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    main()