import requests
from bs4 import BeautifulSoup

def parse_form4_xml(url: str) -> dict:
    try:
        # Fetch the Form 4 XML
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return {"buys": 0, "sells": 0}

    try:
        # Parse the XML with BeautifulSoup
        soup = BeautifulSoup(resp.text, "xml")
        buys = 0
        sells = 0

        # Find all non-derivative transactions
        for txn in soup.find_all("nonDerivativeTransaction"):
            # Extract key fields with safety checks
            code = txn.find("transactionCode")
            acquired_or_disposed = txn.find("transactionAcquiredDisposedCode")
            amount_node = txn.find("transactionShares")

            if not all([code, acquired_or_disposed, amount_node]):
                print(f"❌ Skipping transaction in {url}: Missing data")
                continue

            code_value = code.text.strip() if code.text else ""
            acquired_value = acquired_or_disposed.text.strip() if acquired_or_disposed.text else ""
            amount_str = amount_node.find("value").text.strip() if amount_node.find("value") else "0"
            amount = float(amount_str) if amount_str else 0.0

            # Log for debugging
            print(f"Transaction: Code={code_value}, Acquired/Disposed={acquired_value}, Amount={amount}")

            # Classify as buy or sell
            if code_value == "P" or acquired_value == "A":  # Purchase or Acquired
                buys += amount
            elif code_value == "S" or acquired_value == "D":  # Sale or Disposed
                sells += amount

        print(f"Parsed {url}: Buys={buys}, Sells={sells}")
        return {"buys": buys, "sells": sells}

    except Exception as e:
        print(f"❌ Error parsing {url}: {e}")
        return {"buys": 0, "sells": 0}