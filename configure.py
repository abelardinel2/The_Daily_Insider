# config.py
# Configuration for SEC EDGAR fetcher with OpenBB integration and proxy support

COMPANY_NAME = "Oria Dawn Analytics"
SEC_EMAIL = "contact@oriadawn.xyz"
TELEGRAM_BOT_TOKEN = "7975548444:AAFtmHs3S3GYL_rDpawtDE-f_09_lFg3ex8"
TELEGRAM_CHAT_ID = "6652085600"
SUMMARY_LABEL = "Morning"
RSS_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent"
API_URL = "https://data.sec.gov/submissions/CIK{}.json"
USER_AGENT = f"{COMPANY_NAME}/1.0 ({SEC_EMAIL})"
OPENBB_LOG_COLLECT = False

PROXY_ENABLED = False
PROXY = {
    "http": "http://<username>:<password>@<proxy_host>:<port>",
    "https": "http://<username>:<password>@<proxy_host>:<port>"
}
SCRAPINGBEE_API_KEY = ""
SCRAPINGBEE_URL = "https://api.scrapingbee.com/?api_key={}&url={}"