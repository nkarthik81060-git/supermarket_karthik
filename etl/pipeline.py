"""
etl/pipeline.py
===============
SuperMart ETL — Main Orchestrator
Runs: Extract → Transform → Load

Usage:
    python -m etl.pipeline
    python -m etl.pipeline --date 2025-01-15
    python -m etl.pipeline --sample
"""

import argparse
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("etl_pipeline.log"),
    ],
)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from etl.extract   import extract_csv_files, extract_sample_data
from etl.transform import transform
from etl.load      import load, get_summary


def run_pipeline(date_filter: str = None, use_sample: bool = False) -> bool:
    """
    Execute the full ETL pipeline.

    Returns True on success, False on failure.
    """
    start = time.time()
    banner = "=" * 60
    logger.info(banner)
    logger.info("  🛒 SUPERMART ETL PIPELINE — STARTING")
    logger.info(f"  Run Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if date_filter:
        logger.info(f"  Filter   : date={date_filter}")
    logger.info(banner)

    # ── STAGE 1: EXTRACT ──────────────────────────────────────────
    logger.info("\n📥 STAGE 1: EXTRACT")
    try:
        if use_sample:
            logger.info("  Mode: Sample data generation")
            raw_df = extract_sample_data()
        else:
            logger.info("  Mode: CSV files from data/raw/")
            raw_df = extract_csv_files(date_filter=date_filter)

        if raw_df.empty:
            logger.warning("  ⚠️  No data extracted — pipeline halted.")
            return False

        logger.info(f"  ✅ Extracted {len(raw_df)} rows")

    except Exception as e:
        logger.error(f"  ❌ EXTRACT failed: {e}", exc_info=True)
        return False

    # ── STAGE 2: TRANSFORM ────────────────────────────────────────
    logger.info("\n🔧 STAGE 2: TRANSFORM")
    try:
        transformed = transform(raw_df)
        if not transformed:
            logger.error("  ❌ TRANSFORM returned empty — pipeline halted.")
            return False
        for k, v in transformed.items():
            logger.info(f"  ✅ {k:20s}: {len(v)} rows")

    except Exception as e:
        logger.error(f"  ❌ TRANSFORM failed: {e}", exc_info=True)
        return False

    # ── STAGE 3: LOAD ─────────────────────────────────────────────
    logger.info("\n🗄️  STAGE 3: LOAD")
    try:
        stats = load(transformed)
        for table, rows in stats.items():
            logger.info(f"  ✅ {table:20s}: {rows} rows loaded")

    except Exception as e:
        logger.error(f"  ❌ LOAD failed: {e}", exc_info=True)
        return False

    # ── SUMMARY ───────────────────────────────────────────────────
    elapsed = time.time() - start
    logger.info(f"\n{banner}")
    logger.info(f"  ✅ PIPELINE COMPLETE in {elapsed:.2f}s")
    logger.info(banner)

    summary = get_summary()
    if not summary.empty:
        logger.info("\n📊 DATABASE SUMMARY:")
        for col in summary.columns:
            logger.info(f"   {col:20s}: {summary[col].iloc[0]} rows")

    logger.info("\n📊 Next: Open Power BI and refresh from database/supermart.db")
    return True


def main():
    parser = argparse.ArgumentParser(description="SuperMart ETL Pipeline")
    parser.add_argument("--date",   help="Filter by date YYYY-MM-DD", default=None)
    parser.add_argument("--sample", help="Generate sample data",      action="store_true")
    args = parser.parse_args()

    success = run_pipeline(date_filter=args.date, use_sample=args.sample)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
