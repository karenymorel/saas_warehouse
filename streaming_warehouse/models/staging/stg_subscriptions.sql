{{ config(materialized='table') }}

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
FROM {{ source('bronze', 'raw_subscriptions') }}