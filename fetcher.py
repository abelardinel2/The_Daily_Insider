# fetcher.py
# SEC EDGAR filing fetcher with rate limiting, retries, and Telegram notifications

import time
import logging
import requests
from requests.exceptions import RequestException
import xml.etree.ElementTree as ET
from config import COMPANY_NAME, SEC_EMAIL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, RSS_URL, USER_AGENT, SUMMARY_LABEL

# Configure logging
logging.basicConfig(
    filename="edgar_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Headers for SEC compliance
headers = {
    "User-Agent": USER_AGENT,
    "Accept": "application/xml,text/html"
}

def send_telegram_message(message):
    """Send error notifications via Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"{SUMMARY_LABEL} SEC Fetcher Error: {message}"
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        logging.error(f"Failed to send Telegram message: {str(e)}")

def fetch_with_rate_limit(url):
    """Fetch URL with rate limiting (100ms delay)."""
    time.sleep(0.1)  # 100ms delay to stay under 10 requests/second
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response

def fetch_with_retry(url, max_retries=3):
    """Fetch URL with retry logic and exponential backoff."""
    for attempt in range(max_retries):
        try:
            return fetch_with_rate_limit(url)
        except RequestException as e:
            error_msg = f"Attempt {attempt + 1} failed for {url}: {str(e)}"
            logging.error(error_msg)
            if response.status_code == 403:
                send_telegram_message(f"403 Forbidden: {url}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Backoff: 1s, 2s, 4s
            else:
                send_telegram_message(f"Failed to fetch {url} after {max_retries} attempts")
                raise Exception(error_msg)

def parse_rss_feed():
    """Parse SEC EDGAR RSS feed and fetch filing details."""
    try:
        # Fetch RSS feed
        rss_response = fetch_with_retry(RSS_URL)
        root = ET.fromstring(rss_response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        filings = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text
            link = entry.find("atom:link", ns).attrib["href"]
            # Only process URLs in /Archives/edgar/data (allowed by robots.txt)
            if "/Archives/edgar/data" in link:
                try:
                    filing_response = fetch_with_retry(link)
                    filings.append({
                        "title": title,
                        "url": link,
                        "content": filing_response.text
                    })
                    print(f"{SUMMARY_LABEL} Processed: {title} - {link}")
                except Exception as e:
                    error_msg = f"Failed to process filing {link}: {str(e)}"
                    logging.error(error_msg)
                    send_telegram_message(error_msg)
            else:
                logging.warning(f"Skipping disallowed URL: {link}")

        return filings

    except Exception as e:
        error_msg = f"Failed to parse RSS feed: {str(e)}"
        logging.error(error_msg)
        send_telegram_message(error_msg)
        return []

def main():
    """Main function to run the fetcher."""
    print(f"{SUMMARY_LABEL} SEC EDGAR Fetcher started by {COMPANY_NAME}")
    filings = parse_rss_feed()
    if filings:
        print(f"{SUMMARY_LABEL} Successfully processed {len(filings)} filings")
        for filing in filings:
            print(f"Title: {filing['title']}\nURL: {filing['url']}\n")
    else:
        print(f"{SUMMARY_LABEL} No filings processed")
        send_telegram_message("No filings processed")

if __name__ == "__main__":
    main()