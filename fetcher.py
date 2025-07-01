import requests
from bs4 import BeautifulSoup
import json

def parse_form4_xml(url: str) -> dict:
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url}")

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
    # ✅ Replace with your real SEC Form 4 XML URLs
    urls = [
        "https://www.sec.gov/Archives/edgar/data/0000000000/0001104659-25-000000.xml",
        # Add more if needed
    ]

    total_buys = 0
    total_sells = 0

    for url in urls:
        result = parse_form4_xml(url)
        total_buys += result["buys"]
        total_sells += result["sells"]

    # Example: using same for top buys/sells (adjust if needed)
    output = {
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }

    with open("insider_flow.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ insider_flow.json updated!")

if __name__ == "__main__":
    fetch_and_update_insider_flow()