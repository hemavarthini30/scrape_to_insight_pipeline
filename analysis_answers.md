# Part B – Business Insights, Automation & LLM Design

## B1) Dashboard Design

__Dashboard Title:__  
Daily US Stock Market Performance Dashboard

__Target Stakeholder:__  
Finance leadership / strategy team

__Reasoning:__  
The stakeholder needs a quick daily view of market behavior, key movers, and potential risk or opportunity areas.

### Key KPIs
1. Average daily stock price  
2. Total market capitalization  
3. Average daily percentage change  
4. Number of companies tracked  
5. Top gainers (by % change)  
6. Top losers (by % change)  

### Visuals
- Line chart: average stock price over time  
- Bar chart: top 10 companies by market cap  
- Table: top gainers and losers  
- Distribution chart: daily % price change  
- KPI cards: market summary  
- Heatmap: company vs % change  

### Filters
- Date  
- Company symbol  
- Category  

---

## B2) Stakeholder Insights

### Obvious Insights
- Identify the highest market-cap companies  
- See which stocks gained or dropped the most  
- Understand the overall market direction  
- Track daily company coverage  

### Non-Obvious Insights
- Detect unusually volatile stocks  
- Identify market concentration risk  
- Spot early trend reversals with historical data  
- Find consistent over- and under-performers  

---

## B3) Data Quality & Reliability

### Data Quality Checks
- Not-null checks on price, symbol, and date  
- Duplicate detection using symbol + date  
- Referential integrity between fact and dimension tables  
- Validation for invalid or negative price values  
- Monitoring daily row counts to detect scraping failures  

### Historical Handling
- Append-only fact table  
- Historical data is never overwritten  

---

## B4) LLM Use Cases

### Use Case 1: Automated Market Summary
The LLM generates a plain-English summary of daily market performance using aggregated metrics, top gainers, and top losers.

__Risk:__ Hallucination  
__Mitigation:__ Restrict LLM input strictly to SQL query results  

### Use Case 2: Anomaly Explanation Assistant
When a stock shows an unusual price change, the LLM provides a possible explanation based on historical patterns.

__Risk:__ Speculation  
__Mitigation:__ Clearly label outputs as hypotheses, not facts  

---

## B5) n8n Automation Workflow

__Trigger:__  
Daily scheduled execution  

__Workflow Steps:__
1. Run dbt models  
2. Detect price anomalies  
3. Rank top volatile stocks  
4. Generate summary using LLM  
5. Send report via email or Slack  

__Failure Handling:__
- Retry failed steps  
- Notify data team on repeated failure  

__False Positive Control:__
- Require anomalies to persist across multiple days  

---

## B6) Client Summary

This project delivers an automated data pipeline that collects public stock market data, stores it in Snowflake, and transforms it using dbt into analytics-ready tables. The solution enables daily monitoring of market trends, company performance, and volatility without manual effort.

With additional historical data, the system can support deeper trend analysis, anomaly detection, and executive reporting. Future enhancements include dashboards, alerting, and AI-assisted insights.
