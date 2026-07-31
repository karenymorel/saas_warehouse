# SaaS Churn Data Warehouse (DuckDB + MotherDuck)

## — Overview
This project is an End-to-End Data Engineering and Analytics Engineering pipeline. It extracts raw data from external sources, transforms it following the **Medallion Architecture (Bronze, Silver, Gold)**, and models it into a **Star Schema** to analyze customer churn and support interactions.

## — Tech Stack
* **Data Warehouse / Engine:** DuckDB (Local) & MotherDuck (Cloud)
* **Language:** SQL (Advanced Data Transformations)
* **Version Control:** Git & GitHub
* *(Next Phase: dbt for data transformations & testing)*

## — Architecture & Pipeline
1. **Bronze Layer (Ingestion):** Direct HTTP extraction from raw CSV files in the cloud using DuckDB's `read_csv_auto`.
2. **Silver Layer (Staging):** Data cleaning, type casting, text standardization (`snake_case`), and synthetic key mapping for Identity Resolution.
3. **Gold Layer (Star Schema):** 
   * `dim_customers`: Customer entity attributes.
   * `fact_subscriptions`: Business events and churn tracking.
4. **Analytics Marts (Views):** Business logic layer created to answer specific questions:
   * *Churn rate by geographical state.*
   * *Impact of customer service calls on churn probability.*

## — Key Business Insight
**Support Calls vs. Churn:** Through the `mart_support_calls_impact` view, I discovered a direct correlation between the number of customer service calls and the churn rate. Customers with 4 or more calls exhibit an exponentially higher risk of canceling their subscription, indicating a critical threshold for proactive customer retention strategies.

## — Repository Structure
```text
queries/
├── 1_create_database.sql
├── 2_bronze_schema.sql
├── 3_silver_schema.sql
├── 4_gold_schema.sql
└── 5_analytics_marts.sql
