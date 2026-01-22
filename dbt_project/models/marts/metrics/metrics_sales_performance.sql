{{
    config(
        materialized='view',
        schema='marts'
    )
}}

-- Sales Performance Metrics
-- Tableau-ready view for sales analytics

with daily_sales as (
    select
        date_key,
        order_month,
        order_quarter,
        order_year,
        product_category,
        product_subcategory,
        customer_segment,
        customer_type,
        shipping_state,
        
        -- Metrics
        count(distinct order_id) as order_count,
        count(distinct customer_id) as customer_count,
        sum(quantity) as units_sold,
        sum(net_line_total) as revenue,
        sum(gross_profit) as gross_profit,
        avg(net_line_total) as avg_order_value,
        sum(order_discount_amount) as total_discounts
        
    from {{ ref('fact_sales') }}
    group by 1, 2, 3, 4, 5, 6, 7, 8, 9
)

select 
    *,
    round(gross_profit / nullif(revenue, 0) * 100, 2) as gross_margin_pct,
    round(total_discounts / nullif(revenue + total_discounts, 0) * 100, 2) as discount_pct
from daily_sales
