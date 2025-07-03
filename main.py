import os
import json
import fetcher
import send_telegram
from datetime import datetime

def main():
    try:
        # Fetch and update insider_flow_analyzer.json
        fetcher.fetch_and_update_insider_flow()  # ✅ Runs first to refresh JSON
        with open("insider_flow_analyzer.json", "r") as f:
            data = json.load(f)
        send_telegram.send_summary(data)  # ✅ Sends Analyzer summary
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - File error: {e}\n")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - JSON error: {e}\n")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        with open("output.log", "a") as f:
            f.write(f"{datetime.now()} - Unexpected error: {e}\n")

if __name__ == "__main__":
    main()