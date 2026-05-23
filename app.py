"""
app.py
======
SuperMart — Flask web server
Serves the HTML booking form and accepts JSON POST submissions,
writing them to CSV for the ETL pipeline to process.
"""

import os
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")

RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

CSV_COLUMNS = [
    "order_id","date","customer_name","phone",
    "product_id","product_name","category",
    "qty","unit_price","total_price",
    "payment_method","tax","order_total",
]


@app.route("/")
def index():
    """Serve the HTML booking form."""
    return send_from_directory("templates", "index.html")


@app.route("/api/booking", methods=["POST"])
def receive_booking():
    """
    Accept JSON booking data from the HTML form.
    Appends each line item to today's CSV file.
    This is the EXTRACT step of the ETL pipeline.
    """
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No data received"}), 400

        order_id     = data.get("orderId", f"ORD{int(datetime.now().timestamp())}")
        date_str     = datetime.now().strftime("%Y-%m-%d")
        customer     = data.get("customerName", "Walk-in")
        phone        = data.get("phone", "N/A")
        payment      = data.get("paymentMethod", "cash")
        items        = data.get("items", [])
        order_total  = data.get("total", 0)
        tax          = data.get("tax", 0)

        if not items:
            return jsonify({"error": "No items in order"}), 400

        # Write to today's CSV
        csv_file = RAW_DATA_DIR / f"bookings_{date_str}.csv"
        file_exists = csv_file.exists()

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            if not file_exists:
                writer.writeheader()

            for item in items:
                writer.writerow({
                    "order_id":      order_id,
                    "date":          date_str,
                    "customer_name": customer,
                    "phone":         phone,
                    "product_id":    item.get("id", ""),
                    "product_name":  item.get("name", ""),
                    "category":      item.get("cat", ""),
                    "qty":           item.get("qty", 1),
                    "unit_price":    item.get("price", 0),
                    "total_price":   item.get("qty", 1) * item.get("price", 0),
                    "payment_method":payment,
                    "tax":           round(tax, 2),
                    "order_total":   round(order_total, 2),
                })

        logger.info(f"✅ Booking saved: {order_id} ({len(items)} items) → {csv_file}")

        return jsonify({
            "success":  True,
            "order_id": order_id,
            "csv_file": str(csv_file),
            "items":    len(items),
            "message":  "Booking extracted to CSV. ETL pipeline will process shortly.",
        })

    except Exception as e:
        logger.error(f"❌ Error processing booking: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/run-etl", methods=["POST"])
def trigger_etl():
    """Manually trigger the ETL pipeline (for dev/testing)."""
    try:
        from etl.pipeline import run_pipeline
        success = run_pipeline()
        return jsonify({"success": success, "message": "ETL pipeline completed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/summary")
def summary():
    """Return DB summary stats."""
    try:
        from etl.load import get_summary
        df = get_summary()
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"🛒 SuperMart ETL app starting on http://localhost:{port}")
    app.run(debug=True, port=port)
