{{
    config(
        materialized='view',
        schema='marts'
    )
}}

-- Product Performance Metrics
-- Tableau-ready view for product analytics

with product_metrics as (
    select
        p.product_id,
        p.product_name,
        p.sku,
        p.category,
        p.subcategory,
        p.brand,
        
        -- Sales metrics
        count(distinct s.order_id) as total_orders,
        sum(s.quantity) as total_units_sold,
        sum(s.net_line_total) as total_revenue,
        sum(s.gross_profit) as total_gross_profit,
        avg(s.unit_price) as avg_selling_price,
        
        -- Return metrics
        coalesce(sum(r.quantity_returned), 0) as total_units_returned,
        coalesce(sum(r.refund_amount), 0) as total_refund_amount,
        
        -- Quality metrics
        coalesce(count(distinct q.inspection_id), 0) as total_inspections,
        coalesce(sum(case when q.is_passed = 1 then 1 else 0 end), 0) as passed_inspections,
        coalesce(avg(q.defect_rate), 0) as avg_defect_rate,
        
        -- Waste metrics
        coalesce(sum(w.total_waste_cost), 0) as total_waste_cost
        
    from {{ ref('dim_products') }} p
    left join {{ ref('fact_sales') }} s on p.product_id = s.product_id
    left join {{ ref('fact_returns') }} r on p.product_id = r.product_id
    left join {{ ref('fact_quality') }} q on p.product_id = q.product_id
    left join {{ ref('fact_waste') }} w on p.product_id = w.product_id
    group by 1, 2, 3, 4, 5, 6
)

select 
    *,
    -- Calculated metrics
    round(total_gross_profit / nullif(total_revenue, 0) * 100, 2) as gross_margin_pct,
    round(total_units_returned * 100.0 / nullif(total_units_sold, 0), 2) as return_rate_pct,
    round(passed_inspections * 100.0 / nullif(total_inspections, 0), 2) as quality_pass_rate_pct,
    round((total_revenue - total_gross_profit - total_refund_amount - total_waste_cost), 2) as net_contribution
from product_metrics
