import os
from os.path import dirname, abspath
from dotenv import load_dotenv

path = dirname(abspath(__file__)) + '/.env'
load_dotenv(path)

postgresql_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_database_name = os.getenv('POSTGRES_DB')
database_dialect = os.getenv('BDD_DIALECT')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')


DB_URI = f"postgresql://{postgresql_user}:{postgres_password}@{database_host}:{database_port}/{postgres_database_name}"