CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE silver.stg_customers AS
SELECT
  ROW_NUMBER() OVER () AS customer_id,
  
  LOWER(TRIM(Email)) AS email,
  
  REPLACE(TRIM(Address), chr(10), ', ') AS address,
  
  LOWER(TRIM(Avatar)) AS avatar,
  
  ROUND(CAST("Avg. Session Length" AS DECIMAL(10,2)), 2) AS avg_session_length_min,
  ROUND(CAST("Time on App" AS DECIMAL(10,2)), 2) AS time_on_app_min,
  ROUND(CAST("Time on Website" AS DECIMAL(10,2)), 2) AS time_on_website_min,
  ROUND(CAST("Length of Membership" AS DECIMAL(10,2)), 2) AS length_of_membership_years,
  ROUND(CAST("Yearly Amount Spent" AS DECIMAL(10,2)), 2) AS yearly_amount_spent_usd 
FROM bronze.raw_customers;


CREATE OR REPLACE TABLE silver.stg_subscriptions AS
SELECT
  ROW_NUMBER() OVER () AS subscription_id,
  
  ((ROW_NUMBER() OVER () - 1) % 500) + 1 AS customer_id,
  
  TRIM(State) AS state_code,
  CAST("Account Length" AS INT) AS account_length_months,
  CAST("Area Code" AS INT) AS area_code,
  
  "Int'l Plan" AS has_international_plan,
  "VMail Plan" AS has_vmail_plan,
  
  CAST("VMail Message" AS INT) AS vmail_messages_count,
  
  CAST("CustServ Calls" AS INT) AS customer_service_calls,
  
  CASE WHEN LOWER(TRIM("Churn?")) LIKE 'true%' THEN TRUE ELSE FALSE END AS is_churned
FROM bronze.raw_subscriptions;