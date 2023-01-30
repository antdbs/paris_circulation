import os
from os.path import dirname, abspath
from dotenv import load_dotenv

path = dirname(abspath(__file__)) + '/.env'
load_dotenv(path)

dataset_metadata = {
    "datasets" : {
        "paris_arrondissement": {
            "url": "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/arrondissements/exports/json?lang=fr&timezone=Europe%2FBerlin"
        },
        "traffic_lights": {
            "url": "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/signalisation-tricolore/exports/json?lang=fr&timezone=Europe%2FBerlin"

        }
        # ,
        # "traffic_flow": {
        #     # "url": "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptages-routiers-permanents/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&csv_separator=%3B"
        #     "url": "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptages-routiers-permanents/exports/json?lang=fr&timezone=Europe%2FBerlin"
        # }
    }
}

web_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}

postgresql_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_database_name = os.getenv('POSTGRES_DB')
database_dialect = os.getenv('BDD_DIALECT')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')


DB_URI = f"postgresql://{postgresql_user}:{postgres_password}@{database_host}:{database_port}/{postgres_database_name}"