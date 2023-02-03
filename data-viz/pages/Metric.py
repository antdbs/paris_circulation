import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from config import *

engine = create_engine(DB_URI)

st.set_page_config(layout="wide")
st.markdown("# Metric 🥇")
st.sidebar.markdown("# Metric 🥇")


tl_density = "🚦 Density "

st.balloons()

@st.cache
def load_data():
    with engine.connect() as connection: 

        density_data = pd.read_sql(
            sql="""
                    SELECT *
                    FROM datawarehouse.density;
                """,
            con=connection
        )

        density_data["density_ha"] = density_data["density_ha"].apply(lambda x: round(x, 3))

        density_podium = density_data.sort_values("density_ha" , ascending=False).head(3)

    density_data["lib_region"] = density_data["lib_region"].apply(lambda x: x.replace("Arrondissement", "Arr. "))

    return density_data, density_podium

density_data, density_podium = load_data()


st.markdown("# 🏆 Density podium ")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"""🥇 {density_podium["lib_region"].iloc[0]} 🥇""", density_podium["density_ha"].iloc[0])
    st.caption("I'm the corresponding\nbounding box coordinate\nyou can copy me into Blender 🤖")
    st.code(density_podium["bbox"].iloc[0])
with col2:
    col2.metric(f"""🥈 {density_podium["lib_region"].iloc[1]} 🥈""", density_podium["density_ha"].iloc[1])
    st.caption("I'm the corresponding\nbounding box coordinate\nyou can copy me into Blender 🤖")
    st.code(density_podium["bbox"].iloc[0])
with col3:
    col3.metric(f"""🥉 {density_podium["lib_region"].iloc[2]} 🥉""", density_podium["density_ha"].iloc[2])
    st.caption("I'm the corresponding\nbounding box coordinate\nyou can copy me into Blender 🤖")
    st.code(density_podium["bbox"].iloc[0])

st.markdown("# 🚦 Density ")

for i in range(0, 19, 5):
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(f"""🚦 {density_data["lib_region"].iloc[i]}""", density_data["density_ha"].iloc[i])
    col2.metric(f"""🚦 {density_data["lib_region"].iloc[i+1]}""", density_data["density_ha"].iloc[i+1])
    col3.metric(f"""🚦 {density_data["lib_region"].iloc[i+2]}""", density_data["density_ha"].iloc[i+2])
    col4.metric(f"""🚦 {density_data["lib_region"].iloc[i+3]}""", density_data["density_ha"].iloc[i+3])
    col5.metric(f"""🚦 {density_data["lib_region"].iloc[i+4]}""", density_data["density_ha"].iloc[i+4])