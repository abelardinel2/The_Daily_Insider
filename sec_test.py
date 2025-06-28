import requests

SEC_XML_URL = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"

headers = {
    "User-Agent": "InsiderFlowBot/1.0 (al3000@tc.columbia.edu)"
}

response = requests.get(SEC_XML_URL, headers=headers)

if response.status_code == 200:
    print("✅ SUCCESS: Got the XML!")
    print(response.text[:500])  # print first 500 chars
else:
    print(f"❌ ERROR: {response.status_code} — {response.text}")
