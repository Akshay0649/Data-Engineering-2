{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'order_lines') }}
),

renamed as (
    select
        order_line_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_percent,
        line_total,
        -- Calculate discounted amount
        round(line_total * discount_percent / 100, 2) as discount_amount,
        round(line_total - (line_total * discount_percent / 100), 2) as net_line_total,
        line_status,
        notes
    from source
)

select * from renamed
