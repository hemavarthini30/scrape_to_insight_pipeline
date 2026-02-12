import os
import streamlit as st
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse="COMPUTE_WH",
        database="SCRAPE_PIPELINE",
        schema="ANALYTICS",
        role="SYSADMIN"
    )

st.set_page_config(page_title="Market Analytics Dashboard", layout="wide")

st.title("📊 Market Analytics Dashboard")
st.caption("Analytics on dbt-transformed Snowflake fact & dimension tables")

conn = get_connection()
category_df = pd.read_sql(
    """
    SELECT DISTINCT category
    FROM ANALYTICS.dim_companies
    WHERE category IS NOT NULL
    ORDER BY category
    """,
    conn
)
conn.close()

categories = category_df["CATEGORY"].tolist()

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

min_price = st.sidebar.number_input(
    "Minimum Price",
    min_value=0.0,
    value=0.0,
    step=10.0
)

min_change_pct = st.sidebar.number_input(
    "Minimum % Change",
    min_value=0.0,
    value=0.0,
    step=1.0
)

run_query = st.sidebar.button("Run Query")

if run_query:
    st.info("Running query...")

    conn = get_connection()

    sql = """
        SELECT
            c.symbol,
            c.company_name,
            c.category,
            f.price,
            f.net_change,
            f.change_percent,
            f.observation_date
        FROM ANALYTICS.fct_stock_observations f
        JOIN ANALYTICS.dim_companies c
            ON f.company_sk = c.company_sk
        WHERE c.category = %(category)s
          AND f.price >= %(min_price)s
          AND ABS(f.change_percent) >= %(min_change_pct)s
        ORDER BY ABS(f.change_percent) DESC
        LIMIT 20
    """

    params = {
        "category": selected_category,
        "min_price": min_price,
        "min_change_pct": min_change_pct
    }

    df = pd.read_sql(sql, conn, params=params)
    conn.close()

    if df.empty:
        st.warning("No results found for the selected filters.")
    else:
        st.success(f"Showing top {len(df)} results")
        st.dataframe(df, use_container_width=True)
