{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date,
        order_time,
        cast(order_date || ' ' || order_time as timestamp) as order_timestamp,
        order_status,
        payment_method,
        shipping_address,
        shipping_city,
        shipping_state,
        shipping_postal_code,
        billing_address,
        billing_city,
        billing_state,
        billing_postal_code,
        subtotal,
        tax_amount,
        shipping_cost,
        discount_amount,
        total_amount,
        notes,
        created_date,
        updated_date,
        -- Derived fields
        date_trunc('month', order_date) as order_month,
        date_trunc('quarter', order_date) as order_quarter,
        date_trunc('year', order_date) as order_year,
        extract(dayofweek from order_date) as order_day_of_week,
        extract(hour from order_time) as order_hour
    from source
)

select * from renamed
