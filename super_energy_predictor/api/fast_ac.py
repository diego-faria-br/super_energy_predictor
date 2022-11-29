from datetime import datetime
import pytz
import pandas as pd
import numpy as np
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
def pred(building_id: int, meter: int, initial_date: str, final_date: str):

    initial_timestamp = initial_date +' '+"0:00"
    final_timestamp = final_date + ' '+ "23:00"

    dates = pd.date_range(initial_timestamp, final_timestamp, freq="1h")
    input_values = pd.DataFrame(dates)
    input_values['building_id'] = building_id
    input_values['meter'] = meter
    input_values = input_values.iloc[:,[1,2,0]]
    print(input_values)
    input_values = input_values.rename({0:'timestamp'}, axis = 1)

    X = preprocess(input_values)
    #X = {'building_id': [int(building_id)],'meter': [int(meter)], 'period': [int(dates)]}

    #X = dates.rename(columns={0:'timestamp'})
    #X = preprocess(X)

    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')
    y_pred = (model1.predict(X)+model2.predict(X))/2

    y_pred = pd.DataFrame(y_pred,columns=['Cons. (kwh)'],index = input_values.timestamp )

    to_return = y_pred.to_json()

    return to_return

@app.get("/effiency")
def pred_eff(building_id: int, meter: int, initial_date: str, final_date: str):
    initial_timestamp = initial_date +' '+"0:00"
    final_timestamp = final_date + ' '+ "23:00"

    dates = pd.date_range(initial_timestamp, final_timestamp, freq="1h")
    input_values = pd.DataFrame(dates)
    input_values['building_id'] = building_id
    input_values['meter'] = meter
    input_values = input_values.iloc[:,[1,2,0]]
    print(input_values)
    input_values = input_values.rename({0:'timestamp'}, axis = 1)

    X = preprocess(input_values)
    #X = {'building_id': [int(building_id)],'meter': [int(meter)], 'period': [int(dates)]}

    #X = dates.rename(columns={0:'timestamp'})
    #X = preprocess(X)

    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')
    y_pred = (model1.predict(X)+model2.predict(X))/2/X.iloc[:,6]

    y_pred = pd.DataFrame(y_pred,columns=['Cons. (kwh)'],index = input_values.timestamp )

    to_return = y_pred.to_json()

    return to_return


@app.get("/building_infos")
def info(building_id):
    #X = {'building_id': [int(building_id)],'meter': [int(meter)], 'period': [int(dates)]}
    #df = preprocess(X)

    building_preproc = pd.read_csv("raw_data/building_preproc.csv")
    building_info = building_preproc.loc[(building_preproc['building_id'] == np.int64(building_id))]
    building_info_reset = building_info.drop(['Unnamed: 0'], axis = 1)
    building_dic = building_info_reset.to_dict(orient = 'records')

    #to_return = building_dic[0]

    return building_dic[0]

@app.get("/")

def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
