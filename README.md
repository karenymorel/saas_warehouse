# SaaS Churn Data Warehouse (DuckDB + MotherDuck)

![dbt CI/CD](https://img.shields.io/badge/dbt--duckdb-v1.12.0-orange?style=flat-square&logo=dbt)
![MotherDuck](https://img.shields.io/badge/MotherDuck-Cloud_Data_Warehouse-brightgreen?style=flat-square)
![Streamlit App](https://img.shields.io/badge/Streamlit-Live_Dashboard-FF4B4B?style=flat-square&logo=streamlit)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Passing-success?style=flat-square&logo=githubactions)

<img width="1753" height="769" alt="image" src="https://github.com/user-attachments/assets/13518c91-8a34-4c38-81d6-503020e4d87c" />


🚀 **Live Interactive App & AI Copilot:** [https://saaswarehouse.streamlit.app/](https://saaswarehouse.streamlit.app/)

## — Overview
This is a production-grade **Analytics Engineering Pipeline** designed to ingest, clean, model, and analyze customer subscription churn for a SaaS platform. 

The pipeline transitions from raw HTTP data ingestion to an automated **Kimball Star Schema Data Warehouse**, incorporating automated Data Quality Testing, CI/CD deployment, and an interactive **Streamlit Dashboard with an AI Executive Copilot**.

## — Tech Stack
* **Data Warehouse Engine:** DuckDB (Local Execution) & MotherDuck (Cloud Data Warehouse)
* **Transformation Framework:** dbt Core (`dbt-duckdb`)
* **Presentation Layer & AI:** Streamlit, Plotly, Groq API (`llama-3.3-70b-versatile`)
* **Orchestration & CI/CD:** GitHub Actions
* **Data Quality & Governance:** `dbt test` (Unique, Not Null, Referential Integrity Checks) & `dbt docs` (Lineage Graph)
* **Version Control:** Git & GitHub

## — Architecture & Pipeline
1. **Bronze Layer (Ingestion):** Direct HTTP extraction from raw CSV files in the cloud using DuckDB's `read_csv_auto`.
2. **Silver Layer (Staging):** Data cleaning, type casting, text standardization (`snake_case`), and synthetic key mapping for Identity Resolution.
3. **Gold Layer (Star Schema):** 
   * `dim_customers`: Customer entity attributes.
   * `fact_subscriptions`: Business events and churn tracking.
4. **Analytics Marts (Views):** Business logic layer created to answer specific questions:
   * *Churn rate by geographical state.*
   * *Impact of customer service calls on churn probability.*
5. **Presentation & AI Layer (Streamlit + LLM):** Interactive web dashboard querying MotherDuck in real time with an integrated AI Copilot for automated executive insights.

<img width="1848" height="417" alt="image" src="https://github.com/user-attachments/assets/25ddfd47-a015-4d2e-9b7c-a1e587c85827" />

## — Key Business Insights
Through the `mart_support_calls_impact` analytical view, the pipeline uncovered a critical operational threshold:
* **Support Call Churn Correlation:** Customers contacting customer support **4 or more times** exhibit an exponentially higher churn rate compared to those with fewer interactions. 
* **Business Recommendation:** Implement proactive retention triggers when a user reaches 3 support tickets.

## — Data Quality & Testing (`dbt test`)
Automated data governance assertions are enforced via `models/marts/schema.yml`:
* **Primary Key Uniqueness & Non-Nullability:** Verified on `dim_customers.customer_id` and `fact_subscriptions.subscription_id`.
* **Referential Integrity:** Enforced between `fact_subscriptions.customer_id` and `dim_customers.customer_id` via `relationships` tests.

## — CI/CD Automation (GitHub Actions)
Every code change pushed to `main` triggers an automated GitHub Actions pipeline (`.github/workflows/dbt_ci.yml`) that:
1. Provisions an isolated Python environment.
2. Connects to MotherDuck Cloud via GitHub Repository Secrets.
3. Compiles and executes `dbt run --profiles-dir .`.
4. Runs automated data quality assertions via `dbt test --profiles-dir .`.

## — How to Run Locally

### 1. Clone & Set up Environment
```bash
git clone https://github.com/tu-usuario/STREAMING_WAREHOUSE.git
cd STREAMING_WAREHOUSE
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Set your `MOTHERDUCK_TOKEN` and `GROQ_API_KEY` in a `.env` file or environment variables:
```bash
MOTHERDUCK_TOKEN="your_motherduck_token"
GROQ_API_KEY="your_groq_api_key"
```

### 3. Run Pipeline & Tests
```bash
cd streaming_warehouse
dbt run --profiles-dir .
dbt test --profiles-dir .
```

### 4. Launch Interactive Web App
```bash
streamlit run app.py
```
