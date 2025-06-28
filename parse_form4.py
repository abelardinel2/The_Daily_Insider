import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url):
    """
    Downloads a single SEC Form 4 XML and extracts basic buy/sell count.
    """

    headers = {
        "User-Agent": "InsiderFlowBot/1.0 (al3000@tc.columbia.edu)"
    }

    resp = requests.get(filing_url, headers=headers)
    if resp.status_code != 200:
        raise ValueError(f"Could not fetch XML: {resp.status_code}")

    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError:
        raise ValueError("Invalid XML: Response does not parse.")

    buys = 0
    sells = 0

    for txn in root.iter("nonDerivativeTransaction"):
        code = txn.findtext(".//transactionAcquiredDisposedCode/value")
        shares = txn.findtext(".//transactionShares/value")
        if shares:
            shares = float(shares)
            if code == "A":
                buys += shares
            elif code == "D":
                sells += shares

    return {"buys": buys, "sells": sells}