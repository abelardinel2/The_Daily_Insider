import json
import notifier

def main():
    with open("insider_flow.json") as f:
        data = json.load(f)
    notifier.send_summary(data)

if __name__ == "__main__":
    main()