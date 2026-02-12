WITH source AS (

    SELECT *
    FROM {{ source('raw', 'nasdaq_stocks_raw') }}

)

SELECT
    SYMBOL                          AS symbol,
    COMPANY_NAME                    AS company_name,
    CAST(PRICE AS FLOAT)            AS price,
    CAST(NET_CHANGE AS FLOAT)       AS net_change,
    CAST(CHANGE_PERCENT AS FLOAT)   AS change_percent,
    CAST(MARKET_CAP AS FLOAT)       AS market_cap,
    CATEGORY                        AS category,
    SOURCE_URL                      AS source_url,
    SCRAPED_AT                      AS scraped_at

FROM source
WHERE SYMBOL IS NOT NULL
