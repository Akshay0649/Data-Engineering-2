# Airflow DAGs

Apache Airflow DAGs for orchestrating the Physical Product Platform data pipeline.

## Overview

This directory contains Airflow DAGs that orchestrate the end-to-end data pipeline:
1. Data ingestion from CSV to data warehouse
2. dbt transformations to create analytics marts
3. Data quality checks and monitoring

## DAGs

### 1. `dag_ingestion.py`
**Purpose:** Ingest raw data into the data warehouse

**Schedule:** Daily at 2:00 AM

**Tasks:**
1. `generate_sample_data` - Generate fresh sample data
2. `validate_data_files` - Verify all CSV files exist
3. `ingest_to_warehouse` - Load data into warehouse
4. `run_quality_checks` - Basic validation checks
5. `send_success_notification` - Alert on completion

**Dependencies:** None

**Variables Required:**
- `project_root` - Path to project directory
- `platform` - databricks, snowflake, or bigquery
- `config_path` - Path to ingestion config

### 2. `dag_dbt_transform.py`
**Purpose:** Transform raw data into analytics marts using dbt

**Schedule:** Daily at 3:00 AM (after ingestion)

**Tasks:**
1. `dbt_deps` - Install dbt packages
2. `dbt_debug` - Verify connection
3. `dbt_source_freshness` - Check data freshness
4. `dbt_run_staging` - Run staging models
5. `dbt_test_staging` - Test staging models
6. `dbt_run_marts_core` - Run core mart models
7. `dbt_test_marts_core` - Test core marts
8. `dbt_run_metrics` - Run metrics views
9. `dbt_test_metrics` - Test metrics
10. `dbt_docs_generate` - Generate documentation

**Dependencies:** `dag_ingestion` should complete first

**Variables Required:**
- `project_root` - Path to project directory

### 3. `dag_quality_checks.py`
**Purpose:** Monitor data quality across all layers

**Schedule:** Daily at 4:00 AM (after transformations)

**Tasks:**
1. `check_data_completeness` - Verify table row counts
2. `check_data_freshness` - Verify data is recent
3. `check_data_accuracy` - Validate calculations
4. `check_for_anomalies` - Detect statistical outliers
5. `generate_quality_report` - Compile results
6. `run_dbt_tests` - Execute all dbt tests

**Dependencies:** `dag_dbt_transform` should complete first

**Variables Required:**
- `project_root` - Path to project directory

## Setup

### 1. Install Airflow

```bash
pip install apache-airflow==2.10.4
export AIRFLOW_HOME=~/airflow
airflow db init
```

### 2. Create Admin User

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

### 3. Configure Variables

Set required Airflow variables via CLI or UI:

```bash
# Via CLI
airflow variables set project_root /path/to/Data-Engineering-2
airflow variables set platform databricks
airflow variables set config_path ingestion/config.yaml

# Or import from YAML
airflow variables import config/airflow_variables.yaml
```

### 4. Copy DAGs

```bash
cp -r dags/* $AIRFLOW_HOME/dags/
```

### 5. Start Airflow

```bash
# Terminal 1: Web server
airflow webserver --port 8080

# Terminal 2: Scheduler
airflow scheduler
```

Access UI at http://localhost:8080

## Customization

### Changing Schedule

Edit the `schedule_interval` in each DAG:

```python
dag = DAG(
    'dag_name',
    schedule_interval='0 2 * * *',  # Cron expression
    # or
    schedule_interval='@daily',     # Preset
    ...
)
```

Common schedules:
- `@once` - Run once
- `@hourly` - Every hour
- `@daily` - Once per day
- `@weekly` - Once per week
- `0 */4 * * *` - Every 4 hours
- `0 2 * * 1-5` - 2 AM on weekdays

### Adding Email Alerts

Update `default_args` in each DAG:

```python
default_args = {
    'email': ['your-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'email_on_success': False,  # Usually not needed
}
```

Configure SMTP in `airflow.cfg`:
```ini
[smtp]
smtp_host = smtp.gmail.com
smtp_starttls = True
smtp_ssl = False
smtp_user = your-email@gmail.com
smtp_password = your-app-password
smtp_port = 587
smtp_mail_from = your-email@gmail.com
```

### Adding Slack Notifications

Install the provider:
```bash
pip install apache-airflow-providers-slack
```

Add to DAG:
```python
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

slack_alert = SlackWebhookOperator(
    task_id='slack_notification',
    http_conn_id='slack_webhook',
    message='Data pipeline completed successfully!',
    dag=dag,
)
```

## Using Platform-Specific Operators

### Databricks Operator

```python
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator

databricks_task = DatabricksSubmitRunOperator(
    task_id='run_databricks_job',
    databricks_conn_id='databricks_default',
    new_cluster={
        'spark_version': '11.3.x-scala2.12',
        'node_type_id': 'i3.xlarge',
        'num_workers': 2
    },
    notebook_task={
        'notebook_path': '/path/to/notebook',
    },
    dag=dag,
)
```

### Snowflake Operator

```python
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

snowflake_task = SnowflakeOperator(
    task_id='run_snowflake_query',
    snowflake_conn_id='snowflake_default',
    sql='SELECT COUNT(*) FROM products;',
    warehouse='COMPUTE_WH',
    database='PHYSICAL_PRODUCT_DB',
    schema='RAW',
    dag=dag,
)
```

### BigQuery Operator

```python
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

bigquery_task = BigQueryInsertJobOperator(
    task_id='run_bigquery_query',
    configuration={
        'query': {
            'query': 'SELECT COUNT(*) FROM `project.dataset.products`',
            'useLegacySql': False,
        }
    },
    gcp_conn_id='google_cloud_default',
    dag=dag,
)
```

## Monitoring

### Check DAG Status

```bash
# List all DAGs
airflow dags list

# Check DAG status
airflow dags state dag_ingestion

# List tasks for a DAG
airflow tasks list dag_ingestion

# Test a task
airflow tasks test dag_ingestion generate_sample_data 2024-01-01
```

### View Logs

```bash
# View logs for a task
airflow tasks logs dag_ingestion generate_sample_data 2024-01-01

# Or in UI: DAGs → Select DAG → Graph View → Click Task → Logs
```

### Trigger Manual Run

```bash
# Via CLI
airflow dags trigger dag_ingestion

# Or in UI: DAGs → Toggle to ON → Click "Trigger DAG"
```

## Best Practices

1. **Idempotency**: Ensure tasks can be safely re-run
2. **Dependencies**: Use `depends_on_past=True` for data pipelines
3. **Retries**: Configure appropriate retry logic
4. **Timeouts**: Set execution timeouts to prevent hanging tasks
5. **Testing**: Use `airflow tasks test` before deploying
6. **Monitoring**: Set up alerts for failures
7. **Documentation**: Add docstrings to tasks and DAGs
8. **Version Control**: Track DAG changes in Git

## Troubleshooting

### DAG Not Appearing

- Check for syntax errors: `python dags/dag_name.py`
- Refresh DAG list in UI
- Check `$AIRFLOW_HOME/dags/` directory
- Review scheduler logs

### Task Failures

- Check task logs in UI
- Verify connections are configured
- Test task in isolation: `airflow tasks test`
- Check resource availability (disk, memory, CPU)

### Performance Issues

- Increase worker parallelism in `airflow.cfg`
- Use appropriate executor (LocalExecutor, CeleryExecutor)
- Optimize task concurrency
- Monitor resource usage

## Production Deployment

### Using Docker

```dockerfile
FROM apache/airflow:2.7.0

# Copy DAGs
COPY dags/ /opt/airflow/dags/

# Copy config
COPY config/ /opt/airflow/config/

# Install additional packages
RUN pip install -r requirements.txt
```

### Using Kubernetes

- Deploy with Helm: `helm install airflow apache-airflow/airflow`
- Use KubernetesExecutor for scalability
- Configure persistent volumes for logs
- Set up monitoring with Prometheus/Grafana

## Resources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [dbt + Airflow Guide](https://docs.getdbt.com/docs/running-a-dbt-project/running-dbt-in-production)
