import requests
import os
from datetime import datetime, timedelta
import json
import time
from parse import parse_form4_xml  # Import the parsing function

SEC_BASE = "https://www.sec.gov/Archives/edgar/"
headers = {"User-Agent": f"{os.getenv('SEC_EMAIL')}"}

def fetch_all_forms(days=5):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    
    total_buys = 0
    total_sells = 0
    
    index_url = f"{SEC_BASE}daily-index/{end_date.strftime('%Y%m%d')}/master.idx"
    response = requests.get(index_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch index: {index_url}, {response.status_code}")
        index_url = f"{SEC_BASE}daily-index/{end_date.strftime('%Y%m')}/master.idx"
        response = requests.get(index_url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to fetch monthly index: {index_url}, {response.status_code}")
            return
    
    lines = response.text.splitlines()
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 5 and ("4" in parts[2] or "144" in parts[2]):
            cik = parts[0]
            acc_num = parts[4].replace("-", "")
            filing_date = parts[3]
            filed_dt = datetime.strptime(filing_date, "%Y-%m-%d")
            if start_date <= filed_dt <= end_date:
                if "4" in parts[2]:
                    xml_url = f"{SEC_BASE}edgar/data/{cik}/{acc_num}/xslF345X05/primary_doc.xml"
                elif "144" in parts[2]:
                    xml_url = f"{SEC_BASE}edgar/data/{cik}/{acc_num}/xsl144X01/primary_doc.xml"
                try:
                    result = parse_form4_xml(xml_url)
                    print(f"✅ {xml_url} -> {result}")
                    total_buys += result["buys"]
                    total_sells += result["sells"]
                except Exception as e:
                    print(f"❌ Error parsing {xml_url}: {e}")
                time.sleep(0.1)  # Respect SEC rate limits
    
    data = {
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }
    
    with open("insider_flow.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ insider_flow.json updated!")

if __name__ == "__main__":
    fetch_all_forms()