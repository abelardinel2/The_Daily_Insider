import os
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

# Define WATCHLIST
WATCHLIST = [
    "PFE", "QUBT", "WMT", "JNJ", "COST", "PEP", "XOM", "AGI", "HL", "SILJ", "GLD", "IAU", "BAR", "SLV", "WPM",
    "AG", "B", "XAGUSD", "COIN", "JPM", "IREN", "FPI", "LAND", "WELL", "PSA", "O", "SMCI", "NVDA", "IONQ",
    "RGTI", "ARKQ", "AIQ", "TEM", "PLTR", "USO", "XOP", "PHO", "FIW", "XYL", "AWK", "WTRG", "UFO", "RKLB",
    "ASTS", "BTCUSD", "ETHUSD", "XRPUSD", "SUIUSD", "KYMR", "DHR", "RELIANCE"
]

def fetch_and_update_insider_flow():
    url = "https://www.sec.gov/cgi-bin/current_q?i=csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 (your.email@example.com)",  # Replace with your email
        "Accept": "application/xml"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Fetched RSS at {datetime.now()}: {response.text[:500]}...")
        root = ET.fromstring(response.content)
        trades = {"tickers": {ticker: {"buys": 0, "sells": 0, "alerts": []} for ticker in WATCHLIST}, "last_updated": datetime.utcnow().isoformat() + "Z"}
        for item in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = item.find('{http://www.w3.org/2005/Atom}title').text
            summary = item.find('{http://www.w3.org/2005/Atom}summary').text
            link = item.find('{http://www.w3.org/2005/Atom}link')['href']
            print(f"Processing link: {link}")
            for ticker in WATCHLIST:
                if ticker in title.upper() or ticker in summary.upper():
                    try:
                        form4_data = parse_form4_xml(link)
                        if not isinstance(form4_data, dict) or "buys" not in form4_data or "sells" not in form4_data:
                            raise ValueError("Invalid form4_data format")
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
                    except Exception as e:
                        print(f"Error parsing {link} for {ticker}: {e}")
        print(f"Trade summary: {trades}")
        with open("insider_flow.json", "w") as f:
            json.dump(trades, f, indent=4)
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - Fetch completed: {trades}\n")
    except requests.exceptions.RequestException as e:  # Corrected to RequestException
        print(f"Error fetching data: {e}")
        with open("insider_flow.json", "w") as f:
            json.dump({"tickers": {ticker: {"buys": 0, "sells": 0, "alerts": []} for ticker in WATCHLIST}, "last_updated": datetime.utcnow().isoformat() + "Z"}, f, indent=4)
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - Fetch failed: {e}\n")
    except ET.ParseError:
        print("Error parsing SEC RSS feed")
        with open("insider_flow.json", "w") as f:
            json.dump({"tickers": {ticker: {"buys": 0, "sells": 0, "alerts": []} for ticker in WATCHLIST}, "last_updated": datetime.utcnow().isoformat() + "Z"}, f, indent=4)
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - Parse error\n")

if __name__ == "__main__":
    fetch_and_update_insider_flow()