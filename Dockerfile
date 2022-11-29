FROM --platform=linux/amd64 tensorflow/tensorflow:2.10.0
COPY taxifare/ /taxifare
COPY requirements_prod.txt /requirements_prod.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn taxifare.api.fast:app  --host 0.0.0.0
