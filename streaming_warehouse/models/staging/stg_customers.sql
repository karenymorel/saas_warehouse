{{ config(materialized='table') }}

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
FROM {{ source('bronze', 'raw_customers') }}