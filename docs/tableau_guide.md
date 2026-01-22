# Tableau Connection Guide

Guide for connecting Tableau to the Physical Product Platform data marts.

## Prerequisites

- Tableau Desktop or Tableau Server
- Access to your data warehouse (Databricks, Snowflake, or BigQuery)
- Data marts created (run dbt models first)

## Connection Steps

### Option 1: Databricks

1. **Open Tableau Desktop**
2. **Click "Connect" → "To a Server" → "Databricks"**
3. **Enter connection details:**
   - Server: `your-workspace.cloud.databricks.com`
   - HTTP Path: `/sql/1.0/warehouses/your-warehouse-id`
   - Authentication: Personal Access Token
   - Token: Your Databricks token
4. **Select catalog:** `physical_product_raw`
5. **Select schema:** `marts`

### Option 2: Snowflake

1. **Open Tableau Desktop**
2. **Click "Connect" → "To a Server" → "Snowflake"**
3. **Enter connection details:**
   - Server: `your-account.snowflakecomputing.com`
   - Authentication: Username and Password
   - Warehouse: `COMPUTE_WH`
   - Database: `PHYSICAL_PRODUCT_DB`
   - Schema: `MARTS`
4. **Sign In**

### Option 3: BigQuery

1. **Open Tableau Desktop**
2. **Click "Connect" → "To a Server" → "Google BigQuery"**
3. **Select OAuth or Service Account authentication**
4. **Select Project:** `your-project-id`
5. **Select Dataset:** `physical_product_raw`

## Recommended Data Sources

### For Sales Analysis
**Data Source Name:** Sales Performance

**Tables to connect:**
- `marts.fact_sales` (Primary)
- `marts.dim_products` (Join on product_id)
- `marts.dim_customers` (Join on customer_id)
- `marts.dim_date` (Join on date_key)

**Or use the pre-aggregated view:**
- `marts.metrics_sales_performance`

**Join Configuration:**
```
fact_sales.product_id = dim_products.product_id (Inner Join)
fact_sales.customer_id = dim_customers.customer_id (Inner Join)
fact_sales.date_key = dim_date.date_key (Inner Join)
```

### For Product Performance
**Data Source Name:** Product Analytics

**Tables to connect:**
- `marts.metrics_product_performance` (Primary)
- `marts.dim_products` (Join on product_id for additional attributes)

### For Customer Analytics
**Data Source Name:** Customer Insights

**Tables to connect:**
- `marts.metrics_customer_analytics` (Primary)
- `marts.dim_customers` (Join on customer_id for additional attributes)

### For Quality Monitoring
**Data Source Name:** Quality Dashboard

**Tables to connect:**
- `marts.fact_quality` (Primary)
- `marts.dim_products` (Join on product_id)
- `marts.dim_date` (Join on date_key)

## Creating Your First Dashboard

### Sales Performance Dashboard

**Recommended Sheets:**

1. **Revenue Trend**
   - Chart Type: Line Chart
   - X-Axis: `order_month` or `date_key`
   - Y-Axis: SUM(`revenue`)
   - Color: `product_category`

2. **Revenue by Category**
   - Chart Type: Bar Chart
   - Rows: `product_category`
   - Columns: SUM(`revenue`)
   - Color: `product_category`
   - Sort: Descending by revenue

3. **Top Products**
   - Chart Type: Bar Chart
   - Rows: `product_name`
   - Columns: SUM(`net_line_total`)
   - Filters: Top 10 by revenue

4. **KPI Cards**
   - Total Revenue: SUM(`revenue`)
   - Gross Margin %: SUM(`gross_profit`) / SUM(`revenue`) * 100
   - Order Count: COUNT(DISTINCT `order_id`)
   - Average Order Value: SUM(`revenue`) / COUNT(DISTINCT `order_id`)

### Customer Analytics Dashboard

**Recommended Sheets:**

1. **Customer Segments**
   - Chart Type: Pie Chart
   - Angle: COUNT(`customer_id`)
   - Color: `customer_lifecycle_stage`

2. **RFM Heatmap**
   - Chart Type: Heatmap
   - Columns: `recency_score`
   - Rows: `frequency_score`
   - Color: AVG(`monetary_score`)
   - Size: COUNT(`customer_id`)

3. **CLV Distribution**
   - Chart Type: Histogram
   - Columns: `net_clv` (bins)
   - Rows: COUNT(`customer_id`)

4. **Customer Trends**
   - Chart Type: Area Chart
   - Columns: `account_created_date` (Month)
   - Rows: Running Count of `customer_id`
   - Color: `customer_segment`

## Best Practices

### Performance Optimization

1. **Use Extracts for Large Datasets**
   - For datasets > 1M rows, create Tableau extracts
   - Schedule extract refreshes (daily/hourly as needed)
   - Use incremental refresh where possible

2. **Leverage Aggregate Tables**
   - Use `metrics_*` views for dashboard-level metrics
   - Use fact/dimension tables for detailed analysis
   - Pre-aggregate in dbt when possible

3. **Filter Early**
   - Add date range filters to data source
   - Use context filters for better performance
   - Consider relative date filters (Last 90 days, etc.)

4. **Optimize Calculations**
   - Create calculated fields in dbt instead of Tableau
   - Use table calculations sparingly
   - Pre-calculate complex metrics in the database

### Data Modeling

1. **Star Schema Connections**
   - Connect fact tables to dimension tables
   - Use inner joins for required relationships
   - Use left joins for optional relationships

2. **Date Handling**
   - Always use `dim_date` for time intelligence
   - Leverage pre-built date attributes (quarter, month, week)
   - Create date hierarchies for drill-down

3. **Custom Calculations**
   ```
   // Year-over-Year Growth
   (SUM([Revenue]) - LOOKUP(SUM([Revenue]), -12)) / LOOKUP(SUM([Revenue]), -12)
   
   // Running Total
   RUNNING_SUM(SUM([Revenue]))
   
   // Percent of Total
   SUM([Revenue]) / TOTAL(SUM([Revenue]))
   ```

### Dashboard Design

1. **Layout Structure**
   - Place KPIs at the top
   - Main visualizations in the center
   - Filters on the left or top
   - Details/drill-down at the bottom

2. **Interactivity**
   - Add dashboard filters for date, category, etc.
   - Enable hover tooltips with additional context
   - Use dashboard actions for drill-down
   - Add "Reset" button for filters

3. **Color Palette**
   - Use consistent colors across dashboards
   - Green for positive trends
   - Red for negative/alerts
   - Blue/neutral for standard metrics

## Example Calculated Fields

### Sales Metrics
```
// Gross Margin %
SUM([gross_profit]) / SUM([revenue]) * 100

// Units Per Order
SUM([quantity]) / COUNTD([order_id])

// Discount Impact
SUM([discount_amount]) / (SUM([revenue]) + SUM([discount_amount])) * 100
```

### Customer Metrics
```
// Average Customer Lifetime Value
SUM([monetary_value]) / COUNTD([customer_id])

// Active Customers (Last 90 Days)
COUNTD(IF DATEDIFF('day', [last_purchase_date], TODAY()) <= 90 THEN [customer_id] END)

// Customer Retention Rate
COUNTD(IF [recency_days] <= 90 THEN [customer_id] END) / COUNTD([customer_id])
```

### Product Metrics
```
// Inventory Turnover
SUM([units_sold]) / AVG([reorder_point])

// Product Performance Score
([total_revenue] * [quality_pass_rate_pct] / 100) - [total_waste_cost]
```

## Troubleshooting

### Connection Issues

**Problem:** Can't connect to database
- **Solution:** Verify credentials, network access, and warehouse is running

**Problem:** Tables not showing up
- **Solution:** Ensure dbt models have been run, refresh metadata in Tableau

### Performance Issues

**Problem:** Dashboard is slow
- **Solution:** Create extract, add date filters, use aggregate tables

**Problem:** Out of memory errors
- **Solution:** Reduce data volume with filters, use incremental extracts

### Data Issues

**Problem:** Numbers don't match expectations
- **Solution:** Check join conditions, verify no duplicate rows, check date filters

**Problem:** Missing data
- **Solution:** Verify dbt runs completed, check source data freshness

## Publishing to Tableau Server

1. **Prepare Dashboard**
   - Test with extract
   - Verify all filters work
   - Add clear titles and descriptions

2. **Publish**
   - File → Tableau Server → Publish Workbook
   - Select project
   - Choose authentication method
   - Set permissions

3. **Schedule Refreshes**
   - For extracts: Set refresh schedule (e.g., daily at 5 AM)
   - For live connections: No refresh needed

4. **Set Up Alerts**
   - Configure data-driven alerts for key metrics
   - Set thresholds (e.g., alert if revenue drops 10%)
   - Choose notification recipients

## Additional Resources

- [Tableau Documentation](https://help.tableau.com/)
- [dbt Documentation](https://docs.getdbt.com/)
- Project-specific docs in `docs/metrics.md`
- Sample queries in `docs/metrics.md`

## Support

For issues with:
- **Data accuracy**: Check dbt models and run `dbt test`
- **Performance**: Review query performance in warehouse
- **Tableau-specific**: Consult Tableau documentation
- **Project structure**: See `docs/architecture.md`
