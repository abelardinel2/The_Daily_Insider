import json
from send_telegram import send_summary  # ✅ use the real filename

def main():
    with open("insider_flow.json") as f:
        data = json.load(f)

    send_summary(data)

if __name__ == "__main__":
    main()
