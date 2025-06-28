import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url, email):
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)",
        "Accept": "application/xml"
    }

    resp = requests.get(filing_url, headers=headers)

    print(f"HTTP status: {resp.status_code}")
    print(f"Response (first 200 chars):\n{resp.text[:200]}")

    if not resp.text.strip().startswith("<?xml"):
        raise ValueError(f"Expected XML but got: {resp.text[:200]}...")

    try:
        root = ET.fromstring(resp.text)
    except Exception as e:
        raise ValueError(f"XML parse error: {e}")

    buys = 0
    sells = 0
    for txn in root.iter("{http://www.sec.gov/edgar/document/thirteenf/informationtable}transaction"):
        code = txn.find(".//transactionAcquiredDisposedCode").text
        shares = int(txn.find(".//transactionShares").text)
        if code == "A":
            buys += shares
        elif code == "D":
            sells += shares

    return {"buys": buys, "sells": sells}