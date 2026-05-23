"""
etl/load.py
===========
SuperMart ETL Pipeline — LOAD Stage
Loads transformed DataFrames into SQL Database (SQLite default / PostgreSQL for production).
"""

import logging
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [LOAD] %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = Path("database/supermart.db")


# ── SCHEMA DDL ─────────────────────────────────────────────────────────────────
SCHEMA_SQL = """
-- Orders summary table
CREATE TABLE IF NOT EXISTS orders (
    order_id        TEXT PRIMARY KEY,
    order_date      DATE NOT NULL,
    customer_name   TEXT,
    phone           TEXT,
    payment_method  TEXT,
    total_items     INTEGER,
    subtotal        REAL,
    tax             REAL,
    order_total     REAL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Line items table
CREATE TABLE IF NOT EXISTS order_items (
    item_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        TEXT NOT NULL,
    order_date      DATE,
    product_id      TEXT,
    product_name    TEXT,
    category        TEXT,
    qty             INTEGER,
    unit_price      REAL,
    total_price     REAL,
    tax             REAL,
    net_total       REAL,
    year            INTEGER,
    month           INTEGER,
    day_of_week     TEXT,
    revenue_tier    TEXT,
    etl_loaded_at   TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Daily sales aggregation (for Power BI)
CREATE TABLE IF NOT EXISTS daily_sales (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_date       DATE NOT NULL,
    category        TEXT NOT NULL,
    total_orders    INTEGER,
    total_qty       INTEGER,
    gross_revenue   REAL,
    tax_collected   REAL,
    net_revenue     REAL,
    avg_order_val   REAL,
    loaded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Category sales aggregation (for Power BI)
CREATE TABLE IF NOT EXISTS category_sales (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category        TEXT,
    product_name    TEXT,
    total_qty       INTEGER,
    gross_revenue   REAL,
    net_revenue     REAL,
    order_count     INTEGER,
    avg_unit_price  REAL,
    loaded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ETL run log
CREATE TABLE IF NOT EXISTS etl_run_log (
    run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    stage           TEXT,
    rows_processed  INTEGER,
    status          TEXT,
    notes           TEXT
);
"""

# ── VIEWS (for Power BI DirectQuery) ──────────────────────────────────────────
VIEWS_SQL = """
CREATE VIEW IF NOT EXISTS vw_daily_revenue AS
SELECT
    sale_date,
    SUM(net_revenue)   AS total_revenue,
    SUM(total_orders)  AS total_orders,
    SUM(total_qty)     AS total_qty,
    AVG(avg_order_val) AS avg_order_value
FROM daily_sales
GROUP BY sale_date
ORDER BY sale_date;

CREATE VIEW IF NOT EXISTS vw_top_products AS
SELECT
    product_name,
    category,
    SUM(total_qty)     AS units_sold,
    SUM(net_revenue)   AS revenue,
    AVG(avg_unit_price)AS avg_price
FROM category_sales
GROUP BY product_name, category
ORDER BY revenue DESC;

CREATE VIEW IF NOT EXISTS vw_payment_analysis AS
SELECT
    payment_method,
    COUNT(*)            AS order_count,
    SUM(order_total)    AS total_revenue,
    AVG(order_total)    AS avg_order_value,
    MIN(order_total)    AS min_order,
    MAX(order_total)    AS max_order
FROM orders
GROUP BY payment_method;
"""


# ── PUBLIC API ─────────────────────────────────────────────────────────────────
def load(transformed_data: dict, db_path: str = None) -> dict:
    """
    Load all transformed tables into SQLite database.

    Args:
        transformed_data: dict from transform.py  {table_name: DataFrame}
        db_path:          override default DB path

    Returns:
        dict with load statistics
    """
    path = Path(db_path) if db_path else DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    stats = {}

    with sqlite3.connect(path) as conn:
        _initialize_schema(conn)

        table_map = {
            "orders":         "orders",
            "order_items":    "order_items",
            "daily_sales":    "daily_sales",
            "category_sales": "category_sales",
        }

        for key, table in table_map.items():
            df = transformed_data.get(key)
            if df is None or df.empty:
                logger.warning(f"⚠️  No data for table '{table}' — skipping")
                continue
            rows = _upsert_table(conn, df, table)
            stats[table] = rows
            _log_run(conn, table, rows, "SUCCESS")

        conn.commit()

    total = sum(stats.values())
    logger.info(f"🗄️  LOAD complete → {path}")
    logger.info(f"   Total rows inserted/updated: {total}")
    for t, r in stats.items():
        logger.info(f"   {t:20s}: {r} rows")

    return stats


def _initialize_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    cursor.executescript(VIEWS_SQL)
    conn.commit()
    logger.info("🏗️  Schema initialized")


def _upsert_table(conn: sqlite3.Connection, df: pd.DataFrame, table: str) -> int:
    """
    Load DataFrame into table using INSERT OR REPLACE for idempotency.
    Clears daily aggregation tables first (replace strategy).
    """
    # Convert date columns to string for SQLite
    df = df.copy()
    for col in df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        df[col] = df[col].dt.strftime("%Y-%m-%d")

    # Convert categoricals
    for col in df.select_dtypes(include=["category"]).columns:
        df[col] = df[col].astype(str)

    # For aggregation tables, clear today's data first (idempotent reload)
    if table in ("daily_sales", "category_sales"):
        today = datetime.today().strftime("%Y-%m-%d")
        conn.execute(f"DELETE FROM {table} WHERE date(loaded_at) = '{today}'")

    try:
        df.to_sql(table, conn, if_exists="append", index=False, method="multi")
        logger.info(f"   ✅ {table}: {len(df)} rows loaded")
        return len(df)
    except Exception as e:
        logger.error(f"   ❌ Error loading {table}: {e}")
        return 0


def _log_run(conn: sqlite3.Connection, stage: str, rows: int, status: str) -> None:
    conn.execute(
        "INSERT INTO etl_run_log (stage, rows_processed, status) VALUES (?,?,?)",
        (stage, rows, status),
    )


def get_summary(db_path: str = None) -> pd.DataFrame:
    """Query the DB and return a quick summary for validation."""
    path = Path(db_path) if db_path else DB_PATH
    if not path.exists():
        return pd.DataFrame()

    with sqlite3.connect(path) as conn:
        summary = {}
        for table in ["orders", "order_items", "daily_sales", "category_sales"]:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                summary[table] = count
            except Exception:
                summary[table] = 0

    return pd.DataFrame([summary])


if __name__ == "__main__":
    from extract import extract_sample_data
    from transform import transform
    raw = extract_sample_data()
    transformed = transform(raw)
    stats = load(transformed)
    print("\n✅ Load Stats:", stats)
    print("\n📊 DB Summary:")
    print(get_summary())
