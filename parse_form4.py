import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url: str) -> dict:
    """
    Parse a single SEC Form 4 XML filing and return buy/sell USD totals.
    """
    headers = {"User-Agent": "InsiderFlowBot"}
    resp = requests.get(filing_url, headers=headers)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)

    buys = 0.0
    sells = 0.0

    for tx in root.findall(".//nonDerivativeTransaction"):
        code = tx.findtext(".//transactionAcquiredDisposedCode/value")
        shares = tx.findtext(".//transactionShares/value")
        price = tx.findtext(".//transactionPricePerShare/value")

        try:
            shares = float(shares) if shares else 0.0
            price = float(price) if price else 0.0
        except ValueError:
            shares = 0.0
            price = 0.0

        amount = shares * price

        if code == "A":
            buys += amount
        elif code == "D":
            sells += amount

    return {"buys": buys, "sells": sells}


if __name__ == "__main__":
    # 🔥 Test it directly:
    test_url = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"
    result = parse_form4_amount(test_url)
    print(f"Buys: ${result['buys']:.2f} | Sells: ${result['sells']:.2f}")