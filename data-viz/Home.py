import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pydeck as pdk

from config import *

engine = create_engine(DB_URI)

st.set_page_config(layout="wide")
st.markdown("# Map 🗺")
st.sidebar.markdown("# Map 🗺")

@st.cache(allow_output_mutation=True)
def load_data():
    with engine.connect() as connection: 

        tf_data = pd.read_sql(
            sql="""
                    SELECT *
                    FROM datawarehouse.tf_placment;
                """,
            con=connection
        )

        tf_data["lat"] = tf_data["lat"].apply(lambda x: eval(x))
        tf_data["lon"] = tf_data["lon"].apply(lambda x: eval(x))

    return tf_data.sort_values("code_arr" , ascending=True)

tf_data = load_data()

col1, col2, col3 = st.columns(3)

with col1:
    option = st.selectbox(
        'Which place would you like to see ?',
        tf_data["lib_region"]
    )

filter_df = tf_data[tf_data["lib_region"] == option]

data = np.array([filter_df["lat"].values[0], filter_df["lon"].values[0]])

data = data.transpose()

data = pd.DataFrame(data, columns=['lat', 'lon'])

with col2:
    st.metric("Surface (m²)", filter_df["surface"])

with col3:
    st.metric("Perimetre (m)", filter_df["perimetre"])

col1, col2= st.columns([3, 1])

with col1:
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=48.8534100,
            longitude=2.3488000,
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=20,
            ),
        ],
    ))

with col2:
    st.metric("Nom officiel", filter_df["official_name"].iloc[0])
    st.metric("Code postal", filter_df["code_arr"])
    st.metric("Nombre 🚦", filter_df["count_tl"])
