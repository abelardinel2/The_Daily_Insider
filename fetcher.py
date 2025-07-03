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
        print(f"Fetched RSS from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} at {datetime.now()}: {response.text[:500]}...")
        root = ET.fromstring(response.content)
        trades = {"tickers": {}, "last_updated": datetime.utcnow().isoformat() + "Z"}
        analyzer_trades = {"total_buys": 0.0, "total_sells": 0.0, "top_buys": 0.0, "top_sells": 0.0}

        for item in root.findall('{http://www.w3.org/2005/Atom}entry'):
            try:
                # Safely extract elements
                title_elem = item.find('{http://www.w3.org/2005/Atom}title')
                summary_elem = item.find('{http://www.w3.org/2005/Atom}summary')
                link_elem = item.find('{http://www.w3.org/2005/Atom}link')

                if title_elem is None or link_elem is None:
                    print(f"❌ Skipped entry: Missing title or link")
                    continue

                title = title_elem.text if title_elem.text else ""
                link = link_elem.get('href') if link_elem.get('href') else ""
                
                if not title or not link:
                    print(f"❌ Skipped entry: Empty title or link - Title: {title}, Link: {link}")
                    continue

                print(f"✅ Processing: {title} - Link: {link}")
                
                # Extract ticker using regex
                ticker_match = re.search(r'[A-Z]{1,5}', title)
                ticker = ticker_match.group(0) if ticker_match else "UNKNOWN"
                if ticker not in trades["tickers"]:
                    trades["tickers"][ticker] = {"buys": 0, "sells": 0, "alerts": []}

                # Parse the Form 4 XML
                form4_data = parse_form4_xml(link)
                if not isinstance(form4_data, dict) or "buys" not in form4_data or "sells" not in form4_data:
                    print(f"❌ Invalid form4_data from {link}")
                    continue

                trades["tickers"][ticker]["buys"] += form4_data["buys"]
                trades["tickers"][ticker]["sells"] += form4_data["sells"]
                if form4_data["buys"] > 0 or form4_data["sells"] > 0:
                    trades["tickers"][ticker]["alerts"].append({
                        "link": link,
                        "date": datetime.utcnow().isoformat().split("T")[0],
                        "type": "Buy" if form4_data["buys"] > 0 else "Sell",
                        "amount_buys": form4_data["buys"],
                        "amount_sells": form4_data["sells"]
                    })

                # Aggregate for Analyzer
                analyzer_trades["total_buys"] += form4_data["buys"]
                analyzer_trades["total_sells"] += form4_data["sells"]
                analyzer_trades["top_buys"] += form4_data["buys"] * 100  # Placeholder price multiplier
                analyzer_trades["top_sells"] += form4_data["sells"] * 100  # Placeholder price multiplier

            except Exception as e:
                print(f"❌ Skipped invalid entry: {str(e)}")

        print(f"Trade summary: {trades}")
        with open("insider_flow.json", "w") as f:
            json.dump(trades, f, indent=4)
        with open("insider_flow_analyzer.json", "w") as f:
            json.dump(analyzer_trades, f, indent=4)
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - Fetch completed: {trades}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        with open("insider_flow.json", "w") as f:
            json.dump({"tickers": {}, "last_updated": datetime.utcnow().isoformat() + "Z"}, f, indent=4)
        with open("insider_flow_analyzer.json", "w") as f:
            json.dump({"total_buys": 0.0, "total_sells": 0.0, "top_buys": 0.0, "top_sells": 0.0}, f, indent=4)
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - Fetch failed: {e}\n")

    except ET.ParseError as e:
        print(f"Error parsing SEC RSS feed: {e}")
        with open("insider_flow.json", "w") as f:
            json.dump({"tickers": {}, "last_updated": datetime.utcnow().isoformat() + "Z"}, f, indent=4)
        with open("insider_flow_analyzer.json", "w") as f:
            json.dump({"total_buys": 0.0, "total_sells": 0.0, "top_buys": 0.0, "top_sells": 0.0}, f, indent=4)
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - Parse error: {e}\n")

if __name__ == "__main__":
    fetch_and_update_insider_flow()