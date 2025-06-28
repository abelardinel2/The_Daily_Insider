import requests
import os
from datetime import datetime, timedelta
from parse_form4 import parse_form4_xml
import json

SEC_BASE = "https://data.sec.gov"
headers = {"User-Agent": f"{os.getenv('SEC_EMAIL')} (Insider Flow Analyzer)"}

def fetch_all_form4s(days=1):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    total_buys = 0
    total_sells = 0

    # ✅ Use multiple CIKs!
    CIK_LIST = [
        "0000320193",  # Apple
        "0000789019",  # Microsoft
        "0001652044"   # Alphabet
    ]

    for cik in CIK_LIST:
        company_index = requests.get(f"{SEC_BASE}/submissions/CIK{cik}.json", headers=headers).json()
        for idx, entry in enumerate(company_index["filings"]["recent"]["accessionNumber"]):
            acc_num = entry.replace("-", "")
            filing_date = company_index["filings"]["recent"]["filingDate"][idx]
            filed_dt = datetime.strptime(filing_date, "%Y-%m-%d")

            if not (start_date <= filed_dt <= end_date):
                continue

            xml_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_num}.xml"
            result = parse_form4_xml(xml_url)
            total_buys += result["buys"]
            total_sells += result["sells"]

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
    fetch_all_form4s()