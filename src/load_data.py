"""
load_data.py
Cleans data/raw/Walmart.csv and loads it into db/walmart.db.

Run schema.py first, then this:
    python src/schema.py
    python src/load_data.py
"""

import os
import sqlite3
import pandas as pd

RAW_CSV_PATH = os.path.join("data", "raw", "Walmart.csv")
DB_PATH = os.path.join("db", "walmart.db")


def load_and_clean(csv_path: str = RAW_CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Standardize column names
    df = df.rename(
        columns={
            "Store": "store_id",
            "Date": "sale_date",
            "Weekly_Sales": "weekly_sales",
            "Holiday_Flag": "holiday_flag",
            "Temperature": "temperature",
            "Fuel_Price": "fuel_price",
            "CPI": "cpi",
            "Unemployment": "unemployment",
        }
    )

    # Parse dates (source format is DD-MM-YYYY)
    df["sale_date"] = pd.to_datetime(df["sale_date"], format="%d-%m-%Y")

    # Basic cleaning based on individual EDA findings
    df = df.drop_duplicates()
    df = df.dropna(subset=["store_id", "sale_date", "weekly_sales"])
    df = df[df["weekly_sales"] >= 0]

    # Store as ISO string for SQLite
    df["sale_date"] = df["sale_date"].dt.strftime("%Y-%m-%d")

    return df


def load_into_db(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)

    # Stores table: unique store ids
    stores = df[["store_id"]].drop_duplicates().sort_values("store_id")
    stores.to_sql("Stores", conn, if_exists="append", index=False)

    # Sales table: all weekly records
    sales_cols = [
        "store_id",
        "sale_date",
        "weekly_sales",
        "holiday_flag",
        "temperature",
        "fuel_price",
        "cpi",
        "unemployment",
    ]
    df[sales_cols].to_sql("Sales", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print(f"Loaded {len(stores)} stores and {len(df)} sales records into {db_path}")


def main():
    df = load_and_clean()
    load_into_db(df)

    # Quick sanity check
    conn = sqlite3.connect(DB_PATH)
    count = pd.read_sql("SELECT COUNT(*) AS n FROM Sales", conn).iloc[0, 0]
    print(f"Sanity check - rows in Sales table: {count}")
    conn.close()


if __name__ == "__main__":
    main()
