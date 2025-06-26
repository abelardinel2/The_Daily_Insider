from telegram_bot import send_telegram_message
import requests
import pandas as pd
from datetime import datetime
from io import StringIO

def fetch_insider_data():
    # Pull the latest insider trades from OpenInsider's CSV endpoint
    url = "https://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=0&fdr=&td=0&tdr=&daysago=&xp=1&vl=&vh=&oc=&sicMin=&sicMax=&sortcol=0&maxresults=500&sortdir=desc&tabletype=transaction&csv=true"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch OpenInsider data")

    df = pd.read_csv(StringIO(response.text))

    # Clean column names
    df.columns = df.columns.str.strip()

    # Filter out non-buy/sale transactions and compute $ value
    df = df[df['Transaction'].isin(['Buy', 'Sale'])].copy()
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
    df['$Value'] = df['Price'] * df['Qty']

    df = df.dropna(subset=['$Value'])

    top_buys = df[df['Transaction'] == 'Buy'].sort_values('$Value', ascending=False).head(3)
    top_sells = df[df['Transaction'] == 'Sale'].sort_values('$Value', ascending=False).head(3)

    return {
        "top_buys": top_buys,
        "top_sells": top_sells,
        "total_buys": int(top_buys['$Value'].sum()),
        "total_sells": int(top_sells['$Value'].sum())
    }

def generate_summary(label=""):
    data = fetch_insider_data()
    buys = data["top_buys"]
    sells = data["top_sells"]
    total_buys = data["total_buys"]
    total_sells = data["total_sells"]

    if total_buys > total_sells:
        bias = "BUY-SIDE BIAS 📈"
    elif total_sells > total_buys * 5:
        bias = "HEAVY SELL-SIDE PRESSURE 💣"
    else:
        bias = "Mild Sell–Side Bias 👀"

    today = datetime.now().strftime('%B %d, %Y')
    summary = f"📊 Insider Flow Summary – {today} {label}\n\n"

    summary += "💰 Top Buys\n"
    for _, row in buys.iterrows():
        summary += f"• {row['Ticker']} – ${int(row['$Value']):,} ({row['Insider Name']})\n"

    summary += "\n💥 Top Sells\n"
    for _, row in sells.iterrows():
        summary += f"• {row['Ticker']} – ${int(row['$Value']):,} ({row['Insider Name']})\n"

    summary += f"\n🧮 Total Buys: ${total_buys:,} | Total Sells: ${total_sells:,}\n"
    summary += f"📉 Bias: {bias}"

    return summary

if __name__ == "__main__":
    import os
    label = os.getenv("SUMMARY_LABEL", "(Morning)")
    message = generate_summary(label)
    send_telegram_message(message)