import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url: str, email: str) -> dict:
    """
    Download SEC Form 4 XML and parse buy/sell amounts.
    """
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)"
    }

    resp = requests.get(filing_url, headers=headers)

    if resp.status_code != 200:
        print("-------- RAW RESPONSE --------")
        print(resp.text[:500])
        raise ValueError(f"Could not fetch XML: {resp.status_code}")

    if "html" in resp.headers.get("Content-Type", "").lower():
        print("-------- RAW HTML --------")
        print(resp.text[:500])
        raise ValueError("Expected XML but got HTML instead.")

    if not resp.text.strip().startswith("<?xml"):
        print("-------- RAW RESPONSE --------")
        print(resp.text[:500])
        raise ValueError("Invalid XML: Response does not start with <?xml")

    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as e:
        print("-------- RAW RESPONSE --------")
        print(resp.text[:500])
        raise ValueError(f"Invalid XML: ParseError: {e}")

    buys, sells = 0, 0

    for txn in root.iter("nonDerivativeTransaction"):
        code = txn.findtext(".//transactionAcquiredDisposedCode/value")
        shares = txn.findtext(".//transactionShares/value")

        if shares is None:
            continue

        shares = float(shares)

        if code == "A":
            buys += shares
        elif code == "D":
            sells += shares

    return {"buys": buys, "sells": sells}