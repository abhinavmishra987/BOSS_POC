from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator  # Updated from DummyOperator
from datetime import datetime
import os

# Define the default_args dictionary
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the functions
def find_directories(**context):
    directories = []
    for root, dirs, files in os.walk('/'):
        for directory in dirs:
            directories.append(os.path.join(root, directory))
    context['ti'].xcom_push(key='directories', value=directories)

def print_directory_names(**context):
    directories = context['ti'].xcom_pull(key='directories', task_ids='find_directories')
    for directory in directories:
        print(directory)

def success_message():
    print("Successfully completed all tasks!")

# Define the DAG
with DAG(
    'filesystem_dag',
    default_args=default_args,
    description='A DAG to find directories, print their names, and give a success message',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Define tasks
    start = EmptyOperator(
        task_id='start',
    )

    find_directories_task = PythonOperator(
        task_id='find_directories',
        python_callable=find_directories,
        provide_context=True,
    )

    print_directory_names_task = PythonOperator(
        task_id='print_directory_names',
        python_callable=print_directory_names,
        provide_context=True,
    )

    success_message_task = PythonOperator(
        task_id='success_message',
        python_callable=success_message,
    )

    end = EmptyOperator(
        task_id='end',
    )

    # Define the task dependencies
    start >> find_directories_task >> print_directory_names_task >> success_message_task >> end

# Print a confirmation message to indicate successful loading of the DAG
print("DAG loaded successfully")
