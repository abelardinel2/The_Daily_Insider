import requests
from datetime import datetime

SEC_BASE_URL = "https://data.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str, start_date: str, end_date: str) -> dict:
    headers = {"User-Agent": f"{email} (InsiderFlowBot)"}
    cik_lookup = requests.get(
        f"https://www.sec.gov/files/company_tickers.json", headers=headers
    ).json()

    cik = None
    for k, v in cik_lookup.items():
        if v['ticker'].upper() == ticker.upper():
            cik = str(v['cik_str']).zfill(10)
            break

    if not cik:
        return {"buys": 0, "sells": 0}

    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json", headers=headers
    ).json()

    buys = 0
    sells = 0

    for i, form in enumerate(submissions['filings']['recent']['form']):
        if form != "4":
            continue

        filed_date = submissions['filings']['recent']['filingDate'][i]
        if not (start_date <= filed_date <= end_date):
            continue

        doc_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{submissions['filings']['recent']['accessionNumber'][i].replace('-', '')}/xslF345X03/{submissions['filings']['recent']['accessionNumber'][i]}.xml"
        resp = requests.get(doc_url, headers=headers)
        if resp.status_code != 200:
            continue

        xml = resp.text
        if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml:
            buys += 1
        if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml:
            sells += 1

    return {"buys": buys, "sells": sells}