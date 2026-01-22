{{
    config(
        materialized='table',
        schema='marts'
    )
}}

-- Dimension: Product
-- Slowly Changing Dimension Type 1

with products as (
    select * from {{ ref('stg_products') }}
),

final as (
    select
        product_id,
        sku,
        product_name,
        category,
        subcategory,
        brand,
        unit_cost,
        unit_price,
        profit_margin,
        profit_margin_pct,
        weight_kg,
        dimensions_cm,
        is_active,
        reorder_point,
        lead_time_days,
        created_date,
        updated_date,
        current_timestamp() as _dbt_loaded_at
    from products
)

select * from final
