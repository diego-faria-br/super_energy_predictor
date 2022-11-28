import streamlit as st
import requests
import pandas as pd
import numpy as np

'''
# TaxiFareModel front
'''
st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''

date = st.text_input('Date and Time (YYY-mm-dd HH:MM:SS)', '2018-10-10 05:00')

pickup_lat = st.number_input('Insert the pick-up latitute',format="%.6f")
pickup_long = st.number_input('Insert the pick-up longitude',format="%.6f")

dropoff_lat = st.number_input('Insert the dropoff latitute',format="%.6f")
dropoff_long = st.number_input('Insert the dropoff longitude',format="%.6f")

passenger_count = st.number_input('Passengers',format="%.0f")

params = None

if passenger_count:
    params = {'pickup_datetime':date,
            'pickup_longitude':pickup_long,
            'pickup_latitude':pickup_lat,
            'dropoff_longitude':dropoff_long,
            'dropoff_latitude':dropoff_lat,
            'passenger_count':int(passenger_count)
            }

if params == None:
    params = {
        'pickup_datetime':"2013-07-06 17:18:00",
        'pickup_longitude':-73.950655,
        'pickup_latitude':40.783282,
        'dropoff_longitude':-73.950655,
        'dropoff_latitude':40.783282,
        'passenger_count':2

    }


response = requests.get(url=url,params=params)


st.write(response.json())

location = pd.DataFrame([[pickup_lat,pickup_long],
                         [dropoff_lat,dropoff_long]],columns=['lat','lon'])

st.map(location)
