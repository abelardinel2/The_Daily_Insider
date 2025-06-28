import os
import re

def parse_form4_amount(filing):
    """
    Try to extract the dollar amount from a Form 4 text file.
    Looks for lines with 'Price' and 'Shares' and multiplies.
    """
    path = filing.get("local_path")
    if not path or not os.path.isfile(path):
        return 0

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        # Very simple pattern — find something like:
        # Price: $123.45, Shares: 1000
        price_match = re.search(r"Price[^0-9$]*\$?([\d,.]+)", text, re.IGNORECASE)
        shares_match = re.search(r"Shares[^0-9]*([\d,]+)", text, re.IGNORECASE)

        if price_match and shares_match:
            price = float(price_match.group(1).replace(",", ""))
            shares = int(shares_match.group(1).replace(",", ""))
            amount = price * shares

            # Try to guess if it’s a sale or buy
            if "dispose" in text.lower() or "disposed" in text.lower():
                return -amount
            else:
                return amount

    except Exception as e:
        print(f"Parse error: {e}")
        return 0

    return 0