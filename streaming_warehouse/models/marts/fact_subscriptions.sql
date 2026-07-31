{{ config(materialized='table') }}

SELECT
    subscription_id,
    customer_id,
    state_code,
    account_length_months,
    has_international_plan,
    has_vmail_plan,
    customer_service_calls,
    is_churned
FROM {{ ref('stg_subscriptions') }}