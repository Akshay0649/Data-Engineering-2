"""
Airflow DAG: dbt Transformation

Orchestrates dbt models to transform raw data into analytics-ready marts.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default arguments
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': True,  # Ensure previous runs completed
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'dbt_transformation',
    default_args=default_args,
    description='Run dbt transformations to create analytics marts',
    schedule_interval='0 3 * * *',  # Daily at 3 AM (after ingestion)
    start_date=days_ago(1),
    catchup=False,
    tags=['dbt', 'transformation', 'marts'],
)

# Task: Install dbt dependencies
dbt_deps = BashOperator(
    task_id='dbt_deps',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt deps',
    dag=dag,
)

# Task: Run dbt debug to verify connection
dbt_debug = BashOperator(
    task_id='dbt_debug',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt debug',
    dag=dag,
)

# Task: Run staging models
dbt_run_staging = BashOperator(
    task_id='dbt_run_staging',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt run --models staging',
    dag=dag,
)

# Task: Test staging models
dbt_test_staging = BashOperator(
    task_id='dbt_test_staging',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt test --models staging',
    dag=dag,
)

# Task: Run core mart models (dimensions and facts)
dbt_run_marts_core = BashOperator(
    task_id='dbt_run_marts_core',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt run --models marts.core',
    dag=dag,
)

# Task: Test core mart models
dbt_test_marts_core = BashOperator(
    task_id='dbt_test_marts_core',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt test --models marts.core',
    dag=dag,
)

# Task: Run metrics models
dbt_run_metrics = BashOperator(
    task_id='dbt_run_metrics',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt run --models marts.metrics',
    dag=dag,
)

# Task: Test metrics models
dbt_test_metrics = BashOperator(
    task_id='dbt_test_metrics',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt test --models marts.metrics',
    dag=dag,
)

# Task: Generate dbt documentation
dbt_docs_generate = BashOperator(
    task_id='dbt_docs_generate',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt docs generate',
    dag=dag,
)

# Task: Run source freshness checks
dbt_source_freshness = BashOperator(
    task_id='dbt_source_freshness',
    bash_command='cd {{ var.value.project_root }}/dbt_project && dbt source freshness',
    dag=dag,
)

# Task: Snapshot models (if any SCD Type 2 dimensions)
# dbt_snapshot = BashOperator(
#     task_id='dbt_snapshot',
#     bash_command='cd {{ var.value.project_root }}/dbt_project && dbt snapshot',
#     dag=dag,
# )

# Define task dependencies
dbt_deps >> dbt_debug >> dbt_source_freshness
dbt_source_freshness >> dbt_run_staging >> dbt_test_staging
dbt_test_staging >> dbt_run_marts_core >> dbt_test_marts_core
dbt_test_marts_core >> dbt_run_metrics >> dbt_test_metrics
dbt_test_metrics >> dbt_docs_generate
