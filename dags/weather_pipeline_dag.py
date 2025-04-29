# dags/weather_pipeline_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.fetch_weather import fetch_and_save
from src.preprocess_data import preprocess_and_save
# Optional: from src.train_model import train_and_save

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1
}

with DAG(dag_id='weather_data_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    collect_task = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_and_save
    )
    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_and_save
    )
    # You could also add a training task:
    # train_task = PythonOperator(
    #     task_id='train_model',
    #     python_callable=train_and_save
    # )

    collect_task >> preprocess_task
    # preprocess_task >> train_task
