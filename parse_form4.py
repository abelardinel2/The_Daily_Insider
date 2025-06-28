import requests

SEC_BASE_URL = "https://data.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str) -> dict:
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)"
    }

    # CIK lookup
    cik_lookup = requests.get(
        f"https://www.sec.gov/files/company_tickers.json",
        headers=headers
    ).json()

    cik = None
    for _, v in cik_lookup.items():
        if v['ticker'].upper() == ticker.upper():
            cik = str(v['cik_str']).zfill(10)
            break

    if not cik:
        print(f"⚠️ No CIK for {ticker}")
        return {"buys": 0, "sells": 0}

    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json",
        headers=headers
    ).json()

    form4s = [
        f for f in submissions['filings']['recent']['form']
        if f == '4'
    ]

    amounts = {"buys": 0, "sells": 0}

    accession_numbers = submissions['filings']['recent']['accessionNumber'][:10]
    for acc_num in accession_numbers:
        acc_clean = acc_num.replace("-", "")
        doc_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_clean}/xslF345X03/{acc_num}.xml"

        resp = requests.get(doc_url, headers=headers)
        if resp.status_code != 200:
            continue

        xml = resp.text
        if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml:
            amounts["buys"] += 1
        if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml:
            amounts["sells"] += 1

    return amounts