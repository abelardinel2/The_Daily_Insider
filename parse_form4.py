import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url):
    headers = {
        "User-Agent": "Amelia Belardinelli al3000@tc.columbia.edu"
    }
    resp = requests.get(filing_url, headers=headers)

    if resp.status_code != 200:
        raise ValueError(f"Could not fetch XML: {resp.status_code}")

    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError:
        print("\n------ RAW RESPONSE ------\n")
        print(resp.text)
        print("\n--------------------------\n")
        raise ValueError("Invalid XML: Response does not parse.")

    buys, sells = 0, 0
    for txn in root.iter():
        if "Acquired" in txn.tag:
            buys += 1
        if "Disposed" in txn.tag:
            sells += 1

    return {"buys": buys, "sells": sells}