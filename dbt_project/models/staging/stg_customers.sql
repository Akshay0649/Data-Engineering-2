{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'customers') }}
),

renamed as (
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
        case 
            when total_orders > 0 then round(lifetime_value / total_orders, 2)
            else 0 
        end as avg_order_value,
        is_active,
        credit_limit,
        payment_terms_days,
        account_created_date,
        last_order_date,
        updated_date,
        datediff('day', account_created_date, current_date()) as days_since_first_order,
        datediff('day', last_order_date, current_date()) as days_since_last_order
    from source
)

select * from renamed
