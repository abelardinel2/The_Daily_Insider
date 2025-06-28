import requests
from bs4 import BeautifulSoup

def get_recent_form4_amounts(ticker: str, email: str, start_date: str, end_date: str) -> dict:
    url = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"
    headers = {"User-Agent": f"{email} (InsiderFlowBot)"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Failed: {resp.status_code}")
    soup = BeautifulSoup(resp.text, "xml")

    buys = len(soup.find_all("transactionAcquiredDisposedCode", string="A"))
    sells = len(soup.find_all("transactionAcquiredDisposedCode", string="D"))

    return {"buys": buys, "sells": sells}