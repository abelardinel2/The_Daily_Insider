import requests
from datetime import datetime, timedelta

SEC_BASE_URL = "https://data.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str, days_back: int) -> dict:
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)"
    }

    cik_lookup = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=headers
    ).json()

    cik = None
    for k, v in cik_lookup.items():
        if v['ticker'].upper() == ticker.upper():
            cik = str(v['cik_str']).zfill(10)
            break

    if not cik:
        raise ValueError(f"Could not find CIK for ticker: {ticker}")

    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json",
        headers=headers
    ).json()

    accession_numbers = submissions['filings']['recent']['accessionNumber']

    cutoff = datetime.today() - timedelta(days=days_back)

    amounts = {"buys": 0, "sells": 0}

    for acc_num in accession_numbers:
        acc_clean = acc_num.replace("-", "")
        doc_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_clean}/xslF345X03/{acc_num}.xml"

        resp = requests.get(doc_url, headers=headers)
        if resp.status_code != 200:
            continue

        xml = resp.text

        if "<transactionDate>" not in xml:
            continue

        try:
            tx_date = xml.split("<transactionDate>")[1].split("</transactionDate>")[0].strip()
            tx_date_obj = datetime.strptime(tx_date, "%Y-%m-%d")
            if tx_date_obj < cutoff:
                continue
        except:
            continue

        # Match 'A' or 'P' for buy, 'D' or 'S' for sell — more flexible
        if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml \
           or "<transactionAcquiredDisposedCode>P</transactionAcquiredDisposedCode>" in xml:
            amounts["buys"] += 1

        if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml \
           or "<transactionAcquiredDisposedCode>S</transactionAcquiredDisposedCode>" in xml:
            amounts["sells"] += 1

    return amounts