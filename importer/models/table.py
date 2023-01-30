from sqlalchemy import create_engine


class Table():
    def __init__(self, name: str, schema: str, engine) -> None:
        self.name = name
        self.schema = schema
        self.engine = engine
        pass

    def is_exist(self):
        query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE  table_schema = '{self.schema}'
                AND    table_name   = '{self.name}'
            );
            
        """

        with self.engine.connect() as connection:
            result = connection.execute(query)

        return result.fetchone()[0]

    def create(self, data_dict):

        list_of_keys_string = ""
        for key, value in data_dict.items():
            if isinstance(value, str) or value is None:
                list_of_keys_string += f"{key} text,"
            elif isinstance(value, dict):
                list_of_keys_string += f"{key} json,"
            else:
                list_of_keys_string += f"{key} double precision,"

        list_of_keys_string = list_of_keys_string[:-1]

        query = f"""
            CREATE TABLE {self.schema}.{self.name}
                (
                    {list_of_keys_string}
                ) 
        """

        with self.engine.connect() as connection:
            connection.execute(query)

    def build_insert_query(self, element):
        list_of_keys_string = ""
        list_of_values_string = ""

        for key, value in element.items():
            list_of_keys_string += f"{key},"
            
            if not value:
                list_of_values_string += "Null,"
            else:
                if isinstance(value, str):
                    value = str(value).replace("'","`")
                if isinstance(value, dict):
                    value = str(value).replace("'",'"')
                    pass
                list_of_values_string += f"'{value}',"

        list_of_keys_string = list_of_keys_string[:-1]
        list_of_values_string = list_of_values_string[:-1]

        query = f"""
            INSERT INTO {self.schema}.{self.name}({list_of_keys_string})
            VALUES ({list_of_values_string})
            
        """

        # print(query)

        return query