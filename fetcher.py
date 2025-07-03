import os
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
import re

def parse_form4_xml(url: str) -> dict:
    try:
        # Fetch the Form 4 XML
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return {"buys": 0, "sells": 0}

    try:
        # Parse the XML with BeautifulSoup
        soup = BeautifulSoup(resp.text, "xml")
        buys = 0
        sells = 0

        # Find all non-derivative transactions
        for txn in soup.find_all("nonDerivativeTransaction"):
            code = txn.find("transactionCode")
            acquired_or_disposed = txn.find("transactionAcquiredDisposedCode")
            amount_node = txn.find("transactionShares")

            if not all([code, acquired_or_disposed, amount_node]):
                print(f"❌ Skipping transaction in {url}: Missing data")
                continue

            code_value = code.text.strip() if code.text else ""
            acquired_value = acquired_or_disposed.text.strip() if acquired_or_disposed.text else ""
            amount_value = amount_node.find("value")
            amount_str = amount_value.text.strip() if amount_value and amount_value.text else "0"
            amount = float(amount_str) if amount_str else 0.0

            print(f"Transaction: Code={code_value}, Acquired/Disposed={acquired_value}, Amount={amount}")

            # Classify as buy or sell
            if code_value == "P" or acquired_value == "A":  # Purchase or Acquired
                buys += amount
            elif code_value == "S" or acquired_value == "D":  # Sale or Disposed
                sells += amount

        print(f"Parsed {url}: Buys={buys}, Sells={sells}")
        return {"buys": buys, "sells": sells}
    except Exception as e:
        print(f"❌ Error parsing {url}: {e}")
        return {"buys": 0, "sells": 0}

def fetch_and_update_insider_flow():
    # Set date range (e.g., last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    date_format = "%Y%m%d"
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&dateb={start_date.strftime(date_format)}&datea={end_date.strftime(date_format)}&type=4&owner=include&output=atom"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 (your.email@example.com)",  # Replace with your email
        "Accept": "application/xml"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Fetched RSS from {start_date.strftime('%