import xml.etree.ElementTree as ET

def parse_form4_xml(file_path):
    buys = 0.0
    sells = 0.0

    tree = ET.parse(file_path)
    root = tree.getroot()

    for txn in root.iter("nonDerivativeTransaction"):
        code = txn.findtext(".//transactionCode")
        shares = txn.findtext(".//transactionShares/value")

        if shares is not None:
            shares = float(shares)
            if code == "P":
                buys += shares
            elif code == "S":
                sells += shares

    return buys, sells
