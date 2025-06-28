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

    # Get ALL company tickers and CIKs
    tickers_url = f"{SEC_BASE}/files/company_tickers.json"
    company_index = requests.get(tickers_url, headers=headers).json()

    for entry in company_index.values():
        cik = str(entry['cik_str']).zfill(10)
        sub_url = f"{SEC_BASE}/submissions/CIK{cik}.json"
        resp = requests.get(sub_url, headers=headers)
        if resp.status_code != 200:
            continue

        recent = resp.json().get("filings", {}).get("recent", {})
        accession_numbers = recent.get("accessionNumber", [])
        filing_dates = recent.get("filingDate", [])
        form_types = recent.get("form", [])

        for idx, form in enumerate(form_types):
            if form != "4":
                continue

            filing_date = filing_dates[idx]
            filed_dt = datetime.strptime(filing_date, "%Y-%m-%d")
            if not (start_date <= filed_dt <= end_date):
                continue

            acc_num = accession_numbers[idx].replace("-", "")
            xml_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_num}.xml"

            try:
                result = parse_form4_xml(xml_url)
                total_buys += result["buys"]
                total_sells += result["sells"]
            except Exception as e:
                print(f"Failed parsing {xml_url}: {e}")
                continue

    data = {
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }

    with open("insider_flow.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ insider_flow.json updated!")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    fetch_all_form4s()