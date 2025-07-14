import feedparser
import json
import os
from datetime import datetime, timedelta
from send_telegram import send_telegram_alert

# Load CIK watchlist
with open("cik_watchlist.json", "r") as f:
    cik_data = json.load(f)["tickers"]

def parse_form4_rss():
    FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=4&company=&dateb=&owner=include&start=0&count=100&output=atom"
    feed = feedparser.parse(FEED_URL)
    alerts = []

    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        updated_str = entry.get("updated", "")

        # Convert to datetime object
        try:
            updated = datetime.strptime(updated_str, "%Y-%m-%dT%H:%M:%S-04:00")
        except ValueError:
            continue

        # Skip if older than 7 days
        if updated < seven_days_ago:
            continue

        # Filter to Form 4 and Form 4/A only
        if not any(ftype in title for ftype in ["4", "4/A"]):
            continue

        # Match any known CIK
        for ticker, info in cik_data.items():
            cik = str(info["cik"])
            if cik in link:
                alerts.append((ticker, cik, link))
                break

    return alerts

def main():
    alerts = parse_form4_rss()
    if not alerts:
        send_telegram_alert("🔍 No insider alerts found today.")
        return

    for ticker, cik, link in alerts:
        message = f"🔔 New Form 4 Alert for {ticker}:\n{link}"
        send_telegram_alert(message)

if __name__ == "__main__":
    main()