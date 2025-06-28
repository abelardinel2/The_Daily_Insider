import os
from sec_edgar_downloader import Downloader
from parse_form4 import parse_form4_amount

# Special mappings for tickers with dots
SPECIAL_MAP = {
    "BRK.B": "BRK-B",
    "BRK.A": "BRK-A",
    "BF.B": "BF-B",
    "BF.A": "BF-A"
}

dl = Downloader("Your Company Name", os.getenv("SEC_EMAIL"))

with open("tickers.txt") as f:
    tickers = [line.strip() for line in f]

for ticker in tickers:
    mapped = SPECIAL_MAP.get(ticker, ticker)
    print(f"Processing {mapped}")
    amount = parse_form4_amount(mapped)
    print(f"Parsed amount for {mapped}: {amount}")