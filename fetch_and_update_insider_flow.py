import requests
from bs4 import BeautifulSoup
from parse_form4 import parse_form4_xml  # your custom parser
import json

# ------------ AUTO-RESOLVER ------------
def resolve_to_xml_url(url: str) -> str:
    """If given an index landing page, follow links to find XML."""
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

# ------------ MAIN FETCH + UPDATE ------------
def fetch_and_update_insider_flow():
    # ---- NEW CIK AUTO-FETCH ----
    CIK = "836690"  # << Replace with your target CIK
    index_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK}&type=4&owner=only&count=40"

    resp = requests.get(index_url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch index page for CIK {CIK}")

    soup = BeautifulSoup(resp.text, "html.parser")

    landing_pages = []
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if href.endswith('.xml') and 'Archives' in href:
            if href.startswith('/'):
                resolved = f"https://www.sec.gov{href}"
            else:
                resolved = href
            landing_pages.append(resolved)

    print(f"✅ Found {len(landing_pages)} Form 4 XMLs for CIK {CIK}")

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

# ------------ ENTRY ------------
if __name__ == "__main__":
    fetch_and_update_insider_flow()