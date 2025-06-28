import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

SEC_BASE_URL = "https://data.sec.gov"

def parse_form4_amount(ticker: str, email: str) -> dict:
    headers = {"User-Agent": f"{email} (InsiderFlowBot)"}

    cik_lookup = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
    cik = None
    for _, v in cik_lookup.items():
        if v['ticker'].upper() == ticker.upper():
            cik = str(v['cik_str']).zfill(10)
            break
    if not cik:
        raise ValueError(f"CIK not found for {ticker}")

    submissions = requests.get(f"{SEC_BASE_URL}/submissions/CIK{cik}.json", headers=headers).json()
    accessions = submissions['filings']['recent']['accessionNumber'][:5]

    buys = 0
    sells = 0

    cutoff = datetime.now() - timedelta(days=5)

    for acc in accessions:
        acc_clean = acc.replace("-", "")
        url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc_clean}/xslF345X03/{acc}.xml"

        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "xml")
        trans_dates = soup.find_all("transactionDate")
        codes = soup.find_all("transactionAcquiredDisposedCode")

        for date_tag, code_tag in zip(trans_dates, codes):
            t_date = datetime.strptime(date_tag.text, "%Y-%m-%d")
            if t_date >= cutoff:
                if code_tag.text == "A":
                    buys += 1_000_000
                elif code_tag.text == "D":
                    sells += 1_000_000

    return {"buys": buys, "sells": sells}