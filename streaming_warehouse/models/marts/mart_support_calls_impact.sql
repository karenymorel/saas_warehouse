{{ config(materialized='view') }}

SELECT 
    f.customer_service_calls AS number_of_support_calls,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE f.is_churned = TRUE) AS churned_customers,
    ROUND(COUNT(*) FILTER (WHERE f.is_churned = TRUE) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM {{ ref('fact_subscriptions') }} f
GROUP BY f.customer_service_calls
ORDER BY f.customer_service_calls ASC