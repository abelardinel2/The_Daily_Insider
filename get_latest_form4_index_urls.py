import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "AmeliaBelardinelli (ameliabelardinelli@gmail.com)"
}

def get_latest_form4_index_urls(cik: str, limit: int = 5) -> list:
    """
    Uses EDGAR Atom feed to get recent Form 4 filings for a CIK,
    returns the index page URLs.
    """
    cik = cik.lstrip("0")  # strip leading zeros if present
    feed_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=4&count={limit}&output=atom"

    resp = requests.get(feed_url, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch Atom feed: {feed_url}")

    soup = BeautifulSoup(resp.text, "xml")
    entries = soup.find_all("entry")
    index_urls = []

    for entry in entries[:limit]:
        link_tag = entry.find("link")
        if link_tag and link_tag.has_attr("href"):
            html_page = link_tag['href']
            # Ensure it ends with -index.htm
            if not html_page.endswith("-index.htm"):
                html_page += "-index.htm"
            index_urls.append(html_page)

    print("✅ Latest Form 4 index pages:", index_urls)
    return index_urls
