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

    #initial_timestamp = initial_date +' '+"0:00"
    #final_timestamp = final_date + ' '+ "23:00"

    #dates = pd.date_range(initial_timestamp, final_timestamp, freq="1h")
    #input_values = pd.DataFrame(dates)
    #input_values['building_id'] = building_id
    #input_values['meter'] = meter
    #input_values = input_values.iloc[:,[1,2,0]]
    #print(input_values)
    #input_values = input_values.rename({0:'timestamp'}, axis = 1)

    #X = preprocess(input_values)
    #X = {'building_id': [int(building_id)],'meter': [int(meter)], 'period': [int(dates)]}

    #X = dates.rename(columns={0:'timestamp'})
    #X = preprocess(X)

    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')
    y_pred = (model1.predict(X)+model2.predict(X))/2

    y_pred = pd.DataFrame(y_pred,columns=['Cons. (kwh)'],index = input_values.timestamp )

    to_return = y_pred.to_json()

    return to_return

@app.get("/efficiency")

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


    #initial_timestamp = initial_date +' '+"0:00"
    #final_timestamp = final_date + ' '+ "23:00"

    #dates = pd.date_range(initial_timestamp, final_timestamp, freq="1h")
    #input_values = pd.DataFrame(dates)
    #input_values['building_id'] = building_id
    #input_values['meter'] = meter
    #input_values = input_values.iloc[:,[1,2,0]]
    #print(input_values)
    #input_values = input_values.rename({0:'timestamp'}, axis = 1)

    #print(input_values)

    #X = preprocess(input_values)

    print(X)
    #X = {'building_id': [int(building_id)],'meter': [int(meter)], 'period': [int(dates)]}

    #X = dates.rename(columns={0:'timestamp'})
    #X = preprocess(X)

    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')
    y_pred = (model1.predict(X)+model2.predict(X))/2

    X_sq = np.array(X.iloc[:,6])

    y_pred/=X_sq

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


@app.get("/refit")
def refit(building_id: int,
         meter: int,
         initial_date: str,
         final_date: str,
         primary_use:int=None,
         size_change:float = None):

    initial_timestamp = initial_date +' '+"0:00"
    final_timestamp = final_date + ' '+ "23:00"

    dates = pd.date_range(initial_timestamp, final_timestamp, freq="1h")

    input_values=pd.DataFrame(dates)
    input_values['building_id'] = building_id
    input_values['meter'] = meter
    input_values = input_values.iloc[:,[1,2,0]]
    input_values = input_values.rename(columns={0:'timestamp'})
    X = preprocess(input_values)

    X_modified = X.copy()

    if primary_use:
        X_modified['primary_use'] = primary_use
    if size_change:
        X_modified['square_feet'] *= size_change

    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')

    y_pred = (model1.predict(X)+model2.predict(X))/2

    y_pred_modified = (model1.predict(X_modified)+model2.predict(X_modified))/2

    y =  pd.DataFrame({'Cons. (kwh)':y_pred,'Cons. (kwh) - Retrofit':y_pred_modified},index = input_values.timestamp)

    y_json = y.to_json()

    return y_json

@app.get("/compare")
def compare(building1: int,
            building2: int,
            meter: int,
            initial_date: str,
            final_date: str):

    initial_timestamp = initial_date +' '+"0:00"
    final_timestamp = final_date + ' '+ "23:00"

    dates = pd.date_range(initial_timestamp, final_timestamp, freq="1h")

    input_values1=pd.DataFrame(dates)
    input_values1['building_id'] = building1
    input_values1['meter'] = meter
    input_values1 = input_values1.iloc[:,[1,2,0]]
    input_values1 = input_values1.rename(columns={0:'timestamp'})

    input_values2=pd.DataFrame(dates)
    input_values2['building_id'] = building2
    input_values2['meter'] = meter
    input_values2 = input_values2.iloc[:,[1,2,0]]
    input_values2 = input_values2.rename(columns={0:'timestamp'})

    X1 = preprocess(input_values1)
    X2 = preprocess(input_values2)

    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')

    y_pred1 = (model1.predict(X1)+model2.predict(X1))/2

    y_pred2 = (model1.predict(X2)+model2.predict(X2))/2

    consq1 = y_pred1/X1.square_feet
    consq2= y_pred2/X2.square_feet
    print(consq1)
    print(consq2)

    y =  pd.DataFrame({'cons_kwh1':y_pred1,
                       'cons_square_feet1':list(consq1),
                       'cons_kwh2':y_pred2,
                       'cons_square_feet2':list(consq2)}, index = input_values1.timestamp)

    y_json = y.to_json()

    return y_json

@app.get("/")

def root():
    # $CHA_BEGIN
    return dict(greeting="API is working")
    # $CHA_END
