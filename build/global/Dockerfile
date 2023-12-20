FROM tiangolo/uvicorn-gunicorn:python3.11-slim

RUN apt-get update
RUN apt-get install -y --no-install-recommends

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
