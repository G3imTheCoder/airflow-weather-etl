# 🌤️ Automated Weather ETL Pipeline

Ce projet est un pipeline de données complet (ETL) conçu pour extraire, transformer et charger des données météorologiques en temps réel depuis l'API OpenWeatherMap vers une base de données PostgreSQL, avec une visualisation sur Metabase. L'infrastructure complète est conteneurisée avec Docker.

## 🛠️ Stack Technique
* **Orchestration :** Apache Airflow
* **Base de données :** PostgreSQL
* **Visualisation :** Metabase
* **Langage :** Python (requests, Pandas)
* **Infrastructure :** Docker & Docker Compose
* **Source de données :** OpenWeatherMap API

## ⚙️ Architecture du Pipeline (ETL)
Le DAG Airflow s'exécute automatiquement (`@hourly`) et suit ces 3 étapes :
1. **Extract :** Appel à l'API OpenWeatherMap pour récupérer les données brutes de 5 villes mondiales (Paris, Tokyo, New York, Londres, Sydney).
2. **Transform :** Nettoyage des données JSON pour extraire la température, l'humidité et la description météo, et ajout d'un horodatage.
3. **Load :** Insertion des données propres dans une table `meteo_villes` sur PostgreSQL via un `PostgresHook`.

## 🚀 Comment lancer le projet en local

1. Cloner le dépôt : `git clone https://github.com/TonPseudo/airflow-weather-etl.git`
2. Lancer les conteneurs : `docker compose up -d`
3. Accéder aux interfaces :
   * **Airflow :** `http://localhost:8080` (Identifiants : airflow / airflow)
   * **Metabase :** `http://localhost:3000`
4. Configurer la connexion PostgreSQL dans Airflow (`connexion_postgres_meteo`).
5. Lancer le DAG `3_pipeline_tour_du_monde`.
