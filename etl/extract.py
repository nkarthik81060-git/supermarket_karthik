"""
etl/extract.py
==============
SuperMart ETL Pipeline — EXTRACT Stage
Reads raw CSV bookings captured from the HTML booking form.
"""

import os
import glob
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [EXTRACT] %(message)s")
logger = logging.getLogger(__name__)

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def extract_csv_files(date_filter: str = None) -> pd.DataFrame:
    """
    Extract all CSV files from the raw data directory.
    Optionally filter by date (YYYY-MM-DD).

    Returns a combined DataFrame of all raw bookings.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    pattern = str(RAW_DATA_DIR / "*.csv")
    files = glob.glob(pattern)

    if not files:
        logger.warning(f"No CSV files found in {RAW_DATA_DIR}")
        return pd.DataFrame()

    frames = []
    for f in files:
        try:
            df = pd.read_csv(f)
            df["source_file"] = os.path.basename(f)
            frames.append(df)
            logger.info(f"✅ Extracted: {f}  ({len(df)} rows)")
        except Exception as e:
            logger.error(f"❌ Failed to read {f}: {e}")

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)

    # Optional date filter
    if date_filter and "date" in combined.columns:
        combined["date"] = pd.to_datetime(combined["date"], errors="coerce")
        combined = combined[combined["date"].dt.strftime("%Y-%m-%d") == date_filter]
        logger.info(f"🔍 Filtered to date={date_filter}: {len(combined)} rows")

    logger.info(f"📥 EXTRACT complete: {len(combined)} total rows from {len(frames)} file(s)")
    return combined


def extract_sample_data() -> pd.DataFrame:
    """Generate sample data for testing the pipeline."""
    import random

    products = [
        ("P001","Tomato","vegetables",25,"kg"),
        ("P002","Onion","vegetables",30,"kg"),
        ("P003","Potato","vegetables",20,"kg"),
        ("P007","Apple","fruits",120,"kg"),
        ("P008","Banana","fruits",40,"dozen"),
        ("P011","Milk","dairy",55,"ltr"),
        ("P012","Curd","dairy",45,"500g"),
        ("P015","Rice","grains",65,"kg"),
        ("P017","Dal","grains",95,"kg"),
        ("P019","Biscuits","snacks",20,"pack"),
    ]
    payment_methods = ["cash","upi","card","wallet"]
    customers = [
        ("Arjun Kumar","9876543210"),("Priya Sharma","9123456789"),
        ("Rahul Singh","9988776655"),("Deepa Nair","9871234560"),
        ("Kiran Reddy","9012345678"),
    ]

    rows = []
    for day_offset in range(7):  # 7 days of sample data
        date = (datetime.today() - pd.Timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for _ in range(random.randint(15, 30)):
            order_id = f"ORD{date.replace('-','')}_{random.randint(1000,9999)}"
            cust = random.choice(customers)
            prod = random.choice(products)
            qty = random.randint(1, 5)
            total = qty * prod[3]
            rows.append({
                "order_id": order_id,
                "date": date,
                "customer_name": cust[0],
                "phone": cust[1],
                "product_id": prod[0],
                "product_name": prod[1],
                "category": prod[2],
                "qty": qty,
                "unit_price": prod[3],
                "total_price": total,
                "payment_method": random.choice(payment_methods),
                "tax": round(total * 0.05, 2),
                "order_total": round(total * 1.05, 2),
            })

    df = pd.DataFrame(rows)
    sample_path = RAW_DATA_DIR / f"sample_{datetime.today().strftime('%Y%m%d')}.csv"
    df.to_csv(sample_path, index=False)
    logger.info(f"📝 Sample data written: {sample_path}")
    return df


if __name__ == "__main__":
    df = extract_sample_data()
    print(df.head(10).to_string())
