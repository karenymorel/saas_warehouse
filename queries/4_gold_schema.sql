CREATE SCHEMA IF NOT EXISTS gold;

# Tabla dimensiones
CREATE OR REPLACE TABLE gold.dim_customers AS
SELECT
  customer_id,
  email,
  address,
  length_of_membership_years,
  yearly_amount_spent_usd
FROM silver.stg_customers;

# Table hechos
CREATE OR REPLACE TABLE gold.fact_subscriptions AS
SELECT
  subscription_id,
  customer_id,
  state_code,
  account_length_months,
  has_international_plan,
  has_vmail_plan,
  customer_service_calls,
  is_churned
FROM silver.stg_subscriptions;