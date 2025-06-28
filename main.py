import os
import sqlite3
from datetime import datetime
from telegram_bot import send_telegram_message

DB_PATH = "/data/insider.db" if os.getenv("RAILWAY_VOLUME") else "insider.db"

def save_summary(buys, sells, bias):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            buys INTEGER,
            sells INTEGER,
            bias TEXT
        )
    """)
    c.execute("""
        INSERT INTO summaries (date, buys, sells, bias)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M"), buys, sells, bias))
    conn.commit()
    conn.close()

def get_summary():
    # Dummy data for now
    buys = 50000000
    sells = 0
    bias = "Buy-Side Bias"
    return buys, sells, bias

if __name__ == "__main__":
    buys, sells, bias = get_summary()
    save_summary(buys, sells, bias)
    message = f"""📊 Insider Flow Summary – {datetime.now().strftime('%B %d, %Y')} (Morning)

💰 Top Buys: ${buys:,.0f}
💥 Top Sells: ${sells:,.0f}

🧮 Total Buys: ${buys/1e6:.1f}M | Total Sells: ${sells/1e6:.1f}M
📉 Bias: {bias} 👀
"""
    send_telegram_message(message)
    print("✅ Summary sent & saved.")