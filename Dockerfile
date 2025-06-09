FROM python:3.12.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir setuptools

COPY . /code/

EXPOSE 8000