# Metrics Guide

Comprehensive guide to key metrics, KPIs, and analytical queries for the Physical Product Platform.

## Overview

This guide documents the key metrics available in the data marts, how they're calculated, and example queries for common analytics use cases.

## Metric Categories

### 1. Sales Performance Metrics
### 2. Product Performance Metrics
### 3. Customer Analytics Metrics
### 4. Operational Efficiency Metrics
### 5. Quality Metrics
### 6. Sustainability Metrics

---

## 1. Sales Performance Metrics

### Revenue Metrics

#### Total Revenue
```sql
SELECT 
    SUM(revenue) as total_revenue
FROM marts.metrics_sales_performance
WHERE date_key >= '2024-01-01';
```

#### Revenue by Category
```sql
SELECT 
    product_category,
    SUM(revenue) as total_revenue,
    ROUND(SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER(), 2) as pct_of_total
FROM marts.metrics_sales_performance
GROUP BY product_category
ORDER BY total_revenue DESC;
```

#### Revenue Trends (Monthly)
```sql
SELECT 
    order_month,
    SUM(revenue) as monthly_revenue,
    SUM(gross_profit) as monthly_profit,
    ROUND(SUM(gross_profit) / NULLIF(SUM(revenue), 0) * 100, 2) as profit_margin_pct
FROM marts.metrics_sales_performance
GROUP BY order_month
ORDER BY order_month;
```

### Order Metrics

#### Average Order Value (AOV)
```sql
SELECT 
    AVG(avg_order_value) as overall_aov,
    customer_segment,
    AVG(avg_order_value) as segment_aov
FROM marts.metrics_sales_performance
GROUP BY customer_segment;
```

#### Order Volume by Day of Week
```sql
SELECT 
    DAYOFWEEK(date_key) as day_of_week,
    CASE DAYOFWEEK(date_key)
        WHEN 1 THEN 'Sunday'
        WHEN 2 THEN 'Monday'
        WHEN 3 THEN 'Tuesday'
        WHEN 4 THEN 'Wednesday'
        WHEN 5 THEN 'Thursday'
        WHEN 6 THEN 'Friday'
        WHEN 7 THEN 'Saturday'
    END as day_name,
    SUM(order_count) as total_orders,
    AVG(order_count) as avg_daily_orders
FROM marts.metrics_sales_performance
GROUP BY day_of_week, day_name
ORDER BY day_of_week;
```

### Profitability Metrics

#### Gross Margin Analysis
```sql
SELECT 
    product_category,
    SUM(revenue) as revenue,
    SUM(gross_profit) as profit,
    ROUND(AVG(gross_margin_pct), 2) as avg_margin_pct
FROM marts.metrics_sales_performance
GROUP BY product_category
ORDER BY profit DESC;
```

---

## 2. Product Performance Metrics

### Product Rankings

#### Top 10 Products by Revenue
```sql
SELECT 
    product_name,
    sku,
    category,
    total_revenue,
    total_units_sold,
    gross_margin_pct,
    return_rate_pct
FROM marts.metrics_product_performance
ORDER BY total_revenue DESC
LIMIT 10;
```

#### Bottom 10 Products by Margin
```sql
SELECT 
    product_name,
    sku,
    total_revenue,
    gross_margin_pct,
    return_rate_pct,
    quality_pass_rate_pct
FROM marts.metrics_product_performance
WHERE total_orders > 10  -- Filter for statistical significance
ORDER BY gross_margin_pct ASC
LIMIT 10;
```

### Inventory Metrics

#### Products Needing Attention
```sql
SELECT 
    p.product_name,
    p.sku,
    m.total_units_sold / NULLIF(DATEDIFF('day', MIN(s.date_key), MAX(s.date_key)), 0) as avg_daily_sales,
    p.reorder_point,
    p.lead_time_days,
    CASE 
        WHEN m.total_units_sold > 0 THEN 'High Demand'
        WHEN m.return_rate_pct > 10 THEN 'High Returns'
        WHEN m.quality_pass_rate_pct < 90 THEN 'Quality Issues'
        ELSE 'Normal'
    END as status
FROM marts.dim_products p
LEFT JOIN marts.metrics_product_performance m ON p.product_id = m.product_id
LEFT JOIN marts.fact_sales s ON p.product_id = s.product_id
GROUP BY p.product_name, p.sku, m.total_units_sold, p.reorder_point, p.lead_time_days, m.return_rate_pct, m.quality_pass_rate_pct
ORDER BY avg_daily_sales DESC;
```

---

## 3. Customer Analytics Metrics

### Customer Segmentation (RFM)

#### Customer Segments Distribution
```sql
SELECT 
    customer_lifecycle_stage,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as pct_of_total,
    AVG(monetary_value) as avg_value,
    AVG(frequency_orders) as avg_orders
FROM marts.metrics_customer_analytics
GROUP BY customer_lifecycle_stage
ORDER BY customer_count DESC;
```

#### Champions Analysis
```sql
SELECT 
    customer_name,
    customer_segment,
    monetary_value,
    frequency_orders,
    recency_days,
    avg_order_value,
    net_clv
FROM marts.metrics_customer_analytics
WHERE customer_lifecycle_stage = 'Champions'
ORDER BY net_clv DESC
LIMIT 20;
```

### Customer Lifetime Value

#### CLV by Segment
```sql
SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    AVG(net_clv) as avg_clv,
    SUM(net_clv) as total_clv,
    AVG(frequency_orders) as avg_orders,
    AVG(monetary_value) as avg_revenue
FROM marts.metrics_customer_analytics
GROUP BY customer_segment
ORDER BY total_clv DESC;
```

### Customer Retention

#### Cohort Analysis (Monthly)
```sql
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', account_created_date) as cohort_month
    FROM marts.dim_customers
),
cohort_orders AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC('month', s.date_key) as order_month,
        COUNT(DISTINCT s.customer_id) as active_customers
    FROM customer_cohorts c
    LEFT JOIN marts.fact_sales s ON c.customer_id = s.customer_id
    GROUP BY c.cohort_month, order_month
)
SELECT 
    cohort_month,
    order_month,
    active_customers,
    DATEDIFF('month', cohort_month, order_month) as months_since_first_order
FROM cohort_orders
ORDER BY cohort_month, order_month;
```

---

## 4. Operational Efficiency Metrics

### Fulfillment Metrics

#### On-Time Delivery Rate
```sql
SELECT 
    carrier,
    COUNT(*) as total_shipments,
    SUM(is_on_time_delivery) as on_time_deliveries,
    ROUND(SUM(is_on_time_delivery) * 100.0 / COUNT(*), 2) as on_time_pct,
    AVG(actual_transit_days) as avg_transit_days,
    AVG(days_delayed) as avg_delay_days
FROM staging.stg_shipments
WHERE shipment_status = 'Delivered'
GROUP BY carrier
ORDER BY on_time_pct DESC;
```

#### Average Fulfillment Time
```sql
SELECT 
    service_level,
    COUNT(*) as shipment_count,
    AVG(expected_transit_days) as avg_expected_days,
    AVG(actual_transit_days) as avg_actual_days,
    ROUND((AVG(actual_transit_days) - AVG(expected_transit_days)) / NULLIF(AVG(expected_transit_days), 0) * 100, 2) as variance_pct
FROM staging.stg_shipments
WHERE actual_delivery_date IS NOT NULL
GROUP BY service_level;
```

### Return Metrics

#### Return Rate by Category
```sql
SELECT 
    product_category,
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT return_id) as total_returns,
    ROUND(COUNT(DISTINCT return_id) * 100.0 / NULLIF(COUNT(DISTINCT order_id), 0), 2) as return_rate_pct,
    AVG(net_refund_amount) as avg_refund
FROM marts.fact_returns
GROUP BY product_category
ORDER BY return_rate_pct DESC;
```

#### Return Reasons Analysis
```sql
SELECT 
    return_reason,
    COUNT(*) as return_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as pct_of_returns,
    SUM(refund_amount) as total_refund_amount,
    AVG(days_to_refund) as avg_processing_days
FROM marts.fact_returns
GROUP BY return_reason
ORDER BY return_count DESC;
```

---

## 5. Quality Metrics

### Quality Pass Rate

#### Overall Quality Performance
```sql
SELECT 
    DATE_TRUNC('month', inspection_date) as month,
    COUNT(*) as total_inspections,
    SUM(is_passed) as passed_inspections,
    ROUND(SUM(is_passed) * 100.0 / COUNT(*), 2) as pass_rate_pct,
    AVG(defect_rate) as avg_defect_rate
FROM marts.fact_quality
GROUP BY month
ORDER BY month;
```

#### Quality by Product Category
```sql
SELECT 
    product_category,
    COUNT(*) as inspections,
    ROUND(AVG(CASE WHEN is_passed = 1 THEN 100.0 ELSE 0 END), 2) as pass_rate_pct,
    AVG(defect_rate) as avg_defect_rate,
    SUM(cost_of_quality) as total_quality_cost
FROM marts.fact_quality
GROUP BY product_category
ORDER BY pass_rate_pct ASC;
```

### Defect Analysis

#### Defects by Type and Severity
```sql
SELECT 
    defect_type,
    severity_level,
    COUNT(*) as defect_count,
    AVG(cost_of_quality) as avg_cost,
    SUM(cost_of_quality) as total_cost
FROM marts.fact_quality
WHERE defect_type IS NOT NULL
GROUP BY defect_type, severity_level
ORDER BY defect_count DESC;
```

---

## 6. Sustainability Metrics

### Waste Metrics

#### Waste by Category
```sql
SELECT 
    waste_category,
    COUNT(*) as waste_records,
    SUM(quantity) as total_quantity,
    SUM(total_waste_cost) as total_cost,
    SUM(carbon_footprint_kg) as total_carbon_kg,
    AVG(environmental_impact_score) as avg_impact_score,
    ROUND(SUM(CASE WHEN is_preventable THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as preventable_pct
FROM marts.fact_waste
GROUP BY waste_category
ORDER BY total_cost DESC;
```

#### Waste Reduction Opportunities
```sql
SELECT 
    waste_type,
    root_cause,
    COUNT(*) as occurrences,
    SUM(total_waste_cost) as potential_savings,
    SUM(carbon_footprint_kg) as carbon_impact
FROM marts.fact_waste
WHERE is_preventable = TRUE
GROUP BY waste_type, root_cause
HAVING COUNT(*) > 10
ORDER BY potential_savings DESC
LIMIT 20;
```

### Environmental Impact

#### Carbon Footprint Trends
```sql
SELECT 
    DATE_TRUNC('month', waste_date) as month,
    SUM(carbon_footprint_kg) as total_carbon_kg,
    SUM(carbon_footprint_kg) / 1000.0 as carbon_tonnes,
    AVG(environmental_impact_score) as avg_impact_score
FROM marts.fact_waste
GROUP BY month
ORDER BY month;
```

---

## Dashboard Recommendations

### Executive Dashboard
- **Key Metrics**: Revenue, Gross Margin, Order Volume, Customer Count
- **Trends**: Monthly revenue trends, YoY comparisons
- **Alerts**: Drop in revenue >10%, margin below threshold

### Operations Dashboard
- **Key Metrics**: On-time delivery rate, return rate, fulfillment time
- **Trends**: Daily/weekly performance
- **Alerts**: Delivery delays, high return rates

### Product Dashboard
- **Key Metrics**: Product performance, inventory levels, quality metrics
- **Trends**: Product lifecycle, seasonality
- **Alerts**: Low inventory, quality issues

### Customer Dashboard
- **Key Metrics**: CLV, customer segments, retention rate
- **Trends**: Customer acquisition, churn rate
- **Alerts**: At-risk customers, high-value churn

### Quality Dashboard
- **Key Metrics**: Quality pass rate, defect rate, cost of quality
- **Trends**: Monthly quality trends
- **Alerts**: Below target pass rates, high defect costs

### Sustainability Dashboard
- **Key Metrics**: Waste cost, carbon footprint, recycling rate
- **Trends**: Waste reduction over time
- **Alerts**: Increase in preventable waste

---

## Query Performance Tips

1. **Use date filters**: Always filter on date columns which are often partitioned
2. **Leverage metrics views**: Pre-aggregated for common queries
3. **Avoid SELECT ***: Specify only needed columns
4. **Use appropriate aggregations**: Consider whether you need row-level or aggregated data
5. **Test queries**: Start with LIMIT clause during development

## Next Steps

1. Connect Tableau to the data warehouse
2. Import these queries as starting points for dashboards
3. Customize metrics based on business needs
4. Set up scheduled refresh for dashboards
5. Configure alerts for key thresholds
