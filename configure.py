# config.py
# Configuration for SEC EDGAR fetcher with OpenBB integration and proxy support

COMPANY_NAME = "Oria Dawn Analytics"
SEC_EMAIL = "contact@oriadawn.xyz"
TELEGRAM_BOT_TOKEN = "7975548444:AAFtmHs3S3GYL_rDpawtDE-f_09_lFg3ex8"
TELEGRAM_CHAT_ID = "6652085600"
SUMMARY_LABEL = "Morning"
RSS_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent"
API_URL = "https://data.sec.gov/submissions/CIK{}.json"  # SEC API fallback
USER_AGENT = f"{COMPANY_NAME}/1.0 ({SEC_EMAIL})"
OPENBB_LOG_COLLECT = False  # Disable OpenBB telemetry

# Proxy configuration (update with your proxy provider details)
PROXY_ENABLED = False  # Set to True after configuring proxy
PROXY = {
    "http": "http://<username>:<password>@<proxy_host>:<port>",
    "https": "http://<username>:<password>@<proxy_host>:<port>"
}
# ScrapingBee configuration (recommended for simplicity)
SCRAPINGBEE_API_KEY = ""  # Add your ScrapingBee API key here
SCRAPINGBEE_URL = "https://api.scrapingbee.com/?api_key={}&url={}"