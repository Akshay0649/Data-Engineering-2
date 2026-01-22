# Physical Product Platform - Analytics Engineering Project

A production-ready analytics engineering project simulating a comprehensive physical product platform with end-to-end data pipeline, transformations, and analytics capabilities.

## 🎯 Project Overview

This project demonstrates a complete analytics engineering solution for a physical product platform, covering the entire data lifecycle from raw data generation to analytics-ready data marts. It includes data generators, ingestion pipelines, data transformations using dbt, orchestration with Airflow, and analytics-ready outputs for BI tools like Tableau.

## 📊 Business Domains

The project covers 8 key business domains:

1. **Products** - Product catalog, SKUs, categories, pricing
2. **Recipes** - Bill of materials, ingredients, manufacturing recipes
3. **Customers** - Customer demographics, segments, accounts
4. **Orders** - Sales orders, order lines, order status
5. **Shipments** - Delivery tracking, logistics, fulfillment
6. **Returns** - Return requests, reasons, refund processing
7. **Waste** - Manufacturing waste, scrap tracking, sustainability metrics
8. **Quality** - Quality control checks, defects, compliance

## 🏗️ Architecture

```
┌─────────────────┐
│ Data Generators │ (Python CSV Generators)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Raw Data Lake  │ (CSV Files)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Ingestion    │ (Python Scripts + Airflow)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Data Warehouse │ (Databricks/Snowflake/BigQuery)
│   Raw Layer     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  dbt Transform  │ (Staging + Marts)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analytics Layer │ (Tableau-Ready Marts)
└─────────────────┘
```

## 📁 Project Structure

```
.
├── data_generators/          # Python scripts to generate sample data
│   ├── generate_products.py
│   ├── generate_recipes.py
│   ├── generate_customers.py
│   ├── generate_orders.py
│   ├── generate_shipments.py
│   ├── generate_returns.py
│   ├── generate_waste.py
│   ├── generate_quality.py
│   └── generate_all.py
├── ingestion/               # Data ingestion scripts
│   ├── ingest_to_databricks.py
│   ├── ingest_to_snowflake.py
│   ├── ingest_to_bigquery.py
│   └── config.yaml
├── schemas/                 # Database schema definitions
│   ├── databricks/
│   ├── snowflake/
│   └── bigquery/
├── dbt_project/            # dbt transformation project
│   ├── models/
│   │   ├── staging/       # Staging models (1:1 with sources)
│   │   └── marts/         # Analytics marts (dimensional model)
│   ├── tests/             # Data quality tests
│   ├── macros/            # Reusable SQL macros
│   └── dbt_project.yml
├── airflow/                # Airflow orchestration
│   ├── dags/
│   │   ├── dag_ingestion.py
│   │   ├── dag_dbt_transform.py
│   │   └── dag_quality_checks.py
│   └── config/
├── docs/                   # Documentation
│   ├── setup.md
│   ├── architecture.md
│   └── metrics.md
└── sample_data/           # Generated sample data (gitignored)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda
- Access to one of: Databricks, Snowflake, or BigQuery
- Apache Airflow (optional, for orchestration)
- dbt-core (for transformations)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Akshay0649/Data-Engineering-2.git
cd Data-Engineering-2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate sample data:
```bash
python data_generators/generate_all.py
```

4. Configure your data warehouse connection in `ingestion/config.yaml`

5. Run ingestion:
```bash
python ingestion/ingest_to_[platform].py
```

6. Run dbt transformations:
```bash
cd dbt_project
dbt deps
dbt run
dbt test
```

## 📈 Key Metrics & KPIs

### Product Operations
- **Product Performance**: Sales by SKU, category, region
- **Inventory Turnover**: Stock velocity, reorder points
- **Recipe Efficiency**: Ingredient utilization, yield rates

### Customer Analytics
- **Customer Lifetime Value (CLV)**: Revenue per customer over time
- **Customer Segmentation**: RFM analysis, cohort analysis
- **Retention Metrics**: Repeat purchase rate, churn rate

### Order Fulfillment
- **Order Metrics**: Order volume, average order value, order frequency
- **Fulfillment Rate**: On-time delivery, shipping time
- **Return Rate**: Returns by category, return reasons

### Quality & Waste
- **Quality Metrics**: Defect rate, quality score, compliance rate
- **Waste Metrics**: Waste percentage, scrap cost, sustainability score
- **Operational Efficiency**: Overall Equipment Effectiveness (OEE)

## 🧪 Testing Strategy

The project includes multiple layers of testing:

1. **Schema Tests** (dbt): Uniqueness, not null, relationships, accepted values
2. **Data Quality Tests** (dbt): Custom business logic validation
3. **Ingestion Tests**: Data completeness, format validation
4. **Airflow Tests**: DAG integrity, task dependencies

## 📚 Documentation

- [Setup Guide](docs/setup.md) - Detailed installation and configuration
- [Architecture](docs/architecture.md) - System design and data flow
- [Metrics Guide](docs/metrics.md) - Available metrics and calculations

## 🔧 Technologies Used

- **Data Generation**: Python, Faker, pandas
- **Data Warehouses**: Databricks, Snowflake, BigQuery
- **Transformation**: dbt (data build tool)
- **Orchestration**: Apache Airflow
- **BI/Visualization**: Tableau (compatible outputs)
- **Version Control**: Git

## 🤝 Contributing

This is a demonstration project. Feel free to fork and adapt for your own use cases.

## 📝 License

MIT License

## 👤 Author

Akshay0649

---

**Note**: This is a simulated environment for learning and demonstration purposes. Adapt configurations for production use. 
