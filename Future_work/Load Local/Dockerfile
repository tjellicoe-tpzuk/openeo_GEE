FROM python:3.12-slim

ENV PYTHONBUFFERED 1
ENV PYTHONPATH "/app"

RUN apt-get update
RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install -r requirements.txt

COPY openeo-load-local/ openeo-load-local/

ENTRYPOINT ["python", "-m", "openeo-load-local"]