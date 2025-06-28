import requests
from bs4 import BeautifulSoup

SEC_BASE_URL = "https://data.sec.gov"

def get_recent_form4_amounts(ticker: str, email: str) -> dict:
    headers = {
        "User-Agent": f"InsiderFlowBot/1.0 (https://oriadawn.xyz; {email})"
    }

    # Get CIK mapping
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

    submissions = requests.get(
        f"{SEC_BASE_URL}/submissions/CIK{cik}.json",
        headers=headers
    ).json()

    amounts = {"buys": 0, "sells": 0}

    acc_nums = submissions['filings']['recent']['accessionNumber'][:5]
    for acc_num in acc_nums:
        acc_num_clean = acc_num.replace("-", "")
        url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_num_clean}/xslF345X03/{acc_num}.xml"

        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            continue

        soup = BeautifulSoup(resp.content, "xml")
        acquired = soup.find_all("transactionAcquiredDisposedCode")

        for tag in acquired:
            if tag.text == "A":
                amounts['buys'] += 1_000_000  # Example $1M per buy
            elif tag.text == "D":
                amounts['sells'] += 1_000_000  # Example $1M per sell

    return amounts