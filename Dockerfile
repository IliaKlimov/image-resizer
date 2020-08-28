FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt


