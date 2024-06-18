from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime, timedelta
import os
import glob

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
dag = DAG(
    'file_sensor_dag',
    default_args=default_args,
    description='A simple DAG that processes all .txt files when they appear in a directory',
    schedule_interval=None,
    start_date=datetime(2023, 6, 18),
    catchup=False,
)

# Define the directory to watch
WATCH_DIRECTORY = '/home/e0002/airflow/watch_dir'

# Define the function to process the file
def process_file(**kwargs):
    # List all .txt files in the directory
    files = glob.glob(os.path.join(WATCH_DIRECTORY, '*.txt'))
    
    for file_path in files:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Processing file: {file_path}")
            print(content)
        # Optionally, remove or move the file after processing
        # os.remove(file_path)  # Uncomment to delete the file after processing

# Define the FileSensor task
file_sensor_task = FileSensor(
    task_id='file_sensor_task',
    poke_interval=10,  # Check every 10 seconds
    timeout=600,  # Timeout after 10 minutes
    mode='poke',
    fs_conn_id='fs_default',  # Default filesystem connection
    filepath=os.path.join(WATCH_DIRECTORY, '*.txt'),
    dag=dag,
)

# Define the TriggerDagRunOperator task to trigger another DAG
trigger_another_dag_task = TriggerDagRunOperator(
    task_id='trigger_another_dag',
    trigger_dag_id='another_dag',  # Replace with your target DAG ID
    conf={
        "files": "{{ task_instance.xcom_pull(task_ids='check_files_task', key='file_list') }}"
    },
    dag=dag,
)

# Define the PythonOperator task to process the file
process_file_task = PythonOperator(
    task_id='process_file_task',
    python_callable=process_file,
    provide_context=True,
    dag=dag,
)

# Set the task dependencies
file_sensor_task >> process_file_task
