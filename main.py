import pandas as pd
from telegram_bot import send_telegram_message
import datetime
import requests
from bs4 import BeautifulSoup
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def fetch_insider_summary():
    today = datetime.date.today()
    url = f"https://www.openinsider.com/screener?date={today}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    # Set up retry mechanism
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for 4xx/5xx errors
    except requests.exceptions.RequestException as e:
        error_message = f"⚠️ Error fetching data from OpenInsider: {str(e)}"
        send_telegram_message(error_message)  # Notify via Telegram
        print(error_message)
        return None  # Exit gracefully

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('table.tinytable tr')[1:]
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 9:
            ticker = cols[1].text.strip()
            insider = cols[5].text.strip()
            trade_type = cols[6].text.strip()
            amount_str = cols[10].text.strip().replace('$', '').replace(',', '')
            try:
                amount = float(amount_str)
                data.append((ticker, insider, trade_type, amount))
            except:
                continue

    if not data:
        error_message = f"⚠️ No valid data found for {today.strftime('%B %d, %Y')}"
        send_telegram_message(error_message)
        print(error_message)
        return None

    df = pd.DataFrame(data, columns=["Ticker", "Insider", "Type", "Amount"])
    buys = df[df["Type"] == "P - Purchase"]
    sells = df[df["Type"] == "S - Sale"]

    top_buys = buys.sort_values("Amount", ascending=False).head(3)
    top_sells = sells.sort_values("Amount", ascending=False).head(3)

    total_buy = buys["Amount"].sum()
    total_sell = sells["Amount"].sum()
    bias = "NEUTRAL"
    if total_sell > total_buy * 10:
        bias = "HEAVY SELL-SIDE PRESSURE 💣"
    elif total_buy > total_sell * 10:
        bias = "HEAVY BUY-SIDE PRESSURE 🚀"
    elif total_buy > total_sell:
        bias = "Moderate Buy Bias"
    elif total_sell > total_buy:
        bias = "Moderate Sell Bias"

    def format_row(row):
        return f"• {row['Ticker']} – ${row['Amount']:,.0f} ({row['Insider']})"

    summary = f"""📊 Insider Flow Summary – {today.strftime('%B %d, %Y')} {os.getenv('SUMMARY_LABEL', '')}

💸 Top Buys
{chr(10).join(top_buys.apply(format_row, axis=1))}

💥 Top Sells
{chr(10).join(top_sells.apply(format_row, axis=1))}

🧮 Total Buys: ${total_buy:,.0f} | Total Sells: ${total_sell:,.0f}
📈 Bias: {bias}"""

    return summary

if __name__ == "__main__":
    message = fetch_insider_summary()
    if message:
        send_telegram_message(message)