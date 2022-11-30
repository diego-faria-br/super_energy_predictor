FROM --platform=linux/amd64
FROM python:3.8.12-buster
COPY super_energy_predictor super_energy_predictor
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn super_energy_predictor.api.fast:app  --host 0.0.0.0
