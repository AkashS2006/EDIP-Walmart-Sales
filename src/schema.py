"""
schema.py
Creates the SQLite database and tables for the Walmart Sales project.

Tables:
    Stores - one row per store
    Sales  - one row per store per week

Run this once before load_data.py:
    python src/schema.py
"""

import sqlite3
import os

DB_PATH = os.path.join("db", "walmart.db")


def create_schema(db_path: str = DB_PATH) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS Stores (
            store_id INTEGER PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS Sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            sale_date TEXT NOT NULL,
            weekly_sales REAL,
            holiday_flag INTEGER,
            temperature REAL,
            fuel_price REAL,
            cpi REAL,
            unemployment REAL,
            FOREIGN KEY (store_id) REFERENCES Stores(store_id)
        );

        CREATE INDEX IF NOT EXISTS idx_sales_store_date
            ON Sales (store_id, sale_date);
        """
    )

    conn.commit()
    conn.close()
    print(f"Schema created successfully at {db_path}")


if __name__ == "__main__":
    create_schema()
