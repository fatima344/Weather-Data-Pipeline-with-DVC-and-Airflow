import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='A DAG for collecting and processing weather data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Use the mounted path from the docker-compose file
# This is the path inside the container where your project is mounted
project_path = '/opt/project'

# Define tasks using BashOperator
fetch_task = BashOperator(
    task_id='fetch_weather_data',
    bash_command=f'cd {project_path} && python src/fetch_weather.py',
    dag=dag,
)

preprocess_task = BashOperator(
    task_id='preprocess_data',
    bash_command=f'cd {project_path} && python src/preprocess_data.py',
    dag=dag,
)

train_task = BashOperator(
    task_id='train_model',
    bash_command=f'cd {project_path} && python src/train_model.py',
    dag=dag,
)

evaluate_task = BashOperator(
    task_id='evaluate_model',
    bash_command=f'cd {project_path} && python src/generate_metrics.py',
    dag=dag,
)

dvc_version_task = BashOperator(
    task_id='version_with_dvc',
    bash_command=f'''
    cd {project_path} &&
    dvc repro &&
    git add data/*.dvc models/*.dvc metrics.json .gitignore &&
    git commit -m "Update data and model via Airflow" || echo "No changes to commit" &&
    dvc push || echo "DVC push failed, check authentication"
    ''',
    dag=dag,
)

# Define task dependencies
fetch_task >> preprocess_task >> train_task >> evaluate_task >> dvc_version_task