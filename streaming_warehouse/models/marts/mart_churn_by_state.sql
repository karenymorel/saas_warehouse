{{ config(materialized='view') }}

SELECT 
    f.state_code,
    COUNT(*) AS total_subscriptions,
    COUNT(*) FILTER (WHERE f.is_churned = TRUE) AS churned_subscriptions,
    ROUND(COUNT(*) FILTER (WHERE f.is_churned = TRUE) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(f.customer_service_calls), 2) AS avg_support_calls,
    ROUND(SUM(c.yearly_amount_spent_usd), 2) AS total_revenue_usd
FROM {{ ref('fact_subscriptions') }} f
JOIN {{ ref('dim_customers') }} c ON f.customer_id = c.customer_id
GROUP BY f.state_code
ORDER BY churn_rate_pct DESC