import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import plotly.express as ps
from PIL import Image

col1, mid, col2 = st.columns([1,1,6])
with col1:
    image = Image.open('super_energy_predictor/data/compare.png')
    st.image(image, width = 150)
with col2:
    st.write('''# Super Energy Predictor''')
    st.write('''## Building comparison''')


st.markdown('''


Within a fleet of buildings, quickly assess & compare buildings' energy consumption patterns.


''')

url = 'https://super-energy-predictor-cgtg3y2ydq-uc.a.run.app/compare'


# Building IDs
col1, col2 = st.columns([1,1])

with col1:
    building_id1 = st.number_input('Building to Compare (ID)',value=104,step=1,format=f'%i',min_value=0,max_value=9999)
with col2:
    building_id2 = st.number_input('Reference Bulding (ID)',value=100,step=1,format=f'%i',min_value=0,max_value=9999)


if building_id1 == building_id2:
    st.warning('Your are comparing with the same building', icon="⚠️")

# Limit dates to the available horizon
min_date = datetime.datetime(2017, 1, 1)
max_date = datetime.datetime(2018, 12, 31)
value_date = datetime.datetime(2017, 1, 1)
value_date_final = datetime.datetime(2017, 1, 31)

col3, col4 = st.columns([1,1])
with col3:
    initial_date = st.date_input("Initial Date",value=value_date, min_value=min_date,max_value=max_date)
    initial_date = str(initial_date)
with col4:
    final_date = st.date_input("Final date",value=value_date, min_value=min_date,max_value=max_date)
    final_date = str(final_date)


# Especific meter
col5, col6 = st.columns([1,1])
with col5:
    #meter = st.number_input('Meter',step=1,format=f'%i',min_value=0,max_value=4)
    meter = col5.selectbox("Select a a meter", ('Electricity', 'Chilled water', 'Steam', 'Hot water'))
    if meter == 'Electricity':
        meter = 0
    if meter == 'Chilled water':
        meter = 1
    if meter == 'Steam':
        meter = 2
    if meter == 'Hot water':
        meter = 3

with col6:
    freq =  st.selectbox("Frequency", ['Hourly','Daily',"Monthly"])

accu = st.checkbox("Accumulates over the period")

params = {'building1':building_id1,
          'building2':building_id2,
          'meter':meter,
          'initial_date':initial_date,
          'final_date':final_date,
          }

response = requests.get(url=url,params=params)
y_json = response.json()
y_recovered = pd.read_json(y_json)


if freq == 'Daily':
    y_recovered = y_recovered[['cons_square_feet1','cons_square_feet2']].resample('D').mean()

if freq == 'Monthly':
    y_recovered = y_recovered[['cons_square_feet1','cons_square_feet2']].resample('M').mean()

if accu:
    graph = ps.line(y_recovered[['cons_square_feet1','cons_square_feet2']].cumsum())
else:
    graph = ps.line(y_recovered[['cons_square_feet1','cons_square_feet2']])

st.plotly_chart(graph)




col1, col2 , col3 = st.columns(3)

sum_cons1 = float(y_recovered['cons_square_feet1'].sum())

sum_cons2 = float(y_recovered['cons_square_feet2'].sum())

col1.metric("Efficiency",f"{np.round(sum_cons1,1)} Kwh/sqft", "")

col2.metric("Reference", f"{np.round(sum_cons2,1)} Kwh/sqft","")

col3.metric("Difference",f"{np.round(sum_cons1-sum_cons2,2)} Kwh/sqft",delta = f"{np.round((sum_cons1/sum_cons2-1)*100,1)} %")
