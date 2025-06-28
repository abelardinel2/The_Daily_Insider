import json

def main():
    data = {
        "top_buys": 5000000,
        "top_sells": 2000000,
        "total_buys": 8000000,
        "total_sells": 3000000
    }

    with open("insider_flow.json", "w") as f:
        json.dump(data, f)

    print("✅ insider_flow.json has been written!")

if __name__ == "__main__":
    main()