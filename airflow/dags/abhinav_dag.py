from airflow import DAG
from airflow.operators.empty import EmptyOperator  # Updated from DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define the default_args dictionary
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    'abhinav_dag',  # Updated DAG name
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule='@daily',  # Updated from schedule_interval
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Define a simple function to print the current date
    def print_date():
        print(f"Current date: {datetime.now()}")

    # Define tasks
    start = EmptyOperator(
        task_id='start',
    )

    print_date_task = PythonOperator(
        task_id='print_date',
        python_callable=print_date,
    )

    end = EmptyOperator(
        task_id='end',
    )

    # Define the task dependencies
    start >> print_date_task >> end

# Print a confirmation message to indicate successful loading of the DAG
print("DAG loaded successfully")
