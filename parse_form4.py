import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url):
    resp = requests.get(filing_url)
    if resp.status_code != 200:
        raise ValueError(f"Could not fetch XML: {resp.status_code}")

    text = resp.text

    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        raise ValueError("Invalid XML: Response does not parse.")

    buys = 0
    sells = 0

    for txn in root.iter("nonDerivativeTransaction"):
        code = txn.findtext(".//transactionAcquiredDisposedCode")
        shares = txn.findtext(".//transactionShares/value")

        if shares is None:
            continue

        shares = float(shares)
        if code == "A":
            buys += shares
        elif code == "D":
            sells += shares

    return {"buys": buys, "sells": sells}