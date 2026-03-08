from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests

def extract_weather_data():
    api_key = "Ton_API_KEY_OPENWEATHERMAP"
    villes = ["Paris", "Tokyo", "New York", "London", "Sydney"]
    
    toutes_les_donnees = [] 
    
    for city in villes:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr"
        print(f"📡 Connexion à l'API pour {city}...")
        response = requests.get(url)
        
        if response.status_code == 200:
            toutes_les_donnees.append(response.json()) 
        else:
            print(f"❌ Erreur API pour {city} : {response.status_code}")
            
    return toutes_les_donnees 

def transform_weather_data(ti):
    raw_data_list = ti.xcom_pull(task_ids='extraire_donnees_meteo')
    clean_data_list = []
    
    for raw_data in raw_data_list:
        clean_data = {
            "ville": raw_data["name"],
            "temperature": raw_data["main"]["temp"],
            "humidite": raw_data["main"]["humidity"],
            "meteo": raw_data["weather"][0]["description"],
            "heure_collecte": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        clean_data_list.append(clean_data)
        
    return clean_data_list

def load_weather_data(ti):
    clean_data_list = ti.xcom_pull(task_ids='transformer_donnees_meteo')
    hook = PostgresHook(postgres_conn_id='connexion_postgres_meteo')
    
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS meteo_villes (
        id SERIAL PRIMARY KEY,
        ville VARCHAR(50),
        temperature FLOAT,
        humidite INT,
        meteo VARCHAR(100),
        heure_collecte TIMESTAMP
    );
    """
    hook.run(sql_create_table)
    
    sql_insert = """
    INSERT INTO meteo_villes (ville, temperature, humidite, meteo, heure_collecte)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    for data in clean_data_list:
        hook.run(sql_insert, parameters=(
            data['ville'], data['temperature'], data['humidite'], data['meteo'], data['heure_collecte']
        ))
        print(f"💾 SUCCÈS : {data['ville']} sauvegardée ({data['temperature']}°C)")


with DAG(
    dag_id='3_pipeline_tour_du_monde', 
    start_date=datetime(2024, 1, 1),
    schedule_interval='@hourly', 
    catchup=False
) as dag:

    task_extract = PythonOperator(task_id='extraire_donnees_meteo', python_callable=extract_weather_data)
    task_transform = PythonOperator(task_id='transformer_donnees_meteo', python_callable=transform_weather_data)
    task_load = PythonOperator(task_id='charger_donnees_meteo', python_callable=load_weather_data)

    task_extract >> task_transform >> task_load