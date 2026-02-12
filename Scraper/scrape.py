import requests
import pandas as pd
from datetime import datetime

API_URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=2000"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nasdaq.com/market-activity/stocks/screener"
}

def safe_float(x):
    try:
        x = str(x).replace("$", "").replace(",", "").replace("%", "").strip()
        if x in ["", "N/A", "UNCH", "--", "None", "nan"]:
            return None
        return float(x)
    except:
        return None

def main():
    resp = requests.get(API_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()

    rows = resp.json()["data"]["table"]["rows"]
    df = pd.DataFrame(rows)

    df = df.rename(columns={
        "symbol": "symbol",
        "name": "company_name",
        "lastsale": "price",
        "netchange": "net_change",
        "pctchange": "change_percent",
        "marketCap": "market_cap"
    })

    for col in ["price", "net_change","change_percent", "market_cap"]:
        if col in df.columns:
            df[col] = df[col].apply(safe_float)

    df["category"] = "NASDAQ Listed Stocks"
    df["source_url"] = "https://www.nasdaq.com/market-activity/stocks/screener"
    df["scraped_at"] = datetime.utcnow()

    final_cols = [
        c for c in [
            "symbol",
            "company_name",
            "price",
            "net_change",
            "change_percent",
            "market_cap",
            "category",
            "source_url",
            "scraped_at",
        ]
        if c in df.columns
    ]

    df = df[final_cols]

    df.to_csv("raw_data.csv", index=False)
    print(f"Saved {len(df)} rows to raw_data.csv")

if __name__ == "__main__":
    main()
