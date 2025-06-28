import json

def main():
    data = {
        "summary": "This is test data",
        "buys": 999999,
        "sells": 555555
    }

    with open("insider_flow.json", "w") as f:
        json.dump(data, f)

    print("✅ insider_flow.json has been written.")

if __name__ == "__main__":
    main()