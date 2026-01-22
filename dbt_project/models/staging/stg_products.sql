{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'products') }}
),

renamed as (
    select
        product_id,
        sku,
        product_name,
        category,
        subcategory,
        brand,
        unit_cost,
        unit_price,
        round(unit_price - unit_cost, 2) as profit_margin,
        round((unit_price - unit_cost) / nullif(unit_cost, 0) * 100, 2) as profit_margin_pct,
        weight_kg,
        dimensions_cm,
        is_active,
        reorder_point,
        lead_time_days,
        created_date,
        updated_date
    from source
)

select * from renamed
