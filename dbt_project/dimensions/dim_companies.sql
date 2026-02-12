SELECT DISTINCT
    ROW_NUMBER() OVER (ORDER BY symbol) AS company_sk,
    symbol,
    company_name,
    category

FROM {{ ref('stg_nasdaq_stocks') }}
