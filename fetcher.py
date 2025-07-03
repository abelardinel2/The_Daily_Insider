# ... (existing imports and WATCHLIST definition)
def fetch_and_update_insider_flow():
    url = "https://www.sec.gov/cgi-bin/current_q?i=csv"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Fetched RSS at {datetime.now()}: {response.text[:500]}...")
        root = ET.fromstring(response.content)
        trades = {
            "top_buys": 0.0,
            "top_sells": 0.0,
            "total_buys": 0.0,
            "total_sells": 0.0
        }
        for item in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = item.find('{http://www.w3.org/2005/Atom}title').text
            summary = item.find('{http://www.w3.org/2005/Atom}summary').text
            link = item.find('{http://www.w3.org/2005/Atom}link')['href']
            print(f"Processing link: {link}")
            try:
                form4_data = parse_form4_xml(link)
                trades["total_buys"] += form4_data["buys"]
                trades["total_sells"] += form4_data["sells"]
                # Simple dollar conversion for "top" (refine with real prices)
                trades["top_buys"] += form4_data["buys"] * 100  # Placeholder price
                trades["top_sells"] += form4_data["sells"] * 100  # Placeholder price
            except Exception as e:
                print(f"Error parsing {link}: {e}")
        print(f"Trade summary: {trades}")
        with open("insider_flow.json", "w") as f:
            json.dump(trades, f, indent=4)
    except requests.exceptions.RequestError as e:
        print(f"Error fetching data: {e}")
        with open("insider_flow.json", "w") as f:
            json.dump({"top_buys": 0.0, "top_sells": 0.0, "total_buys": 0.0, "total_sells": 0.0}, f, indent=4)
    except ET.ParseError:
        print("Error parsing SEC RSS feed")
        with open("insider_flow.json", "w") as f:
            json.dump({"top_buys": 0.0, "top_sells": 0.0, "total_buys": 0.0, "total_sells": 0.0}, f, indent=4)

if __name__ == "__main__":
    fetch_and_update_insider_flow()