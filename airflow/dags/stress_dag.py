from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'ml_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

def check_data():
    import pandas as pd
    import os
    data_path = '/opt/airflow/data/stress_data.csv'
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        print(f"Data OK: {len(df)} rows")
        return f"Data OK: {len(df)} rows"
    else:
        print("No data file")
        return "No data file"

with DAG(
    'stress_prediction_pipeline',
    default_args=default_args,
    description='ML pipeline for stress prediction',
    schedule_interval='@daily',
    catchup=False,
    tags=['ml', 'stress'],
) as dag:

    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='python3 /opt/airflow/scripts/data_generator.py',
    )
    
    check_data_task = PythonOperator(
        task_id='check_data',
        python_callable=check_data,
    )
    
    train_model = BashOperator(
        task_id='train_model',
        bash_command='python3 /opt/airflow/scripts/train_model.py',
    )
    
    generate_data >> check_data_task >> train_model

