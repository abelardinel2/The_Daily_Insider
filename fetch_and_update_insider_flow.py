import requests
from bs4 import BeautifulSoup
from parse_form4 import parse_form4_xml  # your existing parser
import json

# ----------- AUTO-RESOLVER -----------
def resolve_to_xml_url(url: str) -> str:
    """If given an index landing page, follow links to get the real XML."""
    if url.endswith('-index.htm') or url.endswith('.htm'):
        print(f"🌐 Resolving index page: {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch landing page: {url}")

        soup = BeautifulSoup(resp.text, "html.parser")

        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.endswith('.xml'):
                if href.startswith('/'):
                    resolved = f"https://www.sec.gov{href}"
                elif href.startswith('http'):
                    resolved = href
                else:
                    base = url.rsplit('/', 1)[0]
                    resolved = f"{base}/{href}"
                print(f"✅ Resolved to XML: {resolved}")
                return resolved

        raise Exception(f"No XML link found on: {url}")

    # If it’s already XML:
    print(f"✅ Using direct XML: {url}")
    return url

# ----------- MAIN FETCH + UPDATE -----------
def fetch_and_update_insider_flow():
    # Example list — replace with your CIK logic!
    landing_pages = [
        "https://www.sec.gov/Archives/edgar/data/836690/0001946479-25-000025-index.htm",
        "https://www.sec.gov/Archives/edgar/data/1419275/000164117225017287-index.htm",
    ]

    total_buys = 0
    total_sells = 0

    for url in landing_pages:
        xml_url = resolve_to_xml_url(url)
        result = parse_form4_xml(xml_url)
        total_buys += result['buys']
        total_sells += result['sells']

    # Write to your JSON file
    output = {
        "top_buys": total_buys,
        "top_sells": total_sells
    }

    with open("insider_flow.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ insider_flow.json updated: {output}")

# ----------- ENTRY -----------
if __name__ == "__main__":
    fetch_and_update_insider_flow()
