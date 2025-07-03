import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
from parse_form4 import parse_form4_xml

# Define assets
OWNED_ITEMS = {'PFE', 'QUBT', 'RGTI', 'SILJ', 'SMCI', 'USO', 'VEGI', 'NBIS', 'AGI', 'B', 'BAR', 'BTCI', 'CETH', 'DHR', 'ENPH', 'FPI', 'HL', 'IONQ', 'JNJ', 'LAND', 'MRNA'}
TARGET_ITEMS = {'WMT', 'COST', 'PEP', 'XOM', 'WELL', 'O', 'PSA', 'GLD', 'IAU', 'XAG', 'SLV', 'AEG', 'AG', 'WPM', 'BTCUSD', 'XRPUSD', 'ETHUSD', 'SUIUSD', 'PLTR', 'ARKQ', 'NVDA', 'AIQ', 'TEM', 'RKLB', 'ASTS', 'UFO', 'TSLA', 'RELIANCE', 'SPY', 'XLP', 'PHO', 'FIW', 'CGW', 'VEOEY', 'XYL', 'WTRG', 'AWK', 'XOP'}
WATCHLIST = OWNED_ITEMS.union(TARGET_ITEMS)

def fetch_and_update_insider_flow():
    url = "https://www.sec.gov/cgi-bin/current_q?i=csv"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Fetched data at {datetime.now()}")
        root = ET.fromstring(response.content)
        trades = {
            "top_buys": 0,
            "top_sells": 0,
            "total_buys": 0,
            "total_sells": 0
        }
        for item in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = item.find('{http://www.w3.org/2005/Atom}title').text
            summary = item.find('{http://www.w3.org/2005/Atom}summary').text
            link = item.find('{http://www.w3.org/2005/Atom}link')['href']
            print(f"Processing link: {link}")  # Debug: Verify URLs
            for ticker in WATCHLIST:
                if ticker in title or ticker in summary:
                    try:
                        form4_data = parse_form4_xml(link)
                        trades["total_buys"] += form4_data["buys"]
                        trades["total_sells"] += form4_data["sells"]
                        # "Top" could be based on owned/targeted significance; for now, mirror totals
                        trades["top_buys"] += form4_data["buys"]
                        trades["top_sells"] += form4_data["sells"]
                    except Exception as e:
                        print(f"Error parsing {link} for {ticker}: {e}")
        print(f"Found total buys: {trades['total_buys']}, total sells: {trades['total_sells']}")
        with open("insider_flow.json", "w") as f:
            json.dump(trades, f, indent=4)
    except requests.exceptions.RequestError as e:
        print(f"Error fetching data: {e}")
        with open("insider_flow.json", "w") as f:
            json.dump({"top_buys": 0, "top_sells": 0, "total_buys": 0, "total_sells": 0}, f, indent=4)
    except ET.ParseError:
        print("Error parsing SEC RSS feed")
        with open("insider_flow.json", "w") as f:
            json.dump({"top_buys": 0, "top_sells": 0, "total_buys": 0, "total_sells": 0}, f, indent=4)

if __name__ == "__main__":
    fetch_and_update_insider_flow()
