import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "AmeliaBelardinelli (ameliabelardinelli@gmail.com)"
}

def get_latest_form4_urls(cik: str, limit: int = 5):
    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url} (Status: {resp.status_code})")

    data = resp.json()

    form_indexes = [i for i, f in enumerate(data["filings"]["recent"]["form"]) if f == "4"]

    urls = []
    for idx in form_indexes[:limit]:
        accession = data["filings"]["recent"]["accessionNumber"][idx].replace("-", "")
        primary_doc = data["filings"]["recent"]["primaryDocument"][idx]
        raw_cik = str(int(cik))  # Remove leading zeros
        xml_url = f"https://www.sec.gov/Archives/edgar/data/{raw_cik}/{accession}/{primary_doc}"
        urls.append(xml_url)

    print("✅ Found Form 4 URLs:", urls)
    return urls


def parse_form4_xml(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url} (Status: {resp.status_code})")

    soup = BeautifulSoup(resp.text, "xml")
    print(f"🔍 XML Preview for {url}:\n", soup.prettify()[:500], "...\n")

    buys = 0
    sells = 0

    transactions = soup.find_all("nonDerivativeTransaction")
    print(f"🧩 Found {len(transactions)} <nonDerivativeTransaction> blocks")

    for txn in transactions:
        print("🗂️ One transaction block:")
        print(txn.prettify())

        code = txn.transactionCode.string.strip() if txn.transactionCode and txn.transactionCode.string else ""
        acquired_or_disposed = txn.transactionAcquiredDisposedCode.string.strip() if txn.transactionAcquiredDisposedCode and txn.transactionAcquiredDisposedCode.string else ""

        amount_node = txn.find("transactionShares")
        amount = 0
        if amount_node and amount_node.value:
            try:
                amount = float(amount_node.value.string.strip())
            except ValueError:
                amount = 0

        print(f"🔑 code: '{code}' | A/D: '{acquired_or_disposed}' | 💵 amount: {amount}")

        if code == "P" or acquired_or_disposed == "A":
            buys += amount
        elif code == "S" or acquired_or_disposed == "D":
            sells += amount

    return {"buys": buys, "sells": sells}


def fetch_and_update_insider_flow():
    cik = "1930021"  # ✅ Replace with your target CIK!
    urls = get_latest_form4_urls(cik, limit=5)

    total_buys = 0
    total_sells = 0

    for url in urls:
        print(f"🚀 Fetching: {url}")
        result = parse_form4_xml(url)
        print(f"✅ Parsed result for {url}: {result}")
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

    print("✅ insider_flow.json updated with totals:", output)


if __name__ == "__main__":
    fetch_and_update_insider_flow()