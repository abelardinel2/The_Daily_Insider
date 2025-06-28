import requests
import os
from datetime import datetime, timedelta

SEC_BASE = "https://data.sec.gov"

def fetch_all_form4s(days=5):
    email = os.getenv("SEC_EMAIL")
    headers = {
        "User-Agent": f"{email} (Oria Dawn Analytics)"
    }

    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    buys, sells = 0, 0

    # Pull master company list
    company_index = requests.get(f"{SEC_BASE}/files/company_tickers.json", headers=headers).json()

    for entry in company_index.values():
        cik = str(entry['cik_str']).zfill(10)
        sub_url = f"{SEC_BASE}/submissions/CIK{cik}.json"
        resp = requests.get(sub_url, headers=headers)
        if resp.status_code != 200:
            continue

        filings = resp.json().get("filings", {}).get("recent", {})
        for idx, form in enumerate(filings.get("form", [])):
            if form != "4":
                continue

            filed_date = filings.get("filingDate", [])[idx]
            filed_dt = datetime.strptime(filed_date, "%Y-%m-%d")
            if not (start_date <= filed_dt <= end_date):
                continue

            acc_num = filings.get("accessionNumber", [])[idx].replace("-", "")
            url = f"{SEC_BASE}/Archives/edgar/data/{int(cik)}/{acc_num}/xslF345X03/{filings['accessionNumber'][idx]}.xml"

            doc = requests.get(url, headers=headers)
            if doc.status_code != 200:
                continue

            xml = doc.text
            if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml:
                buys += 1
            if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml:
                sells += 1

    return buys, sells