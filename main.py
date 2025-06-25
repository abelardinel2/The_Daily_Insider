import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_sample_form4():
    # Example stub: Fetch a recent Form 4 XML page from SEC (to be customized)
    url = "https://www.sec.gov/Archives/edgar/data/1595527/000095014225001669/xslF345X03/es250646322_4-arnyc.xml"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def parse_and_analyze(data):
    # Stub: parsing logic here
    return {"buys": 5_000_000, "sells": 75_000_000, "bias": "Bearish"}

if __name__ == "__main__":
    raw_data = fetch_sample_form4()
    if raw_data:
        result = parse_and_analyze(raw_data)
        print("Bias:", result["bias"])
    else:
        print("Failed to fetch Form 4 data.")
