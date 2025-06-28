import json
import send_telegram

def main():
    with open("insider_flow.json") as f:
        data = json.load(f)
    send_telegram.send_summary(data)

if __name__ == "__main__":
    main()