# Donut Shop Analytics Dashboard - User Documentation

Welcome to the Donut Shop Analytics Dashboard. This application is built to provide comprehensive insights into retail sales performance, inventory tracking, financial metrics, and human resource management.

---

## Architecture Overview

The application processes data across multiple relational database schemas:
* **Sales Schema:** Manages transactional records and purchase items (`sales`, `sale_items`).
* **Inventory Schema:** Handles product catalog, recipes, stock levels, waste logs, and procurement (`categories`, `donuts`, `donut_ingreds`, `ingredients`, `ingred_stock`, `waste_logs`, `purchases`, `suppliers`).
* **HR Schema:** Stores organizational structure, employee profiles, shift schedules, and payroll histories (`employees`, `job_roles`, `shifts`, `payments_history`).

---

## Global Navigation and Layout Standard

Each core operational page in this dashboard follows a unified layout design:
1. **Global Data Refresh:** A top-level refresh button allowing users to clear execution cache and load the latest records directly from the database.
2. **Key Performance Indicators (KPIs):** High-level summary metrics positioned at the top of each module.
3. **Structured Views:** A tabbed interface dividing information into:
   * **Tables Tab:** Filterable and detailed tabular representations of raw/aggregated data.
   * **Charts Tab:** Interactive graphical visualizations for trend analysis and comparative studies.

---

## Module Breakdown

### 1. Sales & Revenue Analysis

This page provides financial performance tracking, sales volume analysis, and discount strategy evaluations.

* **Key Performance Indicators (KPIs):**
  * **Total Quantity Sold:** Aggregate count of donuts sold.
  * **Total Profit:** Cumulative net profit generated across all sales.
  * **Top Selling Donut:** Highest volume product item.

* **Data Tables:**
  * **Sale Statistic With and Without Discount:** Displays comparative performance per donut (`donut_id`, `with_discount_sale`, `without_discount_sale`) to evaluate promotion impact.
  * **Donut Statistic By Sale Date and Month:** Time-based aggregation showing `sale_date`, `total_sale_quantity`, and `total_revenue`. Features an interactive month selection filter to isolate daily metrics.

* **Visualizations:**
  * **Donut Sale Statistic By Month (Line Chart):** Monthly trend tracking total units sold versus total revenue generated.
  * **Total Spending vs Total Profit Per Donut (Scatter Plot):** Profitability mapping evaluating operational cost against net profit per unit.
  * **Donuts Sale Statistic (Bar Chart):** Direct comparison of sales volume across individual donut types.
  * **Profit By Category (Donut Chart):** Percentage contribution of each product category to overall profit.
  * **Sale Quantity By Categories (Donut Chart):** Share of total sales volume broken down by product category.

---

### 2. Inventory & Food Waste Management

This page focuses on supply chain tracking, stock thresholds, supplier expenditures, and waste analysis.

* **Key Performance Indicators (KPIs):**
  * **Total Purchases Amount:** Aggregate financial expenditure on raw ingredients.
  * **Total Donut Waste Quantity:** Total count of discarded or expired donut units.
  * **Total Loss Price:** Financial loss resulting from product wastage.

* **Data Tables:**
  * **Donut Waste History:** Granular records of wastage containing `donut_id`, `name`, `quantity`, `lose_price`, and `date`. Includes an interactive dropdown to filter logs by month.
  * **Full Purchases History:** Comprehensive procurement logs detailing `ingred_name`, `supplier_name`, `quantity_bought`, `price_per_unit`, `unit_name`, `total_price`, and `purchase_date`.

* **Visualizations:**
  * **Donut Waste Stats For Every Month (Line Chart):** Historical monthly trend of wasted product volume.
  * **Donut Waste Status For Every Donut (Bar Chart):** Breakdown of wastage quantity per specific product.
  * **Ingredients Stock Status (Bar Chart):** Metric comparing current stock levels against minimum required inventory thresholds for each ingredient.
  * **Supplier Performance (Bar Chart):** Total financial expenditure distributed by supplier.

---

### 3. Employee Status (HR Analytics)

This page handles workforce management, payroll allocations, schedule tracking, and staff demographics.

* **Key Performance Indicators (KPIs):**
  * **Total Employees:** Active count of workforce personnel.
  * **Total Salary:** Cumulative monthly payroll expenditure.
  * **Average Salary:** Mean compensation across active workforce.

* **Data Tables:**
  * **Employees Details:** Displays complete profile records (`employee_id`, `name`, `email`, `age`, `current_salary`, `role_name`, `shift_name`, `start_time`, `end_time`, `act_stat`). Features a checkbox trigger to enable targeted filtering by job role.
  * **Last 10 Salary Payments:** Audit trail of recent payroll disbursements showing employee details, compensation amount, payment method, and exact timestamp.

* **Visualizations:**
  * **Total Employees For Every Shift (Bar Chart):** Distribution of staff capacity across operational work shifts.
  * **Employees Count By Age Group (Histogram):** Demographic breakdown of workforce age distribution.
  * **Employees Joined Per Month (Line Chart):** Hiring trend tracking staff onboarding over time.
  * **Salary Payments For Every Month (Line Chart):** Historical trend of total monthly salary expenditures.

---

## Getting Started

1. Navigate through individual modules using the sidebar navigation.
2. Apply available selectbox or checkbox filters within the **Tables** tab to query specific timeframes or categories.
3. Use the **Refresh** button at the top of any page after running database updates to instantly reflect new records across all visualizations.
