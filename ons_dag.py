from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from api_extraction import extract_field

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag1 = DAG(
    'ONS_API_Extraction', 
    default_args=default_args,
    description = "first Airflow project"
    
)

task_1 = PythonOperator(
    task_id='data extraction from api',
    python_callable = extract_field,
    dag=dag1,
)

task_1