# Insider Flow Analyzer Bot

This Telegram bot fetches insider trading activity daily and summarizes:

- Top 3 Buys
- Top 3 Sells
- Total Buy and Sell volumes
- Market Bias (Buy-side / Sell-side)

## How It Works

1. Parses insider transaction data from openinsider.com
2. Aggregates buy/sell volumes
3. Sends a summary to your Telegram bot

## Schedule

This bot runs twice per day:
- 🕘 9:00 AM ET (13:00 UTC)
- 🕔 5:00 PM ET (21:00 UTC)

## Setup

1. **Create Telegram Bot** via @BotFather
2. Store your bot token and chat ID as GitHub repository secrets:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Deploy using [Railway](https://railway.app/) or GitHub Actions

## Example Output