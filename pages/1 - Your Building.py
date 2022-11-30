import urllib.request

import matplotlib
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import streamlit as st
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
from pandas import json_normalize
from PIL import Image
from streamlit_lottie import st_lottie
import math
import plotly.express as ps


#st.set_page_config(page_title="Super Energy Predictor", layout="wide")

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url("/Users/diegooliveirafaria/code/diego-faria-br/super_energy_predictor/Sample.png");
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Green Leaves Co.";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()




def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_book = load_lottieurl("https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json")
st_lottie(lottie_book, speed=1, height=200, key="initial")

#API address - to be changed after google cloud implementation

url_mod1 = 'http://127.0.0.1:8000/predict'

url_mod1_2 = 'http://127.0.0.1:8000/efficiency'



matplotlib.use("agg")

_lock = RendererAgg.lock


sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

row0_1.title("Super Energy Predictor")

with row0_2:
    st.write("")

row0_2.subheader(
    "A Streamlit web app by [Alexandre Chartier](https://github.com/opxal89), [Ana Gama](https://github.com/anaflaviagama) and [Diego Faria](https://github.com/diego-faria-br/)"
)


row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

with row1_1:
    st.markdown(
        "Climate has been changing in plain sight. And unfortunately, extreme weather events from heat waves, floods, forest fires have become an everyday reality of our lives."
    )
    st.markdown(
        "**Then, what can you do to effectively switch this path?**"
    )
    st.markdown(
        "**We created Super Energy Predictor to help companies to develop strategies considering energy consumption and efficiency when choosing their new buildings.**"
    )


columns = st.columns(3)

site_name = 'University of Central Florida, Orlando, FL'


df = pd.read_csv('super_energy_predictor/data/building_selection.csv')
site_name = columns[0].selectbox(
        "Select a site", df['site_name'].unique())

site_id = df[df['site_name'] == site_name]['site_id'].values[0]

def building_selection(df):
    keys = df['site_name'].unique()
    response = {}
    for key in keys:
        building_list = df[df['site_name'] == key]['building_id'].to_list()
        response[key] = building_list
    return response

dict_building = building_selection(df)

selected_building_id = columns[1].selectbox("Select a building", dict_building[site_name])

meter = columns[2].selectbox(
        "Select a a meter",
        ('Electricity',
         'Chilled water',
         'Steam',
         'Hot water'
         ))

if meter == 'Electricity':
    meter_num = 0
if meter == 'Chilled water':
    meter_num = 1
if meter == 'Steam':
    meter_num = 2
if meter == 'Hot water':
    meter_num = 3


import datetime

columns = st.columns(2)

start_date = columns[0].date_input(
    "Select a start date",
    datetime.date(2019, 7, 1))

end_date = columns[1].date_input(
    "Select an end date",
    datetime.date(2019, 7, 1))

st.markdown("""
    # Outputs
""")

col1, col2, col3 = st.columns(3)
col1.metric("Size", df[df['building_id'] == selected_building_id]['square_feet'], 'sqft')
col2.metric("Year built", df[df['building_id'] == selected_building_id]['year_built'].values[0])
col3.metric("Primary use", df[df['building_id'] == selected_building_id]['primary_use'].values[0])

start_date = str(start_date)
end_date = str(end_date)


params = {'building_id': selected_building_id,
          'meter': meter_num,
          'initial_date': start_date,
          'final_date': end_date
          }

response = requests.get(url_mod1,params=params)

y = response.json()
y = pd.read_json(y)
energy_consumption  = float(y.sum())







col1, col2 = st.columns(2)
col1.metric("Energy consumption",f'{np.round(energy_consumption,2)} Kwh', "")

response2= requests.get(url_mod1_2,params=params)

response2.status_code
y_eff = response2.json()
y_eff = pd.read_json(y_eff)
efficiency = float(y_eff.sum())
col2.metric("Energy efficiency", f'{np.round(efficiency,2)} Kwh/sqft',"")



line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))


freq =  st.selectbox("Frequency", ['Hourly','Daily',"Monthly"])

accu = st.checkbox("Accumulates over the period")

y_recovered = y

if freq == 'Daily':
    y_recovered = y_recovered.resample('D').mean()

if freq == 'Monthly':
    y_recovered = y_recovered.resample('M').mean()

if accu:
    graph = ps.line(y_recovered.cumsum())
else:
    graph = ps.line(y_recovered)

st.plotly_chart(graph)
