# 📊 RetailPulse — AI-Powered Customer Analytics & Demand Forecasting

**Author:** Shiney Priyanka R
**Internship:** Data Science & Analytics, Zidio Development
**Submission Date:** July 2026

🔗 **Live Demo:** [RetailPulse Dashboard](https://retailpulse-exnr56kipghzahusngitcw.streamlit.app/)
📂 **GitHub Repo:** [github.com/shineypriyanka/retailpulse](https://github.com/shineypriyanka/retailpulse)

---

## Project Overview

RetailPulse is an end-to-end retail analytics platform built on the **Olist Brazilian E-Commerce dataset** (Kaggle). It transforms 110,189 raw order-line records into actionable business intelligence covering sales performance, customer segmentation, churn risk, demand forecasting, and inventory optimization — surfaced through both a live Streamlit web dashboard and a Power BI reporting suite.

**Target users:** Retail analysts, e-commerce operations teams, and business decision-makers who need a single view of sales health, at-risk customers, and stock planning.

**Business value delivered:**
- Identifies BRL 7.6M in revenue tied to high/medium churn-risk customers, enabling targeted retention efforts
- Flags the 28.2% of products (Class A) that drive 80% of revenue, focusing inventory attention where it matters most
- Provides week-ahead demand forecasts to support reorder planning

---

## Key Features

| ID | Feature | Description | Result |
|---|---|---|---|
| F1 | Data Pipeline | Cleans and merges 9 raw Olist CSVs into a unified dataset | 110,189 rows, 93,350 unique customers |
| F2 | Exploratory Data Analysis | Revenue, category, and time-trend analysis | BRL 15.42M total revenue; health_beauty top category; Nov 2017 peak month |
| F3 | RFM Customer Segmentation | Recency-Frequency-Monetary scoring into 8 segments | Loyal Customers 25.1%, Champions 12.5% |
| F4 | Churn Risk Scoring | RFM-based risk tiering (Low/Medium/High) | 25.1% of customers High Risk; BRL 7.6M revenue at risk (High + Medium combined) |
| F5 | Demand Forecasting | Compared Naive baseline vs. LightGBM | Naive baseline outperformed (WAPE 16.1% vs. 25.1%); BRL 267,608 avg. weekly forecast |
| F6 | Inventory Optimization (ABC + EOQ) | Classified all 31,619 products by revenue contribution, calculated Economic Order Quantity | Class A (28.2% of products) drives 80% of revenue |
| F7 | Interactive Dashboards | 4-page Streamlit app + 6-page Power BI report | Real-time filtering, drill-through, and cross-page slicers |

---

## Technology Stack

| Category | Technology | Rationale |
|---|---|---|
| Language | Python | Core data processing and modeling |
| Data Processing | pandas, numpy | Cleaning, merging, feature engineering |
| Machine Learning | scikit-learn, LightGBM | Churn scoring, demand forecast comparison |
| Visualization (Web) | Streamlit, Plotly | Interactive, deployable dashboard |
| Visualization (BI) | Power BI | Semantic model, DAX measures, cross-filtered reporting |
| Version Control | Git & GitHub | Source control and submission |

> **Note on scope:** This project intentionally uses a lean, reproducible stack (LightGBM instead of deep learning forecasting, no orchestration/MLOps layer) appropriate for the dataset size and project timeline. Forecast model selection was evidence-based — a Naive baseline was retained over LightGBM after WAPE comparison showed it performed better on this dataset.

---

## Architecture / Data Flow

```
Raw Olist CSVs (9 files, Kaggle)
        │
        ▼
Data Pipeline (src/pipeline.py) — cleaning, merging, feature engineering
        │
        ▼
master.csv (110,189 rows)
        │
        ├──► EDA (notebooks/01_eda.ipynb)
        ├──► RFM Segmentation (notebooks/02_rfm_segmentation.ipynb)
        ├──► Churn Risk Scoring (notebooks/03_churn.ipynb)
        ├──► Demand Forecasting (notebooks/04_forecasting.ipynb)
        └──► Inventory ABC/EOQ Analysis (notebooks/05_inventory.ipynb)
                │
                ▼
        data/processed/*.csv + *.pkl
                │
        ┌───────┴────────┐
        ▼                ▼
Streamlit Dashboard   Power BI Report
(app/dashboard.py)    (powerbi/RetailPulse_Dashboard.pbix)
```

---

## Project Structure

```
retailpulse/
├── app/
│   └── dashboard.py              # 4-page Streamlit dashboard
├── data/
│   ├── raw/                      # Original Kaggle CSVs (not tracked — see Setup)
│   └── processed/                # Cleaned datasets, model artifacts
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_rfm_segmentation.ipynb
│   ├── 03_churn.ipynb
│   ├── 04_forecasting.ipynb
│   └── 05_inventory.ipynb
├── powerbi/
│   └── RetailPulse_Dashboard.pbix   # 6-page Power BI report (not tracked — large binary)
├── src/
│   └── pipeline.py                # Data cleaning & merge pipeline
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/shineypriyanka/retailpulse.git
cd retailpulse
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the dataset
This repo excludes raw data to keep the repository lightweight. Download the **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** from Kaggle and place the 9 CSVs into `data/raw/`.

### 4. Run the pipeline (optional — processed data is already included)
```bash
python src/pipeline.py
```

### 5. Launch the dashboard locally
```bash
streamlit run app/dashboard.py
```

---

## Dashboards

### Streamlit (Live Demo)
4 pages: **Sales**, **Customer**, **Forecast**, **Inventory** — [view live](https://retailpulse-exnr56kipghzahusngitcw.streamlit.app/)

### Power BI
6 pages: **Executive Summary**, **Sales & Seasonal Trends**, **Product & Region Performance**, **Customer Analytics**, **Profit/Orders/Inventory Risk**, **Advanced & Interactive Filters** (with synced slicers and category drill-through). See the Project Report PDF for screenshots.

---

## Key Insights

- **Revenue:** BRL 15.42M across 96,470 orders from 93,350 unique customers, averaging BRL 159.83 per order
- **Seasonality:** Clear November 2017 peak, consistent with Brazilian retail seasonal patterns
- **Customer health:** 12.5% of customers are Champions; 21.1%+28.26% fall into Medium/High churn risk, representing BRL 7.6M in exposed revenue
- **Geography:** São Paulo (SP) leads all states in revenue, consistent with Brazil's e-commerce concentration
- **Inventory:** Just 28.2% of products (Class A) account for 80% of revenue — the clearest lever for stock prioritization
- **Forecasting:** A simple Naive baseline (16.1% WAPE) outperformed LightGBM (25.1% WAPE) on this dataset — an important, evidence-based finding rather than defaulting to the more complex model

---

## Personal Reflection

This project gave me hands-on experience with the full analytics lifecycle — from messy multi-table raw data through to a deployed, interactive product. Key learnings included the importance of validating model choice with real metrics rather than assuming complexity equals accuracy (the Naive-vs-LightGBM forecasting result was a genuine surprise), and the practical debugging involved in taking a Power BI model from broken relationships and mismatched aggregations to a clean, cross-filtered 6-page report. Deploying to Streamlit Cloud also taught me the gap between "works on my machine" and a reproducible, portable deployment — particularly around relative file paths and dependency management.

**Future improvements:** incorporating true delivery-delay tracking (requires an estimated-delivery-date field not present in this dataset), exploring segment-specific forecasting models, and adding automated data refresh scheduling.
