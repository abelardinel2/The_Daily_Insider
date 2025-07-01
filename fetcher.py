import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "AmeliaBelardinelli (ameliabelardinelli@gmail.com)"
}

def get_latest_form4_urls(cik: str, limit: int = 5):
    # Make sure CIK is 10 digits with leading zeros
    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url} (Status: {resp.status_code})")

    data = resp.json()

    form4_filings = []
    for filing in data["filings"]["recent"]["form"]:
        if filing == "4":
            form4_filings.append(filing)

    # Get the indices of the Form 4s
    form_indexes = [i for i, f in enumerate(data["filings"]["recent"]["form"]) if f == "4"]

    urls = []
    for idx in form_indexes[:limit]:  # Limit to latest `limit` Form 4s
        accession = data["filings"]["recent"]["accessionNumber"][idx].replace("-", "")
        xml_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/xslF345X03/primary_doc.xml"
        urls.append(xml_url)

    return urls

def parse_form4_xml(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url} (Status: {resp.status_code})")

    soup = BeautifulSoup(resp.text, "xml")
    buys = 0
    sells = 0

    for txn in soup.find_all("nonDerivativeTransaction"):
        code = txn.transactionCode.string if txn.transactionCode else ""
        acquired_or_disposed = txn.transactionAcquiredDisposedCode.string if txn.transactionAcquiredDisposedCode else ""

        amount_node = txn.find("transactionShares")
        amount = float(amount_node.value.string) if amount_node and amount_node.value else 0

        if code == "P" or acquired_or_disposed == "A":
            buys += amount
        elif code == "S" or acquired_or_disposed == "D":
            sells += amount

    return {"buys": buys, "sells": sells}


def fetch_and_update_insider_flow():
    cik = "1930021"  # ✅ Replace with your real CIK
    urls = get_latest_form4_urls(cik, limit=5)  # Get last 5 Form 4s

    total_buys = 0
    total_sells = 0

    for url in urls:
        print(f"Fetching: {url}")
        result = parse_form4_xml(url)
        total_buys += result["buys"]
        total_sells += result["sells"]

    output = {
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }

    with open("insider_flow.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ insider_flow.json updated with latest filings!")

if __name__ == "__main__":
    fetch_and_update_insider_flow()