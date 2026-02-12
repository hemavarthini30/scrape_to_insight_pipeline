SELECT
    d.company_sk,
    CAST(s.scraped_at AS DATE)      AS observation_date,
    s.price,
    s.net_change,
    s.change_percent,
    s.market_cap,
    s.source_url,
    s.scraped_at

FROM {{ ref('stg_nasdaq_stocks') }} s
JOIN {{ ref('dim_companies') }} d
    ON s.symbol = d.symbol
