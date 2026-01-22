"""
Airflow DAG: Data Quality Checks

Comprehensive data quality monitoring and alerting.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default arguments
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'data_quality_checks',
    default_args=default_args,
    description='Monitor data quality across all layers',
    schedule_interval='0 4 * * *',  # Daily at 4 AM (after transformations)
    start_date=days_ago(1),
    catchup=False,
    tags=['quality', 'monitoring'],
)

# Task: Check data completeness
def check_data_completeness(**context):
    """Verify all expected tables have data."""
    print("Checking data completeness...")
    
    # Example checks (would query actual warehouse in production)
    tables_to_check = [
        'products', 'customers', 'orders', 'order_lines',
        'shipments', 'returns', 'waste', 'quality_inspections'
    ]
    
    results = {}
    for table in tables_to_check:
        # In production: SELECT COUNT(*) FROM {table}
        results[table] = {
            'row_count': 1000,  # Mock data
            'status': 'OK'
        }
    
    print(f"Completeness check results: {results}")
    return results

completeness_check = PythonOperator(
    task_id='check_data_completeness',
    python_callable=check_data_completeness,
    dag=dag,
)

# Task: Check data freshness
def check_data_freshness(**context):
    """Verify data is up-to-date."""
    print("Checking data freshness...")
    
    # Example: Check if orders table has data from last 24 hours
    # In production: SELECT MAX(order_date) FROM orders
    
    from datetime import datetime, timedelta
    last_order_date = datetime.now() - timedelta(hours=12)
    threshold = datetime.now() - timedelta(hours=24)
    
    is_fresh = last_order_date > threshold
    
    if not is_fresh:
        raise ValueError(f"Data is stale! Last order: {last_order_date}")
    
    print(f"Data is fresh. Last order: {last_order_date}")
    return is_fresh

freshness_check = PythonOperator(
    task_id='check_data_freshness',
    python_callable=check_data_freshness,
    dag=dag,
)

# Task: Check data accuracy
def check_data_accuracy(**context):
    """Verify data accuracy and consistency."""
    print("Checking data accuracy...")
    
    checks = {
        'revenue_reconciliation': {
            'check': 'SUM(order_lines.line_total) = orders.subtotal',
            'status': 'PASS'
        },
        'inventory_consistency': {
            'check': 'All product_ids in orders exist in products',
            'status': 'PASS'
        },
        'customer_orders': {
            'check': 'All customer_ids in orders exist in customers',
            'status': 'PASS'
        }
    }
    
    print(f"Accuracy check results: {checks}")
    return checks

accuracy_check = PythonOperator(
    task_id='check_data_accuracy',
    python_callable=check_data_accuracy,
    dag=dag,
)

# Task: Check for anomalies
def check_for_anomalies(**context):
    """Detect statistical anomalies in data."""
    print("Checking for anomalies...")
    
    anomalies = []
    
    # Example checks
    checks = {
        'order_volume': {'value': 100, 'mean': 95, 'std': 10, 'threshold': 3},
        'avg_order_value': {'value': 150, 'mean': 145, 'std': 15, 'threshold': 3},
        'return_rate': {'value': 5.2, 'mean': 5.0, 'std': 0.5, 'threshold': 3},
    }
    
    for metric, data in checks.items():
        z_score = abs((data['value'] - data['mean']) / data['std'])
        if z_score > data['threshold']:
            anomalies.append({
                'metric': metric,
                'value': data['value'],
                'z_score': z_score
            })
    
    if anomalies:
        print(f"Anomalies detected: {anomalies}")
        # Would trigger alert in production
    else:
        print("No anomalies detected")
    
    return anomalies

anomaly_check = PythonOperator(
    task_id='check_for_anomalies',
    python_callable=check_for_anomalies,
    dag=dag,
)

# Task: Generate quality report
def generate_quality_report(**context):
    """Generate comprehensive data quality report."""
    print("Generating data quality report...")
    
    # Pull results from previous tasks
    ti = context['ti']
    completeness = ti.xcom_pull(task_ids='check_data_completeness')
    accuracy = ti.xcom_pull(task_ids='check_data_accuracy')
    anomalies = ti.xcom_pull(task_ids='check_for_anomalies')
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'completeness': completeness,
        'accuracy': accuracy,
        'anomalies': anomalies,
        'overall_status': 'PASS' if not anomalies else 'WARNING'
    }
    
    print(f"Quality Report: {report}")
    
    # In production: Save to file, send to monitoring system, etc.
    return report

quality_report = PythonOperator(
    task_id='generate_quality_report',
    python_callable=generate_quality_report,
    dag=dag,
)

# Task: Run dbt tests
dbt_test_all = BashOperator(
    task_id='run_dbt_tests',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt test',
    dag=dag,
)

# Define task dependencies
[completeness_check, freshness_check, accuracy_check, anomaly_check] >> quality_report
quality_report >> dbt_test_all
