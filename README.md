# 🍩 Donut Shop Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://donutshopdashboard.streamlit.app/)

> 🚀 **Live Dashboard:** [https://donutshopdashboard.streamlit.app/](https://donutshopdashboard.streamlit.app/) *(Replace with your Streamlit Community Cloud URL)*

A high-performance operational intelligence dashboard for donut retail businesses, delivering real-time analytics across **Sales & Revenue**, **Inventory & Waste**, and **Human Resources**.

---

## ⚡ Accelerated by Polars

Traditional Python dashboard stacks rely on Pandas and SQLAlchemy, which often become bottlenecks under heavy aggregation and database loads. This dashboard is powered end-to-end by **[Polars](https://pola.rs/)**:

- **10x–20x Faster Ingestion:** Pairs `polars.read_database_uri` with **ConnectorX**, loading relational PostgreSQL queries directly into Arrow memory without intermediate Python objects.
- **Multi-Threaded Execution:** Polars leverages Rust's parallel execution across all CPU cores to compute grouped sales, waste losses, and payroll KPIs instantly.
- **Minimal Cloud Footprint:** Ultra-low memory overhead ensures smooth, lightning-fast rendering even on resource-constrained platforms like Streamlit Community Cloud.

---

## 📊 Dashboard Modules

1. **Sales & Revenue Analysis:** Profit margins per donut, promotion vs. non-discount performance, monthly volume trends, and category breakdown.
2. **Inventory & Waste Tracking:** Ingredient stock thresholds, loss valuations per recipe, and supplier expenditure analysis.
3. **Employee Status (HR):** Active shift capacity, demographic distributions, hiring trajectories, and audit-ready payroll histories.
4. **User Guide:** Integrated architectural documentation and schema references.

---

## 🛠️ Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/RozinaRB/donut_shop_dashboard.git
cd donut_shop/dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run locally
```bash
streamlit run main.py
```
