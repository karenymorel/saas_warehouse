-- 1. Churn cancelation rate by state:

CREATE OR REPLACE VIEW gold.mart_churn_by_state AS 
SELECT 
  f.state_code,

  COUNT (*) AS total_subscription,

  COUNT (*) FILTER (WHERE f.is_churned = TRUE) AS churned_subscriptions,

  ROUND(COUNT (*) FILTER (WHERE F.IS_CHURNED = TRUE) * 100 / COUNT(*), 2) AS churn_rate_pct,

  ROUND(AVG(f.customer_service_calls), 2) AS avg_support_calls,

  ROUND(AVG(c.yearly_amount_spent_usd), 2) AS total_revenue_usd
FROM gold.fact_subscriptions f 
INNER JOIN gold.dim_customers c ON f.customer_id = c.customer_id
GROUP BY f.state_code
ORDER BY churn_rate_pct DESC; 


-- 2. Customer support impact on Churn rate:

CREATE OR REPLACE VIEW gold.mart_support_calls_impact AS
SELECT
  f.customer_service_calls AS number_of_support_calls,

  COUNT (*) AS total_customers,
  COUNT (*) FILTER (WHERE f.is_churned = TRUE) AS churned_customers,

  ROUND(COUNT (*) FILTER (WHERE f.is_churned = TRUE) * 100 / COUNT (*), 2) AS churn_rate_pct
FROM gold.fact_subscriptions f 
INNER JOIN gold.dim_customers c ON f.customer_id = c.customer_id
GROUP BY f.customer_service_calls
ORDER BY f.customer_service_calls DESC;