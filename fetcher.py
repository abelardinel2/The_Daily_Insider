# fetcher.py
# SEC EDGAR filing fetcher with OpenBB, RSS, API fallback, and proxy support

import time
import logging
import requests
from requests.exceptions import RequestException
import xml.etree.ElementTree as ET
from openbb import obb
from config import COMPANY_NAME, SEC_EMAIL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, RSS_URL, API_URL, USER_AGENT, SUMMARY_LABEL, OPENBB_LOG_COLLECT, PROXY_ENABLED, PROXY, SCRAPINGBEE_API_KEY, SCRAPINGBEE_URL

# Configure logging
logging.basicConfig(
    filename="edgar_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure OpenBB
obb.user.preferences.log_collect = OPENBB_LOG_COLLECT
obb.user.credentials.user_agent = USER_AGENT

# Headers for SEC compliance
headers =

System: {
    "User-Agent": USER_AGENT,
    "Accept": "application/xml,application/json,text/html",
    "Accept-Encoding": "gzip, deflate"
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
    """Fetch URL with rate limiting (100ms delay) and proxy support."""
    time.sleep(0.1)  # 100ms delay to stay under 10 requests/second
    try:
        if PROXY_ENABLED:
            if SCRAPINGBEE_API_KEY:
                # Use ScrapingBee proxy service
                proxy_url = SCRAPINGBEE_URL.format(SCRAPINGBEE_API_KEY, requests.utils.quote(url))
                response = requests.get(proxy_url, headers=headers, timeout=10)
            else:
                # Use standard proxy
                response = requests.get(url, headers=headers, proxies=PROXY, timeout=10)
        else:
            # No proxy
            response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except RequestException as e:
        raise

def fetch_with_retry(url, max_retries=3):
    """Fetch URL with retry logic and exponential backoff."""
    for attempt in range(max_retries):
        try:
            return fetch_with_rate_limit(url)
        except RequestException as e:
            error_msg = f"Attempt {attempt + 1} failed for {url}: {str(e)}"
            logging.error(error_msg)
            if hasattr(e, 'response') and e.response.status_code == 403:
                send_telegram_message(f"403 Forbidden: {url}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Backoff: 1s, 2s, 4s
            else:
                send_telegram_message(f"Failed to fetch {url} after {max_retries} attempts")
                raise Exception(error_msg)

def fetch_openbb_filings(cik, form_type="4"):
    """Fetch filings using OpenBB for a given CIK and form type."""
    try:
        filings = obb.regulators.sec.filings(cik=cik, form_type=form_type).to_dict()
        if filings:
            print(f"{SUMMARY_LABEL} Successfully fetched {len(filings.get('filings', []))} filings for CIK {cik} via OpenBB")
            return filings
        else:
            error_msg = f"No filings found for CIK {cik} via OpenBB"
            logging.warning(error_msg)
            send_telegram_message(error_msg)
            return None
    except Exception as e:
        error_msg = f"OpenBB failed for CIK {cik}: {str(e)}"
        logging.error(error_msg)
        send_telegram_message(error_msg)
        return None

def fetch_api_filings(cik):
    """Fetch filings using SEC API as a fallback."""
    try:
        url = API_URL.format(cik.zfill(10))
        response = fetch_with_retry(url)
        data = response.json()
        print(f"{SUMMARY_LABEL} Successfully fetched API data for CIK {cik}")
        return data
    except Exception as e:
        error_msg = f"SEC API failed for CIK {cik}: {str(e)}"
        logging.error(error_msg)
        send_telegram_message(error_msg)
        return None

def parse_rss_feed():
    """Parse SEC EDGAR RSS feed as a fallback."""
    try:
        rss_response = fetch_with_retry(RSS_URL)
        root = ET.fromstring(rss_response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        filings = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text
            link = entry.find("atom:link", ns).attrib["href"]
            if "/Archives/edgar/data" in link:  # Respect robots.txt
                try:
                    filing_response = fetch_with_retry(link)
                    filings.append({
                        "title": title,
                        "url": link,
                        "content": filing_response.text
                    })
                    print(f"{SUMMARY_LABEL} Processed RSS filing: {title} - {link}")
                except Exception as e:
                    error_msg = f"Failed to process RSS filing {link}: {str(e)}"
                    logging.error(error_msg)
                    send_telegram_message(error_msg)
        return filings
    except Exception as e:
        error_msg = f"Failed to parse RSS feed: {str(e)}"
        logging.error(error_msg)
        send_telegram_message(error_msg)
        return []

def main():
    """Main function to run the fetcher."""
    print(f"{SUMMARY_LABEL} SEC EDGAR Fetcher started by {COMPANY_NAME} at {time.ctime()}")
    
    # Example CIKs from your data
    ciks = ["0000003545", "0000005272"]  # ALICO, INC. and AMERICAN INTERNATIONAL GROUP, INC.
    all_filings = []

    # Try OpenBB first
    for cik in ciks:
        filings = fetch_openbb_filings(cik)
        if filings:
            all_filings.append({"cik": cik, "source": "OpenBB", "data": filings})
        else:
            # Fallback to SEC API
            print(f"{SUMMARY_LABEL} Falling back to SEC API for CIK {cik}")
            api_filings = fetch_api_filings(cik)
            if api_filings:
                all_filings.append({"cik": cik, "source": "API", "data": api_filings})

    # Fallback to RSS feed if no filings retrieved
    if not all_filings:
        print(f"{SUMMARY_LABEL} Falling back to RSS feed")
        rss_filings = parse_rss_feed()
        if rss_filings:
            all_filings.append({"source": "RSS", "data": rss_filings})

    # Summarize results
    if all_filings:
        print(f"{SUMMARY_LABEL} Processed {len(all_filings)} filing sets")
        for filing_set in all_filings:
            source = filing_set["source"]
            if source == "RSS":
                for filing in filing_set["data"]:
                    print(f"Source: {source}, Title: {filing['title']}, URL: {filing['url']}")
            else:
                cik = filing_set["cik"]
                print(f"Source: {source}, CIK: {cik}, Filings: {len(filing_set['data'].get('filings', []))}")
    else:
        error_msg = "No filings processed"
        print(f"{SUMMARY_LABEL} {error_msg}")
        send_telegram_message(error_msg)

if __name__ == "__main__":
    main()