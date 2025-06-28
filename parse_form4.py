import requests
from bs4 import BeautifulSoup

SEC_BASE_URL = "https://data.sec.gov"

def parse_form4_amount(ticker, email, start_date, end_date):
    headers = {"User-Agent": f"{email} OriaDawnBot"}

    # Get CIK
    lookup = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
    cik = None
    for _, v in lookup.items():
        if v['ticker'].upper() == ticker.upper():
            cik = str(v['cik_str']).zfill(10)
            break
    if not cik:
        raise ValueError(f"No CIK for {ticker}")

    submissions = requests.get(f"{SEC_BASE_URL}/submissions/CIK{cik}.json", headers=headers).json()
    forms = submissions['filings']['recent']
    buys, sells = 0, 0

    for i, form in enumerate(forms['form']):
        if form != '4':
            continue

        filed_date = datetime.strptime(forms['filingDate'][i], "%Y-%m-%d").date()
        if not (start_date <= filed_date <= end_date):
            continue

        acc = forms['accessionNumber'][i].replace("-", "")
        url = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{acc}/xslF345X03/{forms['accessionNumber'][i]}.xml"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            continue

        soup = BeautifulSoup(resp.text, "xml")
        codes = soup.find_all("transactionAcquiredDisposedCode")
        for code in codes:
            if code.text == "A":
                buys += 1
            elif code.text == "D":
                sells += 1

    return {"buys": buys * 1_000_000, "sells": sells * 1_000_000}