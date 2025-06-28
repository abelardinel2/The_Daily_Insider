import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url, email):
    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)",
        "Accept": "application/xml"
    }

    resp = requests.get(filing_url, headers=headers)
    if not resp.text.startswith("<?xml"):
        raise ValueError("Expected XML but got HTML instead.")

    root = ET.fromstring(resp.text)
    # This is just placeholder logic:
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