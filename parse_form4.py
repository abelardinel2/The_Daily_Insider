import requests

SEC_BASE_URL = "https://data.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str, target_date: str) -> dict:
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)"
    }

    # Map ticker to CIK
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

    # Get recent submissions
    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json",
        headers=headers
    ).json()

    recent = submissions['filings']['recent']
    buys, sells = 0, 0

    for idx, form in enumerate(recent['form']):
        if form != "4":
            continue
        if recent['filingDate'][idx] != target_date:
            continue

        acc_num = recent['accessionNumber'][idx]
        acc_num_clean = acc_num.replace("-", "")
        doc_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_num_clean}/xslF345X03/{acc_num}.xml"

        resp = requests.get(doc_url, headers=headers)
        if resp.status_code != 200:
            continue

        xml = resp.text
        if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml:
            buys += 1
        if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml:
            sells += 1

    return {"buys": buys, "sells": sells}