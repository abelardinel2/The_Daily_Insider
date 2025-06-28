import requests
import xml.etree.ElementTree as ET

SEC_BASE_URL = "https://data.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str) -> dict:
    """
    Fetch recent Form 4 filings for a ticker using SEC EDGAR,
    parse XML directly to sum Buys and Sells.
    """
    headers = {
        "User-Agent": f"OriaDawnBot/1.0 (Researcher contact: {email})"
    }

    # 1. Get CIK mapping
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

    # 2. Get recent submissions
    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json",
        headers=headers
    ).json()

    # 3. Filter for Form 4s
    accession_numbers = [
        acc for form, acc in zip(
            submissions['filings']['recent']['form'],
            submissions['filings']['recent']['accessionNumber']
        ) if form == '4'
    ][:5]  # Limit to last 5

    amounts = {"buys": 0, "sells": 0}

    for acc_num in accession_numbers:
        acc_clean = acc_num.replace("-", "")
        xml_url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_clean}/xslF345X03/{acc_num}.xml"
        resp = requests.get(xml_url, headers=headers)
        if resp.status_code != 200:
            continue

        try:
            root = ET.fromstring(resp.text)
        except ET.ParseError:
            continue

        for txn in root.iter("{http://www.sec.gov/edgar/document/thirteenf/informationtable}nonDerivativeTransaction"):
            code = txn.find(".//transactionAcquiredDisposedCode/value").text
            shares = txn.find(".//transactionShares/value").text
            if shares:
                shares = float(shares)
                if code == "A":
                    amounts["buys"] += shares
                elif code == "D":
                    amounts["sells"] += shares

    return amounts