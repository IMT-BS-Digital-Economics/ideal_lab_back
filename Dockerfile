FROM python:3.9-slim-buster

ARG API_PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN apt-get update && apt-get install -y git

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN echo "$API_PORT"

ENV API_PORT_RUNTIME=$API_PORT

COPY . /app

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${API_PORT_RUNTIME} --root-path /api"]