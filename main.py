from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = FastAPI()

# Hardcoded API key
VALID_API_KEY = "k6DliYeidMR64Lix5q32uZEtKVsT671B"

@app.get("/api/v3/insider-trading")
async def insider_trading(apikey: str = "", limit: int = 10):
    if apikey != VALID_API_KEY:
        return JSONResponse(status_code=403, content={"error": "Invalid API key"})

    url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&td=0&xp=1&sortcol=0&cnt=100"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", {"class": "tinytable"})
    rows = table.find_all("tr")[1:]  # Skip header row

    data = []
    for row in rows[:limit]:
        cols = row.find_all("td")
        if len(cols) < 11:
            continue
        data.append({
            "ticker": cols[3].text.strip(),
            "owner": cols[5].text.strip(),
            "relationship": cols[6].text.strip(),
            "transaction_date": cols[1].text.strip(),
            "transaction_type": cols[7].text.strip(),
            "cost": cols[8].text.strip(),
            "shares": cols[9].text.strip(),
            "value": cols[10].text.strip(),
        })

    return {
        "data": data,
        "source": "OpenInsider",
        "fetched_at": datetime.utcnow().isoformat()
    }