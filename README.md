# 📊 Scrape to Insight Pipeline

End-to-end data pipeline that scrapes stock market data, loads it into Snowflake, transforms it using dbt, and exposes analytics via a Streamlit dashboard.

---

## 1. Dataset Source

**Source:** Yahoo Finance – Stock Screeners  

URLs:
- https://finance.yahoo.com/screener/predefined/most_actives  
- https://finance.yahoo.com/screener/predefined/nasdaq  

The scraper extracts:
- Stock symbol  
- Company name  
- Price  
- Net change  
- Percentage change  
- Market category  
- Scrape timestamp  

---

## 2. How to Run the Scraper

### Prerequisites
- Python 3.9+
- Virtual environment activated

### Install dependencies
```bash
cd scraper
pip install -r requirements.txt
```

### Run the scraper
```bash
python scrape.py
```

### Output
- Generates `raw_data.csv` in the `scraper/` directory
- This file is used for Snowflake ingestion

---

## 3. How to Create & Load Snowflake Tables

### 3.1 Create database & schemas

Run the following in **Snowflake Worksheet**:

```sql
CREATE DATABASE IF NOT EXISTS SCRAPE_PIPELINE;

CREATE SCHEMA IF NOT EXISTS SCRAPE_PIPELINE.RAW;
CREATE SCHEMA IF NOT EXISTS SCRAPE_PIPELINE.ANALYTICS;
```

---

### 3.2 Create raw ingestion table

```sql
CREATE OR REPLACE TABLE SCRAPE_PIPELINE.RAW.NASDAQ_STOCKS_RAW (
    symbol STRING,
    company_name STRING,
    price FLOAT,
    net_change FLOAT,
    change_percent FLOAT,
    market_cap FLOAT,
    category STRING,
    source_url STRING,
    scraped_at TIMESTAMP
);
```

---

### 3.3 Load CSV into Snowflake (UI method)

1. Open Snowflake UI
2. Navigate to: `SCRAPE_PIPELINE → RAW → NASDAQ_STOCKS_RAW`
3. Click **Load Data**
4. Upload `scraper/raw_data.csv`
5. Use default CSV options (header = true)
6. Complete the load

---

## 4. How to Run dbt Models

### 4.1 dbt Setup

Ensure `profiles.yml` exists at:
```
~/.dbt/profiles.yml
```

Profile name used in this project:
```yaml
dbt_project:
  target: dev
```

---

### 4.2 Project Structure

```
dbt_project/
├── staging/
│   ├── stg_nasdaq_stocks.sql
│   └── schema.yml
├── dimensions/
│   ├── dim_companies.sql
│   └── schema.yml
├── facts/
│   ├── fct_stock_observations.sql
│   └── schema.yml
└── dbt_project.yml
```

---

### 4.3 Run dbt models

```bash
cd dbt_project
dbt run
```

This creates:
- Staging views
- Dimension tables (with surrogate keys)
- Fact tables for analytics

---

### 4.4 Run dbt tests

```bash
dbt test
```

Tests include:
- not_null
- unique
- relationships (fact → dimension)

---

## 5. How to Run the Frontend App (Streamlit)

### 5.1 Environment Variables

Create a `.env` file in the `app/` directory:

```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_identifier
```

Add `.env` to `.gitignore`:

```gitignore
.env
```

---

### 5.2 Install frontend dependencies

```bash
cd app
pip install -r requirements.txt
```

---

### 5.3 Run Streamlit app

```bash
streamlit run app.py
```

The app will be available at:
```
http://localhost:8501
```

---

### 5.4 App Features

- Category dropdown (driven from Snowflake data)
- Minimum price filter
- Minimum percentage change filter
- “Run Query” button
- Displays top 20 stocks from analytics tables

Backend queries:
- `ANALYTICS.fct_stock_observations`
- `ANALYTICS.dim_companies`

---

## End-to-End Workflow Summary

1. Scrape stock data from Yahoo Finance  
2. Load raw CSV into Snowflake RAW schema  
3. Transform data using dbt into analytics tables  
4. Query analytics tables via Streamlit dashboard  

---

## Notes

- Snowflake credentials are never hardcoded
- dbt models follow staging → dimension → fact layering
- UI filters reflect only real modeled columns
- Entire pipeline is reproducible end-to-end
