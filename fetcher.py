import json

def main():
    # 🔥 Replace this block with your real parse logic!
    data = {
        "top_buys": 5000000,
        "top_sells": 1000000,
        "total_buys": 5000000,
        "total_sells": 1000000
    }

    with open("insider_flow.json", "w") as f:
        json.dump(data, f)

    print("✅ insider_flow.json created")

if __name__ == "__main__":
    main()