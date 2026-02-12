
-- 1.Top 10 entites by a chosen metric

SELECT
    d.company_name,
    d.symbol,
    AVG(f.price) AS avg_price
FROM ANALYTICS.fct_stock_observations f
JOIN ANALYTICS.dim_companies d
    ON f.company_sk = d.company_sk
GROUP BY d.company_name, d.symbol
ORDER BY avg_price DESC
LIMIT 10;


-- 2. Metric trend over time (daily or weekly)

SELECT
    observation_date,
    AVG(price) AS avg_daily_price,
    COUNT(DISTINCT company_sk) AS companies_tracked
FROM ANALYTICS.fct_stock_observations
GROUP BY observation_date
ORDER BY observation_date;


-- 3. Outlier detection on query (percentile or z-score)

WITH price_percentile AS (
    SELECT
        PERCENTILE_CONT(0.95) 
        WITHIN GROUP (ORDER BY price) AS p95_price
    FROM ANALYTICS.fct_stock_observations
)

SELECT
    d.company_name,
    d.symbol,
    f.price,
    f.observation_date
FROM ANALYTICS.fct_stock_observations f
JOIN ANALYTICS.dim_companies d
    ON f.company_sk = d.company_sk
CROSS JOIN price_percentile p
WHERE f.price > p.p95_price
ORDER BY f.price DESC;


-- 4. Geographic breakdown (country or region)--category breakdown in this case

SELECT
    d.category,
    COUNT(DISTINCT d.company_sk) AS company_count,
    AVG(f.price) AS avg_price
FROM ANALYTICS.fct_stock_observations f
JOIN ANALYTICS.dim_companies d
    ON f.company_sk = d.company_sk
GROUP BY d.category
ORDER BY avg_price DESC;


-- 5. A stakeholder-driven query that would realis cally be requested
-- Which stocks show the highest price volatility?

SELECT
    d.company_name,
    d.symbol,
    STDDEV(f.price) AS price_volatility
FROM ANALYTICS.fct_stock_observations f
JOIN ANALYTICS.dim_companies d
    ON f.company_sk = d.company_sk
GROUP BY d.company_name, d.symbol
ORDER BY price_volatility DESC
LIMIT 10;
