#!/bin/bash
# ============================================================
# push_to_github.sh
# Pushes this project to: github.com/nkarthik81060-git/supermarket_karthik
# Run this from the project root directory
# ============================================================

echo "🛒 SuperMart ETL — GitHub Push Script"
echo "======================================"

# Initialize git if needed
if [ ! -d ".git" ]; then
  echo "📦 Initializing git repository..."
  git init
  git remote add origin https://github.com/nkarthik81060-git/supermarket_karthik.git
fi

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/
.env

# Data files (raw CSVs contain customer data)
data/raw/*.csv
data/processed/*.csv

# Database
database/supermart.db

# Logs
*.log

# OS
.DS_Store
Thumbs.db
EOF

echo "✅ .gitignore created"

# Stage all files
git add .
git status

echo ""
echo "📝 Committing..."
git commit -m "feat: SuperMart ETL pipeline - HTML booking form + Extract/Transform/Load + SQL schema + Power BI guide

- templates/index.html  : Daily product booking UI (20 products, 5 categories)
- etl/extract.py        : Stage 1 - Read CSV files from data/raw/
- etl/transform.py      : Stage 2 - Clean, validate, enrich with Pandas
- etl/load.py           : Stage 3 - Load into SQLite with Power BI views
- etl/pipeline.py       : Orchestrator - runs full ETL pipeline
- database/schema.sql   : DDL + 5 Power BI optimized views
- app.py                : Flask server - serves form, receives bookings
- reports/powerbi_guide.md : Power BI connection + DAX measures
- requirements.txt      : Python dependencies"

echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! View at: https://github.com/nkarthik81060-git/supermarket_karthik"
