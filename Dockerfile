FROM --platform=linux/amd64 python:3.8.12-buster
COPY super_energy_predictor super_energy_predictor
COPY requirements_api.txt requirements_api.txt
COPY raw_data/model1.txt raw_data/model1.txt
COPY raw_data/model2.txt raw_data/model2.txt
COPY raw_data/weather_preproc.csv raw_data/weather_preproc.csv
COPY raw_data/building_preproc.csv raw_data/building_preproc.csv
RUN pip install --upgrade pip
RUN pip install -r requirements_api.txt
CMD uvicorn super_energy_predictor.api.fast:app  --host 0.0.0.0 --port $PORT
