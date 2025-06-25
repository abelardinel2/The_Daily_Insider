from telegram_bot import send_telegram_message

def generate_summary():
    # Example static data - replace with real parser results
    buys = 10358620
    sells = 833319502
    ratio = round(sells / buys, 1)
    bias = "🟥 *Risk-Off*" if ratio > 10 else "🟨 Neutral" if ratio > 1 else "🟩 Accumulation"

    message = f"""
📅 *Insider Activity Summary – June 25, 2025*

💰 *Total Buys:* ${buys:,.0f}
💸 *Total Sells:* ${sells:,.0f}
⚖️ *Ratio (Sells:Buys):* {ratio}:1
🧭 *Market Bias:* {bias}

*Top Sales:*
• ORCL: $764M (CEO -77%)
• CRM, SLDE: Cluster sales

*Top Buys:*
• SONO: $4.2M (Fund)
• PSEC: $1.9M (CEO)

📉 Insider flow suggests caution.
"""
    send_telegram_message(message)

if __name__ == "__main__":
    generate_summary()
