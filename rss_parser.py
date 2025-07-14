import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from send_telegram import send_telegram_alert

FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=4&company=&dateb=&owner=include&start=0&count=100&output=atom"

def extract_transaction_type(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")
    buys = sells = 0
    for row in rows:
        cells = row.find_all("td")
        for cell in cells:
            if cell.text.strip() == "P":
                buys += 1
            elif cell.text.strip() == "S":
                sells += 1
    return buys, sells

def parse_form4_rss():
    feed = feedparser.parse(FEED_URL)
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    results = []

    for entry in feed.entries:
        title = entry.get("title", "").lower()
        link = entry.get("link", "")
        updated_str = entry.get("updated", "")
        try:
            updated = datetime.strptime(updated_str, "%Y-%m-%dT%H:%M:%S-04:00")
        except ValueError:
            continue

        if updated < week_ago:
            continue

        if not ("form 4" in title or "form 4/a" in title):
            continue

        try:
            html = requests.get(link).text
            buys, sells = extract_transaction_type(html)
            if buys > 0 or sells > 0:
                results.append((link, buys, sells))
        except Exception as e:
            print(f"Error parsing {link}: {e}")

    return results

def main():
    alerts = parse_form4_rss()
    if not alerts:
        send_telegram_alert("📭 No insider alerts found in the past 7 days.")
        return

    for link, buys, sells in alerts:
        msg = f"📢 Insider Alert:
{link}
👤 Buys: {buys} | Sells: {sells}"
        send_telegram_alert(msg)

if __name__ == "__main__":
    main()