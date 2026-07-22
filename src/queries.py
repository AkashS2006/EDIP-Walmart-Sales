"""
Week 2 — Core SQL Queries for Walmart Sales Analysis
======================================================
Reusable, documented query functions against db/walmart.db (table: Sales).

Usage:
    import sqlite3
    from src.queries import *

    conn = sqlite3.connect("db/walmart.db")
    df = total_sales_by_store(conn)

Table schema (Sales):
    store_id       INTEGER   -- store number
    sale_date      TEXT/DATE -- weekly sale date (YYYY-MM-DD)
    weekly_sales   REAL      -- total sales for that store that week
    holiday_flag   INTEGER   -- 1 if the week includes a holiday, else 0
    temperature    REAL      -- avg temperature that week (F)
    fuel_price     REAL      -- fuel price that week
    cpi            REAL      -- consumer price index
    unemployment   REAL      -- unemployment rate
"""

import pandas as pd


# ---------------------------------------------------------------------------
# 1. Total sales per store
# ---------------------------------------------------------------------------
def total_sales_by_store(conn):
    """Total weekly_sales summed per store, highest first."""
    query = """
        SELECT store_id, SUM(weekly_sales) AS total_sales
        FROM Sales
        GROUP BY store_id
        ORDER BY total_sales DESC
    """
    return pd.read_sql(query, conn)


# ---------------------------------------------------------------------------
# 2. Average weekly sales: holiday vs non-holiday
# ---------------------------------------------------------------------------
def avg_sales_holiday_vs_normal(conn):
    """Average weekly sales split by holiday_flag (0 = normal week, 1 = holiday week)."""
    query = """
        SELECT holiday_flag, AVG(weekly_sales) AS avg_sales
        FROM Sales
        GROUP BY holiday_flag
    """
    return pd.read_sql(query, conn)


# ---------------------------------------------------------------------------
# 3. Top N performing stores
# ---------------------------------------------------------------------------
def top_stores(conn, n=5):
    """Top N stores by total sales."""
    query = f"""
        SELECT store_id, SUM(weekly_sales) AS total_sales
        FROM Sales
        GROUP BY store_id
        ORDER BY total_sales DESC
        LIMIT {n}
    """
    return pd.read_sql(query, conn)


# ---------------------------------------------------------------------------
# 4. Bottom N (worst) performing stores
# ---------------------------------------------------------------------------
def worst_stores(conn, n=5):
    """Bottom N stores by total sales."""
    query = f"""
        SELECT store_id, SUM(weekly_sales) AS total_sales
        FROM Sales
        GROUP BY store_id
        ORDER BY total_sales ASC
        LIMIT {n}
    """
    return pd.read_sql(query, conn)


# ---------------------------------------------------------------------------
# 5. Monthly sales trend (across all stores)
# ---------------------------------------------------------------------------
def monthly_sales_trend(conn):
    """Total sales grouped by calendar month (YYYY-MM), across all stores."""
    query = """
        SELECT strftime('%Y-%m', sale_date) AS month, SUM(weekly_sales) AS total_sales
        FROM Sales
        GROUP BY month
        ORDER BY month
    """
    return pd.read_sql(query, conn)


# ---------------------------------------------------------------------------
# 6. Year-over-year total sales
# ---------------------------------------------------------------------------
def yearly_sales_trend(conn):
    """Total sales grouped by year, to compare 2010 vs 2011 vs 2012."""
    query = """
        SELECT strftime('%Y', sale_date) AS year, SUM(weekly_sales) AS total_sales
        FROM Sales
        GROUP BY year
        ORDER BY year
    """
    return pd.read_sql(query, conn)


# ---------------------------------------------------------------------------
# 7. Per-store monthly trend (for growth/decline analysis)
# ---------------------------------------------------------------------------
def store_monthly_trend(conn, store_id=None):
    """
    Monthly sales trend per store. If store_id is given, filters to that store;
    otherwise returns all stores (store_id, month, total_sales).
    """
    if store_id is not None:
        query = f"""
            SELECT store_id, strftime('%Y-%m', sale_date) AS month, SUM(weekly_sales) AS total_sales
            FROM Sales
            WHERE store_id = {int(store_id)}
            GROUP BY store_id, month
            ORDER BY month
        """
    else:
        query = """
            SELECT store_id, strftime('%Y-%m', sale_date) AS month, SUM(weekly_sales) AS total_sales
            FROM Sales
            GROUP BY store_id, month
            ORDER BY store_id, month
        """
    return pd.read_sql(query, conn)


# ---------------------------------------------------------------------------
# 8. Holiday sensitivity per store
#    (avg holiday sales vs avg non-holiday sales, and the % lift)
# ---------------------------------------------------------------------------
def holiday_sensitivity_by_store(conn):
    """
    For each store: average sales on holiday weeks vs non-holiday weeks,
    and the % lift holidays give. Highest lift = most holiday-sensitive.
    """
    query = """
        SELECT
            store_id,
            AVG(CASE WHEN holiday_flag = 1 THEN weekly_sales END) AS avg_holiday_sales,
            AVG(CASE WHEN holiday_flag = 0 THEN weekly_sales END) AS avg_normal_sales
        FROM Sales
        GROUP BY store_id
    """
    df = pd.read_sql(query, conn)
    df["pct_lift"] = (
        (df["avg_holiday_sales"] - df["avg_normal_sales"]) / df["avg_normal_sales"] * 100
    )
    return df.sort_values("pct_lift", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 9. Store performance tiers (high / medium / low)
#    Done in pandas since SQLite lacks NTILE in older builds; pure-SQL version
#    included below as a comment for reference.
# ---------------------------------------------------------------------------
def store_performance_tiers(conn, n_tiers=3, labels=("Low", "Medium", "High")):
    """
    Buckets stores into performance tiers based on total sales using
    pandas.qcut (equal-sized quantile buckets).
    """
    totals = total_sales_by_store(conn)
    totals["tier"] = pd.qcut(totals["total_sales"], q=n_tiers, labels=labels)
    return totals.sort_values("total_sales", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 10. Full raw table loader (for correlation / pandas-side analysis)
# ---------------------------------------------------------------------------
def load_full_table(conn):
    """Load the entire Sales table into a DataFrame, e.g. for df.corr()."""
    return pd.read_sql("SELECT * FROM Sales", conn, parse_dates=["sale_date"])


if __name__ == "__main__":
    import sqlite3

    conn = sqlite3.connect("db/walmart.db")
    print("Top 5 stores:\n", top_stores(conn))
    print("\nHoliday vs non-holiday avg sales:\n", avg_sales_holiday_vs_normal(conn))
    print("\nMonthly trend (head):\n", monthly_sales_trend(conn).head())
    conn.close()
