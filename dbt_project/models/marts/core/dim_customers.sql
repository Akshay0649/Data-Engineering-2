{{
    config(
        materialized='table',
        schema='marts'
    )
}}

-- Dimension: Customer
-- Slowly Changing Dimension Type 1

with customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        customer_id,
        customer_type,
        customer_name,
        email,
        phone,
        address_line1,
        address_line2,
        city,
        state,
        postal_code,
        country,
        customer_segment,
        lifetime_value,
        total_orders,
        avg_order_value,
        is_active,
        credit_limit,
        payment_terms_days,
        account_created_date,
        last_order_date,
        days_since_first_order,
        days_since_last_order,
        updated_date,
        current_timestamp() as _dbt_loaded_at
    from customers
)

select * from final
