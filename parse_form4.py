import requests
from bs4 import BeautifulSoup

SEC_BASE_URL = "https://www.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str) -> dict:
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov",
        "Referer": "https://www.sec.gov"
    }

    # 1️⃣ Get CIK
    cik_lookup = requests.get(
        f"https://www.sec.gov/files/company_tickers.json",
        headers=headers
    ).json()

    cik = None
    for k, v in cik_lookup.items():
        if v['ticker'].upper() == ticker.upper():
            cik = str(v['cik_str']).zfill(10)
            break

    if not cik:
        raise ValueError(f"Could not find CIK for ticker: {ticker}")

    # 2️⃣ Get recent submissions
    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json",
        headers=headers
    ).json()

    accession_numbers = submissions['filings']['recent']['accessionNumber'][:5]

    amounts = {"buys": 0, "sells": 0}

    for acc_num in accession_numbers:
        acc_num_clean = acc_num.replace("-", "")
        index_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_num_clean}/index.json"

        index_resp = requests.get(index_url, headers=headers)
        if index_resp.status_code != 200:
            continue

        index_json = index_resp.json()
        doc_name = None

        for f in index_json['directory']['item']:
            if f['name'].endswith('.xml'):
                doc_name = f['name']
                break

        if not doc_name:
            continue

        xml_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_num_clean}/{doc_name}"
        resp = requests.get(xml_url, headers=headers)
        if resp.status_code != 200:
            continue

        xml = resp.text

        if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml:
            amounts["buys"] += 1
        if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml:
            amounts["sells"] += 1

    return amounts