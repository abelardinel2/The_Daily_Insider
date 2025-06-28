import requests
import os
import json
from datetime import datetime, timedelta
from parse_form4 import parse_form4_xml

SEC_DAILY_INDEX = "https://www.sec.gov/Archives/edgar/daily-index"

def fetch_full_daily():
    days = 1  # Adjust range if you want multiple days
    end = datetime.today()
    start = end - timedelta(days=days)
    total_buys = 0
    total_sells = 0

    for i in range(days):
        day = (end - timedelta(days=i)).strftime("%Y%m%d")
        # Example daily master index (adjust as needed)
        index_url = f"{SEC_DAILY_INDEX}/2025/QTR2/master.{day}.idx"
        resp = requests.get(index_url, headers={"User-Agent": f"{os.getenv('SEC_EMAIL')} (OriaDawnBot)"})
        if resp.status_code != 200:
            continue
        for line in resp.text.splitlines():
            if "|4|" in line:
                parts = line.split("|")
                if len(parts) >= 5:
                    path = parts[-1].strip()
                    xml_url = f"https://www.sec.gov/Archives/{path.replace('.txt', '.xml')}"
                    result = parse_form4_xml(xml_url)
                    total_buys += result["buys"]
                    total_sells += result["sells"]

    snapshot = {
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }

    with open("insider_flow.json", "w") as f:
        json.dump(snapshot, f, indent=2)

    print("✅ Daily index fetch done!")

if __name__ == "__main__":
    fetch_full_daily()