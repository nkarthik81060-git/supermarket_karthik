# 🛒 SuperMart Daily — ETL Pipeline Project

> **End-to-end data engineering project**: HTML booking form → CSV Extract → Python/Pandas Transform → SQL Load → Power BI Reports

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas)](https://pandas.pydata.org)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)](https://sqlite.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)

---

## 📐 Architecture

```
📥 Extract          🔧 Transform         🗄️ Load            📊 Report
─────────────────   ──────────────────   ───────────────    ──────────────
HTML Booking Form → CSV Raw Data     →  Python + Pandas  → SQL Database → Power BI
(templates/)        (data/raw/*.csv)     (etl/transform)   (supermart.db)  (Dashboard)
```

## 📁 Project Structure

```
supermarket_karthik/
│
├── templates/
│   └── index.html          ← Daily product booking UI (HTML/CSS/JS)
│
├── etl/
│   ├── extract.py          ← Stage 1: Read CSV files
│   ├── transform.py        ← Stage 2: Clean & enrich with Pandas
│   ├── load.py             ← Stage 3: Insert into SQLite/PostgreSQL
│   └── pipeline.py         ← Orchestrator: runs all 3 stages
│
├── database/
│   └── schema.sql          ← Full DDL + Power BI views
│
├── data/
│   ├── raw/                ← CSV files from HTML form (auto-created)
│   └── processed/          ← Transformed CSVs (auto-created)
│
├── reports/
│   └── powerbi_guide.md    ← Power BI connection & dashboard guide
│
├── app.py                  ← Flask server (serves form + receives bookings)
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/nkarthik81060-git/supermarket_karthik
cd supermarket_karthik
pip install -r requirements.txt
```

### 2. Run the Web App
```bash
python app.py
# Open http://localhost:5000
```

### 3. Book Products
- Open the browser, select daily products, fill customer details
- Click **BOOK & EXTRACT DATA**
- CSV is saved to `data/raw/bookings_YYYY-MM-DD.csv`

### 4. Run ETL Pipeline
```bash
# With sample data (for testing)
python -m etl.pipeline --sample

# Process today's bookings
python -m etl.pipeline

# Process specific date
python -m etl.pipeline --date 2025-01-15
```

### 5. Connect Power BI
1. Open Power BI Desktop
2. **Get Data → SQLite** (or ODBC) → select `database/supermart.db`
3. Load views: `vw_daily_revenue`, `vw_top_products`, `vw_payment_analysis`
4. Build dashboards from pre-built views

---

## 🔧 ETL Pipeline Details

### Stage 1 — Extract (`etl/extract.py`)
- Reads all `*.csv` from `data/raw/`
- Supports date filtering
- Combines multiple files into single DataFrame

### Stage 2 — Transform (`etl/transform.py`)
| Step | Action |
|------|--------|
| Schema validation | Check required columns, fill missing |
| Type coercion | Parse dates, numeric types |
| Text cleaning | Strip whitespace, title-case names |
| Category normalization | Map aliases → standard categories |
| Financial recalculation | Recalculate total = qty × price + 5% tax |
| Enrichment | Add year, month, day_of_week, revenue_tier |
| Deduplication | Remove duplicate order+product pairs |
| Aggregation | Build daily_sales, category_sales tables |

### Stage 3 — Load (`etl/load.py`)
- **Target DB**: SQLite (`database/supermart.db`) — swap for PostgreSQL in production
- **Strategy**: Idempotent — daily aggregations replaced, items appended
- **Tables**: `orders`, `order_items`, `daily_sales`, `category_sales`, `etl_run_log`
- **Views**: Pre-built SQL views for Power BI DirectQuery

---

## 📊 Power BI Views

| View | Purpose |
|------|---------|
| `vw_daily_revenue` | Revenue trend by date |
| `vw_category_performance` | Sales by product category |
| `vw_top_products` | Top 20 products by revenue |
| `vw_payment_analysis` | Payment method breakdown |
| `vw_weekly_kpis` | Weekly aggregated KPIs |

---

## 🛒 Products Covered

| Category | Products |
|----------|---------|
| 🥦 Vegetables | Tomato, Onion, Potato, Spinach, Carrot, Capsicum |
| 🍎 Fruits | Apple, Banana, Mango, Grapes |
| 🥛 Dairy | Milk, Curd, Paneer, Butter |
| 🌾 Grains | Rice, Wheat, Dal, Poha |
| 🍪 Snacks | Biscuits, Chips |

---

## 👤 Author
**Karthik** — [GitHub: nkarthik81060-git](https://github.com/nkarthik81060-git)
