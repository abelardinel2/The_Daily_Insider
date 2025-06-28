def parse_form4_amount(ticker):
    # Placeholder logic: simulate amounts
    # Real parser would inspect SEC data
    if ticker in ["AAPL", "TSLA", "NVDA"]:
        return 5_000_000
    elif ticker in ["MSFT", "AMZN", "AMD"]:
        return -4_000_000
    else:
        return 0