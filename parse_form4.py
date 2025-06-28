import requests
from datetime import datetime, timedelta

SEC_BASE_URL = "https://data.sec.gov"
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def get_recent_form4_amounts(ticker: str, email: str) -> dict:
    headers = {"User-Agent": f"{email} (InsiderFlowBot)"}
    cik_lookup = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()

    cik = None
    for _, v in cik_lookup.items():
        if v['ticker'].upper() == ticker.upper():
            cik = str(v['cik_str']).zfill(10)
            break
    if not cik:
        raise ValueError(f"Could not find CIK for ticker: {ticker}")

    submissions = requests.get(f"{SEC_BASE_URL}/submissions/CIK{cik}.json", headers=headers).json()

    amounts = {"buys": 0, "sells": 0}
    acc_nums = submissions['filings']['recent']['accessionNumber']
    dates = submissions['filings']['recent']['filingDate']

    for i, acc_num in enumerate(acc_nums):
        if dates[i] != YESTERDAY:
            continue
        acc_clean = acc_num.replace("-", "")
        url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_clean}/xslF345X03/{acc_num}.xml"

        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            continue

        xml = resp.text
        if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml:
            amounts["buys"] += 1
        if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml:
            amounts["sells"] += 1

    return amounts