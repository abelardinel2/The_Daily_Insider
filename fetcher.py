import json

def main():
    tickers = []
    with open("tickers.txt") as f:
        tickers = [line.strip() for line in f.readlines() if line.strip()]

    summary = []
    total_buys = 0
    total_sells = 0

    for ticker in tickers:
        buys = 1000000  # placeholder example
        sells = 500000
        total_buys += buys
        total_sells += sells
        summary.append({"ticker": ticker, "buys": buys, "sells": sells})

    data = {
        "summary": summary,
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }

    with open("insider_flow.json", "w") as f:
        json.dump(data, f)

    print("✅ insider_flow.json written!")

if __name__ == "__main__":
    main()