# Physical Product Platform - dbt Project

This dbt project transforms raw data from the physical product platform into analytics-ready dimensional models.

## Project Structure

```
models/
├── sources.yml          # Source table definitions
├── staging/            # Staging models (1:1 with source tables)
│   ├── stg_products.sql
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   ├── stg_order_lines.sql
│   ├── stg_shipments.sql
│   ├── stg_returns.sql
│   ├── stg_waste.sql
│   └── stg_quality_inspections.sql
└── marts/              # Analytics-ready models
    ├── core/          # Dimensional model
    │   ├── dim_products.sql
    │   ├── dim_customers.sql
    │   ├── dim_date.sql
    │   ├── fact_sales.sql
    │   ├── fact_returns.sql
    │   ├── fact_quality.sql
    │   └── fact_waste.sql
    └── metrics/       # Pre-aggregated metrics
        ├── metrics_sales_performance.sql
        ├── metrics_product_performance.sql
        └── metrics_customer_analytics.sql
```

## Setup

1. Install dbt:
```bash
pip install dbt-databricks  # or dbt-snowflake or dbt-bigquery
```

2. Configure your profile in `~/.dbt/profiles.yml` using the template in `profiles.yml`

3. Install dependencies:
```bash
dbt deps
```

4. Test connection:
```bash
dbt debug
```

## Running the Project

Run all models:
```bash
dbt run
```

Run tests:
```bash
dbt test
```

Generate documentation:
```bash
dbt docs generate
dbt docs serve
```

## Model Layers

### Staging Layer
- **Purpose**: Clean and standardize raw data
- **Materialization**: Views
- **Naming**: `stg_<source_table>`
- **Tests**: Schema tests on sources

### Core Layer (Marts)
- **Purpose**: Dimensional model for analytics
- **Materialization**: Tables
- **Models**:
  - **Dimensions**: Products, Customers, Date
  - **Facts**: Sales, Returns, Quality, Waste
- **Grain**: Clearly defined for each fact table

### Metrics Layer
- **Purpose**: Pre-aggregated metrics for BI tools
- **Materialization**: Views
- **Use Case**: Tableau dashboards, reporting

## Key Metrics

### Sales Metrics
- Revenue, gross profit, gross margin %
- Units sold, order count
- Average order value
- Discount %

### Product Metrics
- Product performance by category/SKU
- Return rate by product
- Quality pass rate
- Waste cost by product

### Customer Metrics
- Customer Lifetime Value (CLV)
- RFM segmentation (Recency, Frequency, Monetary)
- Customer lifecycle stages
- Retention and churn

### Quality Metrics
- Defect rate
- Quality pass rate
- Cost of quality
- Inspection compliance

### Waste Metrics
- Waste cost by category
- Carbon footprint
- Environmental impact score
- Preventable vs. non-preventable waste

## Testing Strategy

1. **Source Tests**: Uniqueness, not null, relationships
2. **Schema Tests**: Data type validation
3. **Data Quality Tests**: Business logic validation
4. **Custom Tests**: Domain-specific validations

## Data Freshness

Models can be configured to check data freshness:
```yaml
freshness:
  warn_after: {count: 24, period: hour}
  error_after: {count: 48, period: hour}
```

## Performance Optimization

- Staging models: Materialized as views (low cost)
- Core models: Materialized as tables (performance)
- Metrics models: Materialized as views (always fresh)
- Incremental models: Can be added for large fact tables

## Contributing

When adding new models:
1. Follow naming conventions
2. Add appropriate tests
3. Document model purpose and grain
4. Update this README
