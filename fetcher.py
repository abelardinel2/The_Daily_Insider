import requests
import os
from datetime import datetime, timedelta
import json
from xml.etree import ElementTree as ET
import time

SEC_BASE = "https://www.sec.gov/Archives/edgar/"
headers = {"User-Agent": f"{os.getenv('SEC_EMAIL')}"}

def parse_form_xml(xml_url):
    response = requests.get(xml_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch {xml_url}: {response.status_code}")
        return [0, 0]  # [buys, sells]
    tree = ET.fromstring(response.content)
    total_buys = 0
    total_sells = 0
    
    # Handle Form 4
    for table in tree.findall(".//table[@id='nonDerivativeTable']"):
        for row in table.findall("tr"):
            cols = row.findall("td")
            if len(cols) >= 6:
                code = cols[3].text.strip()  # Transaction Code (P or S)
                shares = float(cols[4].text.split()[0].replace(",", ""))  # Handle commas
                price = float(cols[5].text.split()[0].replace("$", "").replace(",", ""))  # Handle commas and $
                value = shares * price
                if code == "P":
                    total_buys += value
                elif code == "S":
                    total_sells += value
    
    # Handle Form 144 (sales only)
    if "144" in xml_url:
        # Securities Information Table
        for row in tree.findall(".//table[@id='securitiesInformationTable']"):
            cols = row.findall("td")
            if len(cols) >= 6 and cols[5].text:  # Approximate Date of Sale
                sale_date = datetime.strptime(cols[5].text, "%m/%d/%Y")
                end_date = datetime.today()
                start_date = end_date - timedelta(days=5)
                if start_date <= sale_date <= end_date:
                    value = float(cols[3].text.replace(",", "").replace("$", ""))  # Aggregate Market Value
                    total_sells += value
        # Past 3 Months Sales Table
        for row in tree.findall(".//table[@id='securitiesSoldTable']"):
            cols = row.findall("td")
            if len(cols) >= 4 and cols[2].text:  # Date of Sale
                sale_date = datetime.strptime(cols[2].text, "%m/%d/%Y")
                if start_date <= sale_date <= end_date:
                    value = float(cols[4].text.replace(",", "").replace("$", ""))  # Gross Proceeds
                    total_sells += value
    
    return [total_buys, total_sells]

def fetch_all_forms(days=5):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    
    total_buys = 0
    total_sells = 0
    
    # Fetch the daily index for the latest date
    index_url = f"{SEC_BASE}daily-index/{end_date.strftime('%Y%m%d')}/master.idx"
    response = requests.get(index_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch index: {index_url}, {response.status_code}")
        # Fallback to monthly index if daily fails
        index_url = f"{SEC_BASE}daily-index/{end_date.strftime('%Y%m')}/master.idx"
        response = requests.get(index_url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to fetch monthly index: {index_url}, {response.status_code}")
            return
    
    lines = response.text.splitlines()
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 5 and ("4" in parts[2] or "144" in parts[2]):
            cik = parts[0]
            acc_num = parts[4].replace("-", "")
            filing_date = parts[3]
            filed_dt = datetime.strptime(filing_date, "%Y-%m-%d")
            if start_date <= filed_dt <= end_date:
                if "4" in parts[2]:
                    xml_url = f"{SEC_BASE}edgar/data/{cik}/{acc_num}/xslF345X05/primary_doc.xml"  # Matches your example
                elif "144" in parts[2]:
                    xml_url = f"{SEC_BASE}edgar/data/{cik}/{acc_num}/xsl144X01/primary_doc.xml"
                result = parse_form_xml(xml_url)
                print(f"✅ {xml_url} -> {result}")
                total_buys += result[0]
                total_sells += result[1]
                time.sleep(0.1)  # Respect SEC rate limits
    
    data = {
        "top_buys": total_buys,
        "top_sells": total_sells,
        "total_buys": total_buys,
        "total_sells": total_sells
    }
    
    with open("insider_flow.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ insider_flow.json updated!")

if __name__ == "__main__":
    fetch_all_forms()