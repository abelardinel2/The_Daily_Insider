name: Fetch and Notify Insider Flow

on:
  workflow_dispatch:
  schedule:
    - cron: '0 12 * * *'  # Runs daily at 12:00 UTC (adjust if needed)

jobs:
  fetch_and_notify:
    runs-on: ubuntu-latest

    steps:
    - name: Set up job
      run: echo "Starting job..."

    - name: Checkout Repository
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Fetch and Update insider_flow.json
      run: python fetch_and_update_insider_flow.py

    - name: Commit and push updated insider_flow.json
      run: |
        git config --global user.name "github-actions[bot]"
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git add insider_flow.json
        if git diff --cached --quiet; then
          echo "✅ No changes to commit."
        else
          git commit -m "Update insider
