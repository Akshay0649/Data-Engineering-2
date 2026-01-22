# Setup Guide

Complete setup instructions for the Physical Product Platform analytics engineering project.

## Prerequisites

### Software Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Access to one of:
  - Databricks workspace
  - Snowflake account
  - Google Cloud Platform (for BigQuery)
- Apache Airflow (optional, for orchestration)
- Tableau Desktop or Tableau Server (optional, for visualization)

### Python Libraries
All required Python libraries are listed in `requirements.txt`.

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Akshay0649/Data-Engineering-2.git
cd Data-Engineering-2
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Generate Sample Data

```bash
cd data_generators
python generate_all.py
```

This will create CSV files in the `sample_data/` directory.

### 4. Configure Data Warehouse Connection

#### Option A: Databricks

1. Copy the config template:
```bash
cd ingestion
cp config_template.yaml config.yaml
```

2. Edit `config.yaml` and fill in Databricks credentials:
```yaml
platform: "databricks"
databricks:
  server_hostname: "your-workspace.cloud.databricks.com"
  http_path: "/sql/1.0/warehouses/your-warehouse-id"
  access_token: "your-access-token"
  catalog: "physical_product_raw"
```

3. Create database schema:
```bash
# Run the SQL script in Databricks SQL Editor
# File: schemas/databricks/create_raw_tables.sql
```

#### Option B: Snowflake

1. Configure Snowflake in `config.yaml`:
```yaml
platform: "snowflake"
snowflake:
  account: "your-account.snowflakecomputing.com"
  user: "your-username"
  password: "your-password"
  warehouse: "COMPUTE_WH"
  database: "PHYSICAL_PRODUCT_DB"
  schema: "RAW"
```

2. Create database schema:
```sql
-- Run in Snowflake
-- File: schemas/snowflake/create_raw_tables.sql
```

#### Option C: BigQuery

1. Set up service account and download credentials JSON

2. Configure BigQuery in `config.yaml`:
```yaml
platform: "bigquery"
bigquery:
  project_id: "your-project-id"
  dataset_id: "physical_product_raw"
  credentials_path: "path/to/service-account-key.json"
  location: "US"
```

3. Create dataset and tables:
```bash
bq mk --dataset physical_product_raw
# Then run the SQL from schemas/bigquery/create_raw_tables.sql
```

### 5. Run Data Ingestion

```bash
cd ingestion
python ingest_to_[databricks|snowflake|bigquery].py
```

### 6. Set Up dbt

#### Install dbt for your platform:

```bash
# For Databricks
pip install dbt-databricks

# For Snowflake
pip install dbt-snowflake

# For BigQuery
pip install dbt-bigquery
```

#### Configure dbt profile:

```bash
# Copy profile template
cp dbt_project/profiles.yml ~/.dbt/profiles.yml

# Edit ~/.dbt/profiles.yml with your credentials
```

#### Install dbt dependencies:

```bash
cd dbt_project
dbt deps
```

#### Test connection:

```bash
dbt debug
```

#### Run dbt models:

```bash
# Run all models
dbt run

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

### 7. Set Up Airflow (Optional)

#### Install Airflow:

```bash
pip install apache-airflow==2.10.4
```

#### Initialize Airflow database:

```bash
export AIRFLOW_HOME=~/airflow
airflow db init
```

#### Create admin user:

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

#### Configure Airflow variables:

```bash
# Set project root
airflow variables set project_root /path/to/Data-Engineering-2

# Set platform
airflow variables set platform databricks

# Set config path
airflow variables set config_path ingestion/config.yaml
```

#### Copy DAGs to Airflow:

```bash
cp -r airflow/dags/* $AIRFLOW_HOME/dags/
```

#### Start Airflow:

```bash
# Start web server
airflow webserver --port 8080

# Start scheduler (in another terminal)
airflow scheduler
```

Access Airflow UI at http://localhost:8080

## Verification

### Check Data Generation
```bash
ls -lh sample_data/
```
You should see 10 CSV files.

### Check Data Ingestion
Run a query in your data warehouse:
```sql
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;
```

### Check dbt Models
```bash
cd dbt_project
dbt run
dbt test
```

All tests should pass.

### Check Airflow DAGs
1. Go to http://localhost:8080
2. Enable the DAGs:
   - data_ingestion
   - dbt_transformation
   - data_quality_checks
3. Trigger a manual run

## Troubleshooting

### Connection Issues

**Databricks**: Verify your access token is valid
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://YOUR_WORKSPACE.cloud.databricks.com/api/2.0/clusters/list
```

**Snowflake**: Test connection
```python
import snowflake.connector
conn = snowflake.connector.connect(
    user='YOUR_USER',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT'
)
print("Connected!")
```

**BigQuery**: Verify credentials
```bash
gcloud auth application-default login
bq ls
```

### dbt Issues

**Profile not found**: Make sure `~/.dbt/profiles.yml` exists and is properly configured

**Compilation errors**: Run `dbt debug` to check configuration

**Test failures**: Review test results with `dbt test --store-failures`

### Airflow Issues

**DAGs not showing**: Check `$AIRFLOW_HOME/dags/` contains the DAG files

**Import errors**: Ensure all dependencies are installed in the Airflow environment

**Task failures**: Check logs in Airflow UI or `$AIRFLOW_HOME/logs/`

## Next Steps

1. Explore the dbt documentation at http://localhost:8080 (after running `dbt docs serve`)
2. Connect Tableau to your data warehouse and use the metrics views
3. Customize the data generators to match your specific use case
4. Add more dbt models and tests as needed
5. Set up alerting and monitoring for production

## Support

For issues or questions:
1. Check the README.md in each directory
2. Review the code comments
3. Consult the official documentation:
   - [dbt docs](https://docs.getdbt.com/)
   - [Airflow docs](https://airflow.apache.org/docs/)
   - [Databricks docs](https://docs.databricks.com/)
   - [Snowflake docs](https://docs.snowflake.com/)
   - [BigQuery docs](https://cloud.google.com/bigquery/docs)
