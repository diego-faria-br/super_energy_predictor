###########################################################################################################
###########################################################################################################
###########################################################################################################
######## Le Wagon batch #1011
######## authors = Alexandre Chartier, Ana Gama, Diego Faria
######## version = 1.0
######## status = WIP
######## deployed at = https://share.streamlit.io/tdenzl/bulian/main/BuLiAn.py
######## layout inspired by https://share.streamlit.io/tylerjrichards/streamlit_goodreads_app/books.py
###########################################################################################################
###########################################################################################################
###########################################################################################################

import matplotlib
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import streamlit as st
from matplotlib.backends.backend_agg import RendererAgg
import plotly.express as ps
import datetime
from PIL import Image




st.set_page_config(page_title="Predict the Future of Your Building", layout="wide")


### Data Import ###

matplotlib.use("agg")

_lock = RendererAgg.lock

### Helper Methods ###

########################
### ANALYSIS METHODS ###
########################

sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)



###################


url_mod1 = 'http://127.0.0.1:8000/predict'

url_mod1_2 = 'http://127.0.0.1:8000/efficiency'


####

####################
### INTRODUCTION ###
####################
col1, mid, col2 = st.columns([1,1,6])
with col1:
    image = Image.open('super_energy_predictor/data/compare.png')
    st.image(image, width = 150)
with col2:
    st.write('''# Super Energy Predictor''')
    st.write('''## Analyse your Bulding''')

#################
### MODULE 1 ###
#################

### Inputs ###

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


columns = st.columns(2)

start_date = columns[0].date_input(
    "Select a start date",
    datetime.date(2019, 7, 1))

start_date = str(start_date)

end_date = columns[1].date_input(
    "Select an end date",
    datetime.date(2019, 7, 1))

end_date = str(end_date)

### Outputs ###

st.markdown("""
    # Outputs
""")

if site_name == 'University of Central Florida, Orlando, FL':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **University of Central Florida, Orlando, FL**')
        st.image('img/img_0.png', width=900)
    with col3:
        st.write("")

if site_name == 'Southampton University, UK':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Southampton University, UK**')
        st.image('img/img_1.png', width=900)
    with col3:
        st.write("")

if site_name == 'Arizona State University, Tempe, AZ':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Arizona State University, Tempe, AZ**')
        st.image('img/img_2.png', width=900)
    with col3:
        st.write("")

if site_name == 'Washington DC, WA':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Washington DC, WA**')
        st.image('img/img_3.png', width=900)
    with col3:
        st.write("")

if site_name == 'University of California, Berkeley, CA':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **University of California, Berkeley, CA**')
        st.image('img/img_4.png', width=900)
    with col3:
        st.write("")

if site_name == 'London, UK':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **London, UK**')
        st.image('img/img_5.png', width=900)
    with col3:
        st.write("")

if site_name == 'Philadelphia, PA':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Philadelphia, PA**')
        st.image('img/img_6.png', width=900)
    with col3:
        st.write("")

if site_name == 'Montreal/Ottawa, Canada (site 1)':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Montreal/Ottawa, Canada (site 1)**')
        st.image('img/img_7.png', width=900)
    with col3:
        st.write("")

if site_name == 'Orlando, FL':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Orlando, FL**')
        st.image('img/img_8.png', width=900)
    with col3:
        st.write("")

if site_name == 'University of Texas at Austin, Texas':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **University of Texas at Austin, Texas**')
        st.image('img/img_9.png', width=900)
    with col3:
        st.write("")

if site_name == 'Weber State University, Ogden, Utah':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Weber State University, Ogden, Utah**')
        st.image('img/img_10.png', width=900)
    with col3:
        st.write("")

if site_name == 'Montreal/Ottawa, Canada (site 2)':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Montreal/Ottawa, Canada (site 2)**')
        st.image('img/img_11.png', width=900)
    with col3:
        st.write("")

if site_name == 'Ireland':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Ireland**')
        st.image('img/img_12.png', width=900)
    with col3:
        st.write("")


if site_name == 'University of Minnesota, Twin Cities, MN':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **University of Minnesota, Twin Cities, MN**')
        st.image('img/img_13.png', width=900)
    with col3:
        st.write("")

if site_name == 'Charlottesville, VA':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Charlottesville, VA**')
        st.image('img/img_14.png', width=900)
    with col3:
        st.write("")

if site_name == 'Cornell University, Ithaca, New York':
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown('## **Cornell University, Ithaca, New York**')
        st.image('img/img_15.png', width=900)
    with col3:
        st.write("")

st.text("")
st.text("")


col1, col2, col3 = st.columns(3)
col1.metric("Size", str(df[df['building_id'] == selected_building_id]['square_feet'].values[0]) + ' sqft')
col2.metric("Year built", (df[df['building_id'] == selected_building_id]['year_built'].values[0]))
col3.metric("Primary use", df[df['building_id'] == selected_building_id]['primary_use'].values[0])
####

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

#response2.status_code
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
