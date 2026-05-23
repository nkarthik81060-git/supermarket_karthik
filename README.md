# 🛒 Supermarket Data Pipeline — ETL + Reporting

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![ETL](https://img.shields.io/badge/ETL%20Pipeline-00897B?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-00d4aa?style=for-the-badge)

**A full end-to-end data pipeline for supermarket sales — from raw data ingestion to interactive Power BI reporting.**

[🌐 Live Demo](https://nkarthik81060-git.github.io/supermarket_karthik/) · [📂 Repository](https://github.com/nkarthik81060-git/supermarket_karthik) · [👤 Author](https://www.linkedin.com/in/nagiri-karthik-data-analyst/)

</div>

---

## 📌 Project Overview

This project implements a **complete supermarket data pipeline** that ingests raw sales data, transforms and cleans it using Python and SQL, and delivers actionable insights through a Power BI dashboard.

The goal is to help supermarket stakeholders understand:
- 📈 Sales trends across product categories and time periods
- 🏷️ Top-selling products and underperformers
- 👥 Customer purchase patterns and behaviour
- 💰 Revenue, profit margins, and branch performance

---

## 🏗️ Architecture

```
Raw Data (CSV)
      │
      ▼
 Python ETL Layer
  ├── Data Extraction
  ├── Data Cleaning & Transformation
  └── Data Loading
      │
      ▼
  SQL Database
  ├── Staging Tables
  ├── Transformed Tables
  └── Reporting Views
      │
      ▼
 Power BI Dashboard
  ├── Sales Analysis
  ├── Product Performance
  ├── Customer Insights
  └── Branch Comparisons
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔁 **ETL Pipeline** | Automated extraction, transformation and loading of raw supermarket CSV data |
| 🧹 **Data Cleaning** | Handles missing values, duplicates, data type fixes and standardisation |
| 🗄️ **SQL Storage** | Structured staging and reporting tables for clean, queryable data |
| 📊 **Power BI Reports** | Interactive dashboard with filters by branch, product, date and category |
| 📈 **Sales Analysis** | Revenue trends, daily/monthly sales comparison and growth tracking |
| 🏪 **Branch Performance** | Side-by-side comparison across supermarket branches |
| 🛍️ **Product Insights** | Top and bottom performing products by category |
| 👥 **Customer Analysis** | Purchase frequency, average basket size and customer segmentation |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.x |
| **Data Processing** | Pandas, NumPy |
| **Database** | SQL (MySQL / SQLite) |
| **Reporting** | Microsoft Power BI |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
supermarket_karthik/
│
├── data/
│   ├── raw/                  # Raw input CSV files
│   └── processed/            # Cleaned and transformed data
│
├── etl/
│   ├── extract.py            # Data extraction scripts
│   ├── transform.py          # Cleaning and transformation logic
│   └── load.py               # Loading data into SQL
│
├── sql/
│   ├── create_tables.sql     # Table schema definitions
│   ├── staging.sql           # Staging layer queries
│   └── reporting_views.sql   # Views used by Power BI
│
├── dashboard/
│   └── supermarket_report.pbix  # Power BI dashboard file
│
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
MySQL or SQLite
Microsoft Power BI Desktop
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/nkarthik81060-git/supermarket_karthik.git

# 2. Navigate to the project folder
cd supermarket_karthik

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the ETL pipeline
python etl/extract.py
python etl/transform.py
python etl/load.py

# 5. Open the SQL scripts to set up the database
# Run sql/create_tables.sql first, then staging.sql

# 6. Open dashboard/supermarket_report.pbix in Power BI Desktop
```

---

## 📊 Dashboard Preview

> 🔗 **[View Live Demo →](https://nkarthik81060-git.github.io/supermarket_karthik/)**

The Power BI dashboard includes:

- **Overview Page** — Total revenue, transactions, average order value
- **Sales Trends** — Daily, weekly and monthly sales charts
- **Product Analysis** — Category-wise breakdown and top products
- **Branch Comparison** — Performance metrics across all branches
- **Customer Insights** — Purchase patterns and segmentation

---

## 📈 Key Insights Delivered

- Identified **top revenue-generating product categories** across branches
- Tracked **month-on-month sales growth** for business forecasting
- Highlighted **peak shopping hours and days** for staffing decisions
- Compared **branch performance** to flag underperforming locations
- Analysed **customer basket size trends** for pricing strategy

---

## 🤝 Author

**Nagiri Karthik** — Data Analyst at TCS, Bengaluru

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/nagiri-karthik-data-analyst/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/nkarthik81060-git)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-00d4aa?style=flat-square&logo=githubpages)](https://nkarthik81060-git.github.io/karthik_profile/)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=flat-square&logo=gmail)](mailto:karthiknagiri554658@gmail.com)

---

<div align="center">
  <sub>⭐ If you found this project useful, please give it a star!</sub>
</div>
