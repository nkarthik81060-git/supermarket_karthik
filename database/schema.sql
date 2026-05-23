-- ============================================================
-- SuperMart ETL — Database Schema
-- Compatible: SQLite (dev) / PostgreSQL (production)
-- ============================================================

-- Orders table (one row per order)
CREATE TABLE IF NOT EXISTS orders (
    order_id        TEXT        PRIMARY KEY,
    order_date      DATE        NOT NULL,
    customer_name   TEXT,
    phone           TEXT,
    payment_method  TEXT        CHECK(payment_method IN ('cash','upi','card','wallet')),
    total_items     INTEGER     DEFAULT 0,
    subtotal        REAL        DEFAULT 0.0,
    tax             REAL        DEFAULT 0.0,
    order_total     REAL        DEFAULT 0.0,
    created_at      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- Order items (line-level detail)
CREATE TABLE IF NOT EXISTS order_items (
    item_id         INTEGER     PRIMARY KEY AUTOINCREMENT,
    order_id        TEXT        NOT NULL REFERENCES orders(order_id),
    order_date      DATE,
    product_id      TEXT        NOT NULL,
    product_name    TEXT,
    category        TEXT        CHECK(category IN ('vegetables','fruits','dairy','grains','snacks','other')),
    qty             INTEGER     DEFAULT 1,
    unit_price      REAL        DEFAULT 0.0,
    total_price     REAL        DEFAULT 0.0,
    tax             REAL        DEFAULT 0.0,
    net_total       REAL        DEFAULT 0.0,
    year            INTEGER,
    month           INTEGER,
    day_of_week     TEXT,
    revenue_tier    TEXT,
    etl_loaded_at   TIMESTAMP
);

-- Daily aggregated sales (Power BI source)
CREATE TABLE IF NOT EXISTS daily_sales (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    sale_date       DATE        NOT NULL,
    category        TEXT        NOT NULL,
    total_orders    INTEGER     DEFAULT 0,
    total_qty       INTEGER     DEFAULT 0,
    gross_revenue   REAL        DEFAULT 0.0,
    tax_collected   REAL        DEFAULT 0.0,
    net_revenue     REAL        DEFAULT 0.0,
    avg_order_val   REAL        DEFAULT 0.0,
    loaded_at       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- Category / product aggregation
CREATE TABLE IF NOT EXISTS category_sales (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    category        TEXT,
    product_name    TEXT,
    total_qty       INTEGER     DEFAULT 0,
    gross_revenue   REAL        DEFAULT 0.0,
    net_revenue     REAL        DEFAULT 0.0,
    order_count     INTEGER     DEFAULT 0,
    avg_unit_price  REAL        DEFAULT 0.0,
    loaded_at       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- ETL run audit log
CREATE TABLE IF NOT EXISTS etl_run_log (
    run_id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    run_date        TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    stage           TEXT,
    rows_processed  INTEGER,
    status          TEXT,
    notes           TEXT
);

-- ============================================================
-- VIEWS FOR POWER BI
-- ============================================================

-- Daily revenue trend
CREATE VIEW IF NOT EXISTS vw_daily_revenue AS
SELECT
    sale_date                       AS "Date",
    SUM(net_revenue)                AS "Total Revenue (₹)",
    SUM(total_orders)               AS "Total Orders",
    SUM(total_qty)                  AS "Units Sold",
    ROUND(AVG(avg_order_val), 2)    AS "Avg Order Value"
FROM daily_sales
GROUP BY sale_date
ORDER BY sale_date;

-- Category performance
CREATE VIEW IF NOT EXISTS vw_category_performance AS
SELECT
    category                        AS "Category",
    SUM(total_qty)                  AS "Units Sold",
    SUM(net_revenue)                AS "Revenue (₹)",
    COUNT(DISTINCT product_name)    AS "Product Count"
FROM category_sales
GROUP BY category
ORDER BY "Revenue (₹)" DESC;

-- Top products
CREATE VIEW IF NOT EXISTS vw_top_products AS
SELECT
    product_name                    AS "Product",
    category                        AS "Category",
    SUM(total_qty)                  AS "Units Sold",
    ROUND(SUM(net_revenue), 2)      AS "Revenue (₹)",
    ROUND(AVG(avg_unit_price), 2)   AS "Avg Price"
FROM category_sales
GROUP BY product_name, category
ORDER BY "Revenue (₹)" DESC
LIMIT 20;

-- Payment method analysis
CREATE VIEW IF NOT EXISTS vw_payment_analysis AS
SELECT
    payment_method                  AS "Payment Method",
    COUNT(*)                        AS "Orders",
    ROUND(SUM(order_total), 2)      AS "Total Revenue",
    ROUND(AVG(order_total), 2)      AS "Avg Order Value"
FROM orders
GROUP BY payment_method;

-- Weekly KPIs
CREATE VIEW IF NOT EXISTS vw_weekly_kpis AS
SELECT
    strftime('%Y-W%W', sale_date)   AS "Week",
    SUM(net_revenue)                AS "Weekly Revenue",
    SUM(total_orders)               AS "Weekly Orders",
    SUM(total_qty)                  AS "Weekly Units",
    ROUND(AVG(avg_order_val), 2)    AS "Avg Order Value"
FROM daily_sales
GROUP BY strftime('%Y-W%W', sale_date)
ORDER BY "Week";
