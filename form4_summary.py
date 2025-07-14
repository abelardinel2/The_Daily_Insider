def summarize_trades(entries):
    sales = []
    buys = []

    for entry in entries:
        summary = entry["summary"]
        if "S - Sale" in summary or "S - Sale+OE" in summary:
            sales.append(summary)
        elif "P - Purchase" in summary:
            buys.append(summary)

    total_sales = len(sales)
    total_buys = len(buys)

    if total_sales == 0 and total_buys == 0:
        return None

    sale_lines = "\n".join([f"• {s.splitlines()[0]}" for s in sales[:5]])
    buy_lines = "\n".join([f"• {b.splitlines()[0]}" for b in buys[:3]])

    ratio = f"{total_buys} : {total_sales}" if total_buys > 0 else f"0 : {total_sales}"

    return f"""📊 Insider Flow Summary — {datetime.now().strftime('%B %d, %Y')}
Total Sales: {total_sales}
Total Buys: {total_buys}
Buy/Sell Ratio: {ratio}

🚨 Notable Sales:
{sale_lines or 'None'}

🟢 Notable Buys:
{buy_lines or 'None'}
"""
