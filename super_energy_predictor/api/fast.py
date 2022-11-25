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
def pred(building_id: int, meter: int, timestamp: str):
    X = {'building_id': [int(building_id)],'meter': [int(meter)],'timestamp': [timestamp]}
    X = preprocess(X)
    model1 = lgb.Booster(model_file='raw_data/model1.txt')
    model2 = lgb.Booster(model_file='raw_data/model2.txt')
    y_pred = (model1.predict(X)+model2.predict(X))/2

    to_return = {'meter_reading':float(y_pred)}

    return to_return

@app.get("/")

def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
