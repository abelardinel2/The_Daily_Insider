import os
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

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
                title = item.find('{http://www.w3.org/2005/Atom}title').text
                summary = item.find('{http://www.w3.org/2005/Atom}summary').text
                link = item.find('{http://www.w3.org/2005/Atom}link')['href']
                print(f"Processing link: {link}")
                # Extract ticker from title or summary (simplified heuristic)
                import re
                ticker_match = re.search(r'[A-Z]{1,5}', title)
                ticker = ticker_match.group(0) if ticker_match else "UNKNOWN"
                if ticker not in trades["tickers"]:
                    trades["tickers"][ticker] = {"buys": 0, "sells": 0, "alerts": []}
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
                    # Aggregate for Analyzer
                    analyzer_trades["total_buys"] += form4_data["buys"]
                    analyzer_trades["total_sells"] += form4_data["sells"]
                    # Placeholder dollar conversion for "top" (refine with real prices)
                    analyzer_trades["top_buys"] += form4_data["buys"] * 100  # Adjust price as needed
                    analyzer_trades["top_sells"] += form4_data["sells"] * 100  # Adjust price as needed
                except Exception as e:
                    print(f"Error parsing {link} for {ticker}: {e}")
            except Exception as e:
                print(f"❌ Skipped invalid entry: {e}")
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