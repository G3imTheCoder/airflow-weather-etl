from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def test_hello():
    print("🚀 Bonjour depuis Airflow ! Le système fonctionne parfaitement.")
    return "Test OK"

with DAG(
    dag_id='1_mon_premier_dag_test', 
    start_date=datetime(2024, 1, 1), 
    schedule_interval='@daily',      
    catchup=False                   
) as dag:

   
    tache_1 = PythonOperator(
        task_id='dire_bonjour',
        python_callable=test_hello
    )

