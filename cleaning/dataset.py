import pandas as pd
from shapely.geometry import shape
from sqlalchemy import create_engine
from config import *

from config import *

engine = create_engine(DB_URI)
class CleanDataset:

    def __init__(self, engine) -> None:
        self.engine = engine
        pass

    def metric_kpi(self):

        with self.engine.connect() as connection: 

            # Get traffic light data
            traffic_ligths = pd.read_sql(
                sql="""
                        SELECT lib_region, count(*) as count_tl
                        FROM datalake.traffic_lights
                        WHERE lib_region not in ('PERIPHERIQUE')
                        GROUP BY lib_region;
                    """,
                con=connection
            )

            # Get arrondissment data
            paris_arr = pd.read_sql(
                sql="""
                        SELECT c_arinsee, surface, geom
                        FROM datalake.paris_arrondissement;
                    """,
                con=connection
            )

        traffic_ligths["code_arr"] = traffic_ligths["lib_region"].apply(lambda x: int("750"+x.split(" ")[1]))
        traffic_ligths["lib_region"] = traffic_ligths["lib_region"].apply(lambda x: x.replace(" ", " n°"))

        paris_arr["c_arinsee"] = paris_arr["c_arinsee"].apply(lambda x: int(x)-100)
        paris_arr["bbox"] = paris_arr["geom"].apply(lambda x: str(shape(x["geometry"]).bounds)[1:-1])

        del paris_arr['geom']

        paris_arr = paris_arr.rename(columns={'c_arinsee': 'code_arr'})

        density_table = pd.merge(traffic_ligths, paris_arr, on='code_arr')

        density_table["density_m_sqrt"] = density_table["count_tl"] / density_table["surface"]
        density_table["density_ha"] = density_table["count_tl"] / density_table["surface"] * 1000
        density_table = density_table.sort_values(by=['code_arr'])

        density_table.to_sql('density', con=engine, schema="datawarehouse", if_exists='replace')

        print(f"[✅] : table density is up-to-date")
        

    def map_kpi(self):

        with self.engine.connect() as connection: 

            # Get arrondissment data
            paris_arr = pd.read_sql(
                sql="""
                        SELECT 
                            c_arinsee as code_arr, 
                            l_aroff as official_name, 
                            surface, 
                            perimetre
                        FROM datalake.paris_arrondissement;
                    """,
                con=connection
            )

            # Get traffic light data
            traffic_ligths = pd.read_sql(
                sql="""
                        SELECT 
                            lib_region, 
                            count(*) as count_tl,
                            json_agg(geo_point_2d) as geom
                        FROM datalake.traffic_lights
                        WHERE lib_region not in ('PERIPHERIQUE')
                        GROUP BY lib_region;
                    """,
                con=connection
            )

        traffic_ligths["code_arr"] = traffic_ligths["lib_region"].apply(lambda x: int("750"+x.split(" ")[1]))
        traffic_ligths["lib_region"] = traffic_ligths["lib_region"].apply(lambda x: x.replace(" ", " n°"))

        paris_arr["code_arr"] = paris_arr["code_arr"].apply(lambda x: int(x)-100)


        traffic_ligths["lat"] = traffic_ligths["geom"].apply(lambda coor_dict: [item["lat"] for item in coor_dict])
        traffic_ligths["lon"] = traffic_ligths["geom"].apply(lambda coor_dict: [item["lon"] for item in coor_dict])

        del traffic_ligths['geom']

        tf_table = pd.merge(traffic_ligths, paris_arr, on='code_arr')

        tf_table["lat"] = tf_table["lat"].apply(lambda x: str(x))
        tf_table["lon"] = tf_table["lon"].apply(lambda x: str(x))

        tf_table.to_sql('tf_placment', con=engine, schema="datawarehouse", if_exists='replace')

        print(f"[✅] : table tf_placment is up-to-date")


CleanDataset(engine).metric_kpi()
CleanDataset(engine).map_kpi()