import json
import send_telegram  # ✅ FIXED!

def main():
    with open("insider_flow.json") as f:
        data = json.load(f)
    send_telegram.send_summary(data)  # ✅ FIXED!

if __name__ == "__main__":
    main()