import json
import requests
from config import *
from sqlalchemy import create_engine

from models.table import Table

engine = create_engine(DB_URI)

def get_data_from_web(url, limit_size=None):

    if limit_size is not None:
        url = f"{url}&limit={limit_size}"

    request_result = requests.get(url, headers=web_header, stream = True)

    return request_result.json()

def create_dataset_folder(name):
    if not os.path.exists(f"./tmp/{name}"):
        os.makedirs(f"./tmp/{name}")

def save_sample_into_a_file(data):  
    with open(f"./tmp/{name}/{name}.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def bulk_file_to_postgresql_database(name, schema, List_of_dict):

    table = Table(name, schema, engine)

    with engine.connect() as connection:
        connection.execute(f"DROP TABLE {schema}.{name};")

    if table.is_exist() == False:
        try: 
            table.create(List_of_dict[0])
            print(f"[✅] : table {name} created")
            try:
                for element in List_of_dict:
                    insert_query = table.build_insert_query(element)

                    with engine.connect() as connection:
                        connection.execute(insert_query)
                    
                print(f"[✅] : data insert into {name} table")
            except:
                pass
        except Exception as ex:
            print(f"[❌] : can't create table cause to : {ex}")

    else:
        print(f"[ ❕] : Table {name} already exist")

if __name__ == '__main__':
    
    for name in dataset_metadata["datasets"]:
        url = dataset_metadata["datasets"][name]["url"]
        create_dataset_folder(name)
        web_data = get_data_from_web(url) 
        bulk_file_to_postgresql_database(name, "datalake", web_data)

    pass 