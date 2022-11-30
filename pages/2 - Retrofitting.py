import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import plotly.express as ps
import base64


'''
# Super Energy Predictior
'''
st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')


url = 'http://127.0.0.1:8000/refit'



building_id = st.number_input('Building ID',step=1,format=f'%i',min_value=0,max_value=9999)

meter = st.number_input('Meter',step=1,format=f'%i',min_value=0,max_value=4)


# Limit dates to the available horizon
min_date = datetime.datetime(2017, 1, 1)
max_date = datetime.datetime(2018, 12, 31)
value_date = datetime.datetime(2017, 1, 1)


initial_date = st.date_input("Initial Date",value=value_date, min_value=min_date,max_value=max_date)
initial_date = str(initial_date)
final_date = st.date_input("Final date",value=value_date, min_value=min_date,max_value=max_date)
final_date = str(final_date)

primary_use = st.number_input('New Primary Use',format=f'%i',min_value=0,max_value=16)
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
