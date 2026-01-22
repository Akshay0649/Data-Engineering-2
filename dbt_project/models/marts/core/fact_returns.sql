{{
    config(
        materialized='table',
        schema='marts'
    )
}}

-- Fact: Returns
-- Grain: One row per return

with returns as (
    select * from {{ ref('stg_returns') }}
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
        r.return_id,
        r.order_id,
        r.order_line_id,
        r.product_id,
        r.customer_id,
        r.return_request_date as date_key,
        
        -- Attributes
        r.return_reason,
        r.return_status,
        r.return_condition,
        r.refund_method,
        r.is_warranty_return,
        
        -- Quantities
        r.quantity_returned,
        
        -- Amounts
        r.refund_amount,
        r.restocking_fee,
        r.shipping_label_cost,
        r.net_refund_amount,
        
        -- Dates
        r.return_request_date,
        r.approved_date,
        r.received_date,
        r.refund_date,
        
        -- Metrics
        r.days_to_approval,
        r.days_to_refund,
        
        -- Product attributes
        p.category as product_category,
        p.subcategory as product_subcategory,
        p.brand as product_brand,
        
        -- Customer attributes
        c.customer_segment,
        c.customer_type,
        
        current_timestamp() as _dbt_loaded_at
    from returns r
    left join products p on r.product_id = p.product_id
    left join customers c on r.customer_id = c.customer_id
)

select * from final
