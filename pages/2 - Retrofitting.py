import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import plotly.express as ps
from PIL import Image

col1, mid, col2 = st.columns([1,1,6])
with col1:
    image = Image.open('super_energy_predictor/data/Energy_Icon.gif')
    st.image(image, width = 150)
with col2:
    st.write('''# Super Energy Predictor''')
    st.write('''## Building retro-fitting''')


st.markdown('''
Retro-fitting a building can lead to significant improvements of energy consumption.

Our model allows a new energy consumption calculation, based on new parameters such as surface change (in square-feet)
as well as primary use of the building in order to take into account specific patterns of usage.
''')


url = 'http://127.0.0.1:8000/refit'

col1, col2 = st.columns([1,1])

with col1:
    building_id = st.number_input('Building ID',step=1,format=f'%i',min_value=0,max_value=9999)
with col2:
    #meter = st.number_input('Meter',step=1,format=f'%i',min_value=0,max_value=4)
    meter = col2.selectbox("Select a a meter", ('Electricity', 'Chilled water', 'Steam', 'Hot water'))
    if meter == 'Electricity':
        meter = 0
    if meter == 'Chilled water':
        meter = 1
    if meter == 'Steam':
        meter = 2
    if meter == 'Hot water':
        meter = 3

# Limit dates to the available horizon
min_date = datetime.datetime(2017, 1, 1)
max_date = datetime.datetime(2018, 12, 31)

value_date = datetime.datetime(2017, 1, 1)

col3, col4 = st.columns([1,1])
with col3:
    initial_date = st.date_input("Initial Date",value=value_date, min_value=min_date,max_value=max_date)
    initial_date = str(initial_date)
with col4:
    final_date = st.date_input("Final date",value=value_date, min_value=min_date,max_value=max_date)
    final_date = str(final_date)

col5, col6 = st.columns([1,1])
with col5:
    #primary_use = st.number_input('New Primary Use',format=f'%i',min_value=0,max_value=16)
    df = pd.read_csv('super_energy_predictor/data/building_selection.csv')
    primary_use = st.selectbox("Select a new primary use", df['primary_use'].unique())
    if primary_use == 'Education':
        primary_use = 0
    if primary_use == 'Entertainment/public assembly':
        primary_use = 1
    if primary_use == 'Food sales and service':
        primary_use = 2
    if primary_use == 'Healthcare':
        primary_use = 3
    if primary_use == 'Lodging/residential':
        primary_use = 4
    if primary_use == 'Manufacturing/industrial':
        primary_use = 5
    if primary_use == 'Office':
        primary_use = 6
    if primary_use == 'Other':
        primary_use = 7
    if primary_use == 'Parking':
        primary_use = 8
    if primary_use == 'Public services':
        primary_use = 9
    if primary_use == 'Religious worship':
        primary_use = 10
    if primary_use == 'Retail':
        primary_use = 11


with col6:
    size_change = st.number_input('Proportion size change',step =.1, format=f'%.1f')

freq =  st.selectbox("Frequency", ['Hourly','Daily',"Monthly"])

accu = st.checkbox("Accumulates over the period")

params = {'building_id':building_id,
          'meter':meter,
          'initial_date':initial_date,
          'final_date':final_date,
          'primary_use':primary_use,
          'size_change':size_change
          }

response = requests.get(url=url,params=params)

y_json = response.json()
y_recovered = pd.read_json(y_json)


if freq == 'Daily':
    y_recovered = y_recovered.resample('D').mean()

if freq == 'Monthly':
    y_recovered = y_recovered.resample('M').mean()

if accu:
    graph = ps.line(y_recovered.cumsum())
else:
    graph = ps.line(y_recovered)

st.plotly_chart(graph)
