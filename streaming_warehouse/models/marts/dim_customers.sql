{{ config(materialized='table') }}

SELECT
    customer_id,
    email,
    address,
    length_of_membership_years,
    yearly_amount_spent_usd
FROM {{ ref('stg_customers') }}