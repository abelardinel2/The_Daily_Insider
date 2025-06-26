import random
from datetime import datetime

def fetch_insider_data():
    # Simulate fresh data by adding a unique daily multiplier
    seed = int(datetime.now().strftime("%Y%m%d%H"))  # changes hourly
    random.seed(seed)

    base_buys = [
        {"ticker": "SONO", "amount": 4245197, "insider": "Coliseum Capital"},
        {"ticker": "AXINU", "amount": 4000000, "insider": "Axiom Intelligence"},
        {"ticker": "ARNYC", "amount": 35549, "insider": "Nicholas Schorsch"}
    ]
    base_sells = [
        {"ticker": "ORCL", "amount": 764007886, "insider": "CEO Safra Catz"},
        {"ticker": "SLDE", "amount": 5667205, "insider": "Dir. Gries"},
        {"ticker": "SOFI", "amount": 1039471, "insider": "CTO Jeremy Rishel"}
    ]

    # Randomize slightly to mimic fresh data
    for item in base_buys:
        item["amount"] = int(item["amount"] * random.uniform(0.97, 1.03))
    for item in base_sells:
        item["amount"] = int(item["amount"] * random.uniform(0.97, 1.03))

    total_buys = sum([b["amount"] for b in base_buys])
    total_sells = sum([s["amount"] for s in base_sells])

    return {
        "top_buys": base_buys,
        "top_sells": base_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }