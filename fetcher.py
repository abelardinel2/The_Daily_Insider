import json

def load_tickers():
    with open("tickers.txt") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    tickers = load_tickers()
    total_buys = 0
    total_sells = 0

    for ticker in tickers:
        total_buys += 100000  # placeholder logic
        total_sells += 50000  # placeholder logic

    data = {
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }

    with open("insider_flow.json", "w") as f:
        json.dump(data, f)

    print(f"✅ insider_flow.json created for tickers: {tickers}")

if __name__ == "__main__":
    main()