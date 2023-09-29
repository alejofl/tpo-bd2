FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY requirements.txt /src
RUN pip install --no-cache-dir -r requirements.txt
