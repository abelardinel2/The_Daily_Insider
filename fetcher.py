
import json

data = {"buys": 5, "sells": 3}

with open("insider_flow.json", "w") as f:
    json.dump(data, f)

print("✅ insider_flow.json written!")
