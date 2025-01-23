from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'nyc_taxi_pipeline',
    default_args=default_args,
    description='ETL pipeline for NYC Taxi data',
    schedule_interval='@daily',  # Adjust based on how often you want it to run
    catchup=False,
) as dag:
    
        # Task 1: Extract data
        # Task 1: Extract data
    extract_task = BashOperator(
        task_id='extract_data',
        bash_command='cd /opt/airflow/extract-pipeline && python grab_taxi_data.py'
    )

    # Task 2: Load data into PostgreSQL
    load_postgres_task = BashOperator(
        task_id='load_to_postgres',
        bash_command='cd /opt/airflow/staging-pipeline && python load_to_postgres.py'
    )

    # Task 3: Clean and transform data
    clean_task = BashOperator(
        task_id='clean_data',
        bash_command='cd /opt/airflow/staging-pipeline && python data_cleanup.py'
    )

    # Task 4: Upload cleaned data to GCS
    upload_gcs_task = BashOperator(
        task_id='upload_to_gcs',
        bash_command='cd /opt/airflow/gcs-pipeline && python load_to_gcs.py'
    )

    # Task 5: Load data into BigQuery
    load_bigquery_task = BashOperator(
        task_id='load_to_bigquery',
        bash_command='cd /opt/airflow/bigquery-pipeline && python load_to_bigquery.py'
    )


    # Define task dependencies
    extract_task >> load_postgres_task >> clean_task >> upload_gcs_task >> load_bigquery_task
