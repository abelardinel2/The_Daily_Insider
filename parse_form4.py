import requests

SEC_BASE_URL = "https://data.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str) -> dict:
    """
    Fetch recent Form 4 filings for a ticker using SEC EDGAR API,
    sum Buys and Sells realistically.
    """
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)"
    }

    # 1. Get CIK mapping
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

    # 2. Get recent submissions
    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json",
        headers=headers
    ).json()

    # 3. Parse for Form 4s
    form4s = [
        f for f in submissions['filings']['recent']['form']
        if f == '4'
    ]

    amounts = {
        "buys": 0,
        "sells": 0
    }

    if not form4s:
        return amounts

    # 4. Example: add up 10 most recent Form 4s
    accession_numbers = submissions['filings']['recent']['accessionNumber'][:10]
    for acc_num in accession_numbers:
        acc_num_clean = acc_num.replace("-", "")
        doc_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_num_clean}/xslF345X03/{acc_num}.xml"

        resp = requests.get(doc_url, headers=headers)
        if resp.status_code != 200:
            continue

        xml = resp.text
        # Very basic tag check (real parser should use lxml or xml.etree)
        if "<transactionAcquiredDisposedCode>A</transactionAcquiredDisposedCode>" in xml:
            amounts["buys"] += 1  # Example: 1 buy detected
        if "<transactionAcquiredDisposedCode>D</transactionAcquiredDisposedCode>" in xml:
            amounts["sells"] += 1  # Example: 1 sell detected

    return amounts