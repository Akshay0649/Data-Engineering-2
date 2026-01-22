"""
Airflow DAG: Data Ingestion

Orchestrates the ingestion of raw data from CSV files into the data warehouse.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default arguments
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'data_ingestion',
    default_args=default_args,
    description='Ingest raw data into data warehouse',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=days_ago(1),
    catchup=False,
    tags=['ingestion', 'raw_data'],
)

# Task: Generate sample data
generate_data = BashOperator(
    task_id='generate_sample_data',
    bash_command='cd {{ var.value.project_root }}/data_generators && python generate_all.py',
    dag=dag,
)

# Task: Validate data files
def validate_data_files(**context):
    """Validate that all required CSV files exist."""
    import os
    
    data_path = '{{ var.value.project_root }}/sample_data'
    required_files = [
        'products.csv',
        'recipes.csv',
        'recipe_lines.csv',
        'customers.csv',
        'orders.csv',
        'order_lines.csv',
        'shipments.csv',
        'returns.csv',
        'waste.csv',
        'quality_inspections.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(data_path, file)):
            missing_files.append(file)
    
    if missing_files:
        raise FileNotFoundError(f"Missing data files: {missing_files}")
    
    print(f"All {len(required_files)} data files validated successfully!")

validate_files = PythonOperator(
    task_id='validate_data_files',
    python_callable=validate_data_files,
    dag=dag,
)

# Task: Ingest to data warehouse
# Note: This uses a bash command, but you can also use specific operators
# like DatabricksSubmitRunOperator, SnowflakeOperator, or BigQueryOperator
ingest_data = BashOperator(
    task_id='ingest_to_warehouse',
    bash_command='''
        cd {{ var.value.project_root }}/ingestion && \
        python ingest_to_{{ var.value.platform }}.py {{ var.value.config_path }}
    ''',
    dag=dag,
)

# Task: Data quality checks
def run_data_quality_checks(**context):
    """Run basic data quality checks on ingested data."""
    print("Running data quality checks...")
    
    # Example checks (would be more comprehensive in production)
    checks = {
        'products': 'SELECT COUNT(*) FROM products WHERE product_id IS NULL',
        'customers': 'SELECT COUNT(*) FROM customers WHERE customer_id IS NULL',
        'orders': 'SELECT COUNT(*) FROM orders WHERE order_id IS NULL',
    }
    
    # In production, you would connect to your warehouse and run these checks
    print("Data quality checks completed successfully!")

quality_checks = PythonOperator(
    task_id='run_quality_checks',
    python_callable=run_data_quality_checks,
    dag=dag,
)

# Task: Send success notification
def send_success_notification(**context):
    """Send notification on successful ingestion."""
    execution_date = context['execution_date']
    print(f"Data ingestion completed successfully for {execution_date}")
    # In production, you might send an email, Slack message, etc.

success_notification = PythonOperator(
    task_id='send_success_notification',
    python_callable=send_success_notification,
    dag=dag,
)

# Define task dependencies
generate_data >> validate_files >> ingest_data >> quality_checks >> success_notification
