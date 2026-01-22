{{
    config(
        materialized='table',
        schema='marts'
    )
}}

-- Fact: Sales Orders
-- Grain: One row per order line

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_lines as (
    select * from {{ ref('stg_order_lines') }}
),

products as (
    select * from {{ ref('dim_products') }}
),

customers as (
    select * from {{ ref('dim_customers') }}
),

final as (
    select
        -- Keys
        ol.order_line_id,
        ol.order_id,
        o.customer_id,
        ol.product_id,
        o.order_date as date_key,
        
        -- Degenerate dimensions
        o.order_status,
        o.payment_method,
        ol.line_status,
        
        -- Geography
        o.shipping_city,
        o.shipping_state,
        o.shipping_postal_code,
        
        -- Quantities
        ol.quantity,
        
        -- Amounts
        ol.unit_price,
        ol.line_total,
        ol.discount_percent,
        ol.discount_amount,
        ol.net_line_total,
        
        -- Order level amounts (for aggregation)
        o.subtotal as order_subtotal,
        o.tax_amount as order_tax_amount,
        o.shipping_cost as order_shipping_cost,
        o.discount_amount as order_discount_amount,
        o.total_amount as order_total_amount,
        
        -- Product attributes (for filtering)
        p.category as product_category,
        p.subcategory as product_subcategory,
        p.brand as product_brand,
        p.unit_cost as product_cost,
        round(ol.net_line_total - (p.unit_cost * ol.quantity), 2) as gross_profit,
        
        -- Customer attributes (for filtering)
        c.customer_segment,
        c.customer_type,
        
        -- Timestamps
        o.order_timestamp,
        o.order_month,
        o.order_quarter,
        o.order_year,
        o.order_day_of_week,
        o.order_hour,
        
        current_timestamp() as _dbt_loaded_at
    from order_lines ol
    inner join orders o on ol.order_id = o.order_id
    left join products p on ol.product_id = p.product_id
    left join customers c on o.customer_id = c.customer_id
)

select * from final
