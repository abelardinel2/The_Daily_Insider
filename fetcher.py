import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

SEC_BASE = "https://www.sec.gov"
HEADERS = {
    "User-Agent": f"{os.getenv('SEC_EMAIL')} OriaDawnBot"
}

def get_cik(ticker):
    res = requests.get("https://www.sec.gov/files/company_tickers.json", headers=HEADERS)
    mapping = res.json()
    for entry in mapping.values():
        if entry['ticker'].upper() == ticker.upper():
            return str(entry['cik_str']).zfill(10)
    return None

def parse_form4(cik):
    url = f"{SEC_BASE}/submissions/CIK{cik}.json"
    res = requests.get(url, headers=HEADERS).json()
    data = {"buys": 0, "sells": 0}
    recent = res['filings']['recent']
    for idx, form in enumerate(recent['form']):
        if form != "4":
            continue
        accession = recent['accessionNumber'][idx].replace("-", "")
        xml_url = f"{SEC_BASE}/Archives/edgar/data/{int(cik)}/{accession}/xslF345X03/primary_doc.xml"
        xml = requests.get(xml_url, headers=HEADERS)
        if xml.status_code != 200:
            continue
        soup = BeautifulSoup(xml.text, "xml")
        for code in soup.find_all("transactionAcquiredDisposedCode"):
            if code.text == "A":
                data["buys"] += 1
            elif code.text == "D":
                data["sells"] += 1
    return data

def main():
    tickers = []
    with open("tickers.txt") as f:
        tickers = [line.strip() for line in f]

    results = {}
    for t in tickers:
        cik = get_cik(t)
        if not cik:
            continue
        amounts = parse_form4(cik)
        results[t] = amounts

    with open("insider_flow.json", "w") as out:
        json.dump(results, out, indent=2)

if __name__ == "__main__":
    main()
