import json

def main():
    data = {
        "top_buys": 999999,
        "top_sells": 555555,
        "total_buys": 999999,
        "total_sells": 555555
    }

    with open("insider_flow.json", "w") as f:
        json.dump(data, f)

    print("✅ insider_flow.json has been written!")

if __name__ == "__main__":
    main()