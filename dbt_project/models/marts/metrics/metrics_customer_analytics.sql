{{
    config(
        materialized='view',
        schema='marts'
    )
}}

-- Customer Analytics Metrics
-- Tableau-ready view for customer analytics including RFM

with customer_summary as (
    select
        c.customer_id,
        c.customer_name,
        c.customer_type,
        c.customer_segment,
        c.city,
        c.state,
        c.account_created_date,
        
        -- RFM Components
        max(s.date_key) as last_purchase_date,
        datediff('day', max(s.date_key), current_date()) as recency_days,
        count(distinct s.order_id) as frequency_orders,
        sum(s.net_line_total) as monetary_value,
        
        -- Additional metrics
        avg(s.net_line_total) as avg_order_value,
        sum(s.quantity) as total_units_purchased,
        
        -- Return metrics
        coalesce(count(distinct r.return_id), 0) as total_returns,
        coalesce(sum(r.refund_amount), 0) as total_refunds
        
    from {{ ref('dim_customers') }} c
    left join {{ ref('fact_sales') }} s on c.customer_id = s.customer_id
    left join {{ ref('fact_returns') }} r on c.customer_id = r.customer_id
    group by 1, 2, 3, 4, 5, 6, 7
),

rfm_scores as (
    select
        *,
        -- RFM Scores (1-5, 5 is best)
        ntile(5) over (order by recency_days desc) as recency_score,
        ntile(5) over (order by frequency_orders) as frequency_score,
        ntile(5) over (order by monetary_value) as monetary_score
    from customer_summary
),

final as (
    select
        *,
        -- Combined RFM Score
        (recency_score + frequency_score + monetary_score) as rfm_total_score,
        concat(cast(recency_score as varchar), cast(frequency_score as varchar), cast(monetary_score as varchar)) as rfm_segment,
        
        -- Customer Classification
        case
            when recency_score >= 4 and frequency_score >= 4 and monetary_score >= 4 then 'Champions'
            when recency_score >= 3 and frequency_score >= 3 and monetary_score >= 3 then 'Loyal Customers'
            when recency_score >= 4 and frequency_score <= 2 and monetary_score <= 2 then 'Promising'
            when recency_score >= 3 and frequency_score <= 3 and monetary_score <= 3 then 'Potential Loyalists'
            when recency_score <= 2 and frequency_score >= 3 and monetary_score >= 3 then 'At Risk'
            when recency_score <= 2 and frequency_score <= 2 and monetary_score >= 4 then 'Cant Lose Them'
            when recency_score >= 3 and frequency_score <= 2 and monetary_score <= 2 then 'Need Attention'
            else 'Others'
        end as customer_lifecycle_stage,
        
        -- Return rate
        round(total_returns * 100.0 / nullif(frequency_orders, 0), 2) as return_rate_pct,
        
        -- Customer lifetime value
        round(monetary_value - total_refunds, 2) as net_clv
        
    from rfm_scores
)

select * from final
