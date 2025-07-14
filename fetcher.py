import feedparser

SEC_FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&owner=only&count=100&output=atom"

def fetch_form4_entries():
    feed = feedparser.parse(SEC_FEED_URL)
    entries = []

    for entry in feed.entries:
        if "form-type" in entry and entry["form-type"] == "4":
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "updated": entry.updated
            })
    return entries