import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import plotly.express as ps
from PIL import Image

import base64


from PIL import Image
import streamlit as st

# You can always call this function where ever you want

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="super_energy_predictor/data/background.png", width=700, height=300)
st.image(my_logo)


#st.header(Image.open('super_energy_predictor/data/background.png'))
image = Image.open('super_energy_predictor/data/background.png')

st.markdown('# Green Leaves Co.')
col1, mid, col2 = st.columns([1,1,6])
with col1:
    image = Image.open('super_energy_predictor/data/office-building.png')
    st.image(image, width = 130)

with col2:
    st.markdown('''
    *Millions of years* were needed to achieve the development level the world enjoys today. \n
    However, besides technology evolution has been increasingly faster so it is our natural resources consumption. \n
    And unfortunately, **the preservation mindset is quite new**. \n
    In this context, Green Leaves Co. effectively takes part in the **urgent mission of saving the planet** through **efficient** and **conscious** energy spending.
    ''')

st.markdown('# The Technologies we use')
col1, mid, col2 = st.columns([1,1,6])
with col1:
    image = Image.open('super_energy_predictor/data/technology.png')
    st.image(image, width = 130)

with col2:
    st.markdown('''
    We use AI tools to predict **future energy consumption** for many different types of buildings. \n
    Our predictions take into consideration the **characteristics of your building** and **weather forecast**.
    With our tools and expertise,  we can also simulate the result of **retrofitting** in any building and what would be the **gain/loss in energy efficiency** after the changes.
    ''')

st.markdown('# How to use the App')

col1, mid, col2 = st.columns([1,1,6])
with col1:
    image = Image.open('super_energy_predictor/data/virtual.png')
    st.image(image, width = 130)

with col2:
    st.markdown('''
    Our app allows a dynamic management of energy efficiency for your building fleet. \n
    In our **first module**, we offer a dashboard to **retrieve key information** about a building along with its **specific energy consumption evolution** based on your chosen timeframe. \n
    Our **second module** allows a modelization of changes in its potential energy consumption based on **updated parameters** (switched primary use, increase/decrease of used sq/feet).
    The impact of those updates can be compared with original building to assess the impact on a hourly/monthly/yearly consumption.\n
    Lastly, our **third module** can fetch data on energy consumption for 2 buildings in your fleet, offering a clear **face-to-face comparison**.
    This can be handy in comparing one specific building against a benchmark and/or detect outlier patterns.
    ''')
