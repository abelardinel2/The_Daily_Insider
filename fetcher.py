import os
import json
import requests
from datetime import datetime, timedelta
from parse import parse_form4_xml

def fetch_and_update_insider_flow():
    sec_email = os.getenv("SEC_EMAIL")
    if not sec_email:
        raise ValueError("SEC_EMAIL environment variable not set")

    headers = {"User-Agent": sec_email}
    end_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=5)

    form4_urls = []
    for offset in range(6):
        check_date = end_date - timedelta(days=offset)
        daily_url = f"https://www.sec.gov/Archives/edgar/daily-index/{check_date.strftime('%Y%m%d')}/master.idx"
        try:
            resp = requests.get(daily_url, headers=headers, timeout=10)
            resp.raise_for_status()
            lines = resp.text.splitlines()
            for line in lines:
                if not line or line.startswith("Date"):
                    continue
                parts = line.split("|")
                if len(parts) >= 5:
                    _, _, _, filename, _ = parts
                    if filename.endswith((".xml", ".XML")) and "form4" in filename.lower():
                        form4_url = f"https://www.sec.gov/Archives/edgar/data/{filename.split('/')[0]}/{filename}"
                        form4_urls.append(form4_url)
        except requests.RequestException as e:
            print(f"Failed to fetch {daily_url}: {e}")
            continue

    if not form4_urls:
        print("No Form 4/144 URLs found, check SEC access or index availability.")

    current_data = {"top_buys": 0, "top_sells": 0, "total_buys": 0, "total_sells": 0}
    try:
        with open("insider_flow.json", "r") as f:
            current_data = json.load(f)
    except FileNotFoundError:
        pass

    for url in form4_urls:
        try:
            trade_data = parse_form4_xml(url)
            current_data["total_buys"] += trade_data["buys"]
            current_data["total_sells"] += trade_data["sells"]
            current_data["top_buys"] = max(current_data["top_buys"], trade_data["buys"])
            current_data["top_sells"] = max(current_data["top_sells"], trade_data["sells"])
        except Exception as e:
            print(f"Error processing {url}: {e}")

    with open("insider_flow.json", "w") as f:
        json.dump(current_data, f, indent=2)

    print(f"Updated insider_flow.json with {len(form4_urls)} Form 4/144 filings")

if __name__ == "__main__":
    fetch_and_update_insider_flow()