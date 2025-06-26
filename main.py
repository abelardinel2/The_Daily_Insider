import requests
import pandas as pd
import datetime
import os
from telegram_bot import send_telegram_message

def fetch_data():
    url = f"https://www.openinsider.com/screener?date={datetime.datetime.now().strftime('%Y-%m-%d')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    return pd.read_html(response.text)

def parse_table(tables):
    df = tables[11]  # Targeting the correct table index from OpenInsider
    df.columns = df.columns.droplevel(0)
    df = df.rename(columns=lambda col: col.strip())
    df = df[df['Trade Type'].str.contains('P|S')]
    df['Cost'] = df['Price'] * df['Qty (#)']
    return df

def summarize(df):
    df['Buy/Sell'] = df['Trade Type'].apply(lambda x: 'Buy' if 'P' in x else 'Sell')
    total_buys = df[df['Buy/Sell'] == 'Buy']['Cost'].sum()
    total_sells = df[df['Buy/Sell'] == 'Sell']['Cost'].sum()

    top_buys = df[df['Buy/Sell'] == 'Buy'].nlargest(3, 'Cost')
    top_sells = df[df['Buy/Sell'] == 'Sell'].nlargest(3, 'Cost')

    bias = "NEUTRAL"
    if total_buys > total_sells * 2:
        bias = "HEAVY BUY-SIDE PRESSURE 💚"
    elif total_sells > total_buys * 2:
        bias = "HEAVY SELL-SIDE PRESSURE 💣"
    elif total_buys > total_sells:
        bias = "MILD BUY-SIDE BIAS"
    elif total_sells > total_buys:
        bias = "MILD SELL-SIDE BIAS"

    return top_buys, top_sells, total_buys, total_sells, bias

def format_summary(top_buys, top_sells, total_buys, total_sells, bias):
    today = datetime.datetime.now().strftime("%B %d, %Y")
    summary = f"📊 Insider Flow Summary – {today}\n\n"

    summary += "💸 Top Buys\n"
    for _, row in top_buys.iterrows():
        summary += f"• {row['Ticker']} – ${row['Cost']:,.0f} ({row['Insider Name']})\n"

    summary += "\n💥 Top Sells\n"
    for _, row in top_sells.iterrows():
        summary += f"• {row['Ticker']} – ${row['Cost']:,.0f} ({row['Insider Name']})\n"

    summary += f"\n🧮 Total Buys: ${total_buys:,.0f} | Total Sells: ${total_sells:,.0f}\n"
    summary += f"📈 Bias: {bias}"

    return summary

def main():
    tables = fetch_data()
    df = parse_table(tables)
    top_buys, top_sells, total_buys, total_sells, bias = summarize(df)
    summary_text = format_summary(top_buys, top_sells, total_buys, total_sells, bias)
    send_telegram_message(summary_text)

if __name__ == "__main__":
    main()