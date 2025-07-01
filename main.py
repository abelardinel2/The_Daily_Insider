import json
import fetcher
import send_telegram

def main():
    fetcher.fetch_and_update_insider_flow()  # ✅ Runs first to refresh JSON
    with open("insider_flow.json") as f:
        data = json.load(f)
    send_telegram.send_summary(data)  # ✅ Sends fresh data to Telegram

if __name__ == "__main__":
    main()