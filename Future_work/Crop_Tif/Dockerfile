FROM python:3.8-slim

ENV PYTHONBUFFERED 1
ENV PYTHONPATH "/app"

RUN apt-get update && apt-get install --yes libgdal-dev
RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt

COPY crop_tif/ crop_tif/

ENTRYPOINT ["python", "-m", "crop_tif"]