from datetime import datetime
import pytz
import pandas as pd

from super_energy_predictor.preprocessing.preprocessing import preprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import lightgbm as lgb

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    )

#app.state.model = load_model()
#uvicorn simple:app --reload

@app.get("/predict")
def pred(building_id: int,
         meter: int,
         timestamp: str
         ):
    X = {'building_id': [int(building_id)],'meter': [int(meter)],'timestamp': [timestamp]}
    X = preprocess(X)
    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')
    y_pred = (model1.predict(X)+model2.predict(X))/2

    to_return = {'meter_reading':float(y_pred)}

    return to_return

@app.get("/retrofit")
def pred(building_id: int,
         meter: int,
         initial_date: str,
         final_date: str,
         primary_use:int=None,
         size_change:float = None):

    initial_timestamp = initial_date +' '+"0:00"
    final_timestamp = final_date + ' '+ "23:00"

    dates = pd.date_range(initial_timestamp, final_timestamp, freq="1h")
    input_values=pd.DataFrame(dates)
    input_values['building_id'] = 100
    input_values['meter'] = 0
    input_values = input_values.iloc[:,[1,2,0]]
    input_values = input_values.rename(columns={0:'timestamp'})

    X = preprocess(input_values)

    if primary_use:
        X['primary_use'] = primary_use
    if primary_use:
        X['square_feet'] = X['square_feet']*size_change
    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')
    y_pred = (model1.predict(X)+model2.predict(X))/2

    y_pred = pd.DataFrame(y_pred,columns=['Cons. (kwh)'],index = input_values.timestamp )

    to_return = y_pred.to_json()

    return to_return

@app.get("/")

def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
