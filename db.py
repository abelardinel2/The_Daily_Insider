import json

SNAPSHOT_FILE = "snapshot.json"

def save_snapshot(data):
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(data, f)

def load_snapshot():
    try:
        with open(SNAPSHOT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
