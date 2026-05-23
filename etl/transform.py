"""
etl/transform.py
================
SuperMart ETL Pipeline — TRANSFORM Stage
Cleans, validates, deduplicates, and enriches raw booking data.
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [TRANSFORM] %(message)s")
logger = logging.getLogger(__name__)

PROCESSED_DIR = Path("data/processed")

# ── SCHEMA ────────────────────────────────────────────────────────────────────
REQUIRED_COLUMNS = [
    "order_id", "date", "customer_name", "product_id",
    "product_name", "category", "qty", "unit_price",
    "total_price", "payment_method",
]

CATEGORY_MAP = {
    "veg": "vegetables", "vegetable": "vegetables",
    "fruit": "fruits",
    "milk": "dairy", "milk products": "dairy",
    "grain": "grains", "cereal": "grains",
    "snack": "snacks", "chips": "snacks",
}

# ── MAIN TRANSFORM ─────────────────────────────────────────────────────────────
def transform(df: pd.DataFrame) -> dict:
    """
    Full transformation pipeline.
    Returns dict with transformed DataFrames:
    {
        'orders':      order-level summary,
        'order_items': line-item detail,
        'daily_sales': daily aggregation,
        'category_sales': category aggregation,
    }
    """
    if df.empty:
        logger.warning("Empty DataFrame — nothing to transform.")
        return {}

    logger.info(f"🔧 Starting transform on {len(df)} rows...")

    df = _validate_schema(df)
    df = _clean_types(df)
    df = _clean_text(df)
    df = _fix_categories(df)
    df = _recalculate_financials(df)
    df = _add_enrichment_columns(df)
    df = _deduplicate(df)

    orders     = _build_orders_table(df)
    items      = _build_items_table(df)
    daily      = _build_daily_sales(df)
    category   = _build_category_sales(df)

    _save_processed(orders,   "orders")
    _save_processed(items,    "order_items")
    _save_processed(daily,    "daily_sales")
    _save_processed(category, "category_sales")

    logger.info(f"✅ TRANSFORM complete:")
    logger.info(f"   Orders:         {len(orders)} rows")
    logger.info(f"   Order Items:    {len(items)} rows")
    logger.info(f"   Daily Sales:    {len(daily)} rows")
    logger.info(f"   Category Sales: {len(category)} rows")

    return {
        "orders": orders,
        "order_items": items,
        "daily_sales": daily,
        "category_sales": category,
    }


# ── STEPS ──────────────────────────────────────────────────────────────────────
def _validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        logger.warning(f"⚠️  Missing columns: {missing} — filling with defaults")
        for c in missing:
            df[c] = np.nan
    return df


def _clean_types(df: pd.DataFrame) -> pd.DataFrame:
    df["date"]        = pd.to_datetime(df["date"], errors="coerce")
    df["qty"]         = pd.to_numeric(df["qty"], errors="coerce").fillna(0).astype(int)
    df["unit_price"]  = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce").fillna(0.0)
    df["tax"]         = pd.to_numeric(df.get("tax", 0), errors="coerce").fillna(0.0)
    # Drop rows with invalid dates or zero qty
    before = len(df)
    df = df.dropna(subset=["date"])
    df = df[df["qty"] > 0]
    logger.info(f"   Dropped {before - len(df)} invalid rows")
    return df


def _clean_text(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["customer_name", "product_name", "category", "payment_method"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    df["order_id"]    = df["order_id"].astype(str).str.strip().str.upper()
    df["product_id"]  = df["product_id"].astype(str).str.strip().str.upper()
    if "phone" in df.columns:
        df["phone"] = df["phone"].astype(str).str.replace(r"\D", "", regex=True)
    return df


def _fix_categories(df: pd.DataFrame) -> pd.DataFrame:
    df["category"] = df["category"].str.lower().map(
        lambda x: CATEGORY_MAP.get(x, x)
    )
    valid = {"vegetables", "fruits", "dairy", "grains", "snacks"}
    df.loc[~df["category"].isin(valid), "category"] = "other"
    return df


def _recalculate_financials(df: pd.DataFrame) -> pd.DataFrame:
    # Recalculate to ensure consistency
    df["unit_price"]  = df["unit_price"].round(2)
    df["total_price"] = (df["qty"] * df["unit_price"]).round(2)
    df["tax"]         = (df["total_price"] * 0.05).round(2)
    df["net_total"]   = (df["total_price"] + df["tax"]).round(2)
    return df


def _add_enrichment_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["year"]         = df["date"].dt.year
    df["month"]        = df["date"].dt.month
    df["month_name"]   = df["date"].dt.strftime("%B")
    df["day_of_week"]  = df["date"].dt.day_name()
    df["week_number"]  = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekend"]   = df["date"].dt.dayofweek >= 5

    # Revenue tier
    df["revenue_tier"] = pd.cut(
        df["net_total"],
        bins=[0, 100, 300, 600, float("inf")],
        labels=["Low", "Medium", "High", "Premium"],
    )

    df["etl_loaded_at"] = datetime.now().isoformat()
    return df


def _deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["order_id", "product_id"], keep="last")
    logger.info(f"   Deduplication: removed {before - len(df)} duplicates")
    return df


# ── AGGREGATIONS ───────────────────────────────────────────────────────────────
def _build_orders_table(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("order_id")
        .agg(
            order_date    = ("date", "first"),
            customer_name = ("customer_name", "first"),
            phone         = ("phone", "first") if "phone" in df.columns else ("order_id", "first"),
            payment_method= ("payment_method", "first"),
            total_items   = ("qty", "sum"),
            subtotal      = ("total_price", "sum"),
            tax           = ("tax", "sum"),
            order_total   = ("net_total", "sum"),
        )
        .reset_index()
    )


def _build_items_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["order_id","date","product_id","product_name","category",
            "qty","unit_price","total_price","tax","net_total",
            "year","month","day_of_week","revenue_tier","etl_loaded_at"]
    return df[[c for c in cols if c in df.columns]].reset_index(drop=True)


def _build_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["date","category"])
        .agg(
            total_orders  = ("order_id", "nunique"),
            total_qty     = ("qty", "sum"),
            gross_revenue = ("total_price", "sum"),
            tax_collected = ("tax", "sum"),
            net_revenue   = ("net_total", "sum"),
            avg_order_val = ("net_total", "mean"),
        )
        .reset_index()
        .sort_values("date")
    )


def _build_category_sales(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["category","product_name"])
        .agg(
            total_qty     = ("qty", "sum"),
            gross_revenue = ("total_price", "sum"),
            net_revenue   = ("net_total", "sum"),
            order_count   = ("order_id", "nunique"),
            avg_unit_price= ("unit_price", "mean"),
        )
        .reset_index()
        .sort_values("net_revenue", ascending=False)
    )


# ── SAVE ───────────────────────────────────────────────────────────────────────
def _save_processed(df: pd.DataFrame, name: str) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / f"{name}_{datetime.today().strftime('%Y%m%d')}.csv"
    df.to_csv(path, index=False)
    logger.info(f"   💾 Saved {name} → {path}")


if __name__ == "__main__":
    from extract import extract_sample_data
    raw = extract_sample_data()
    results = transform(raw)
    print("\n--- ORDERS TABLE ---")
    print(results["orders"].head(5).to_string())
    print("\n--- DAILY SALES ---")
    print(results["daily_sales"].head(5).to_string())
