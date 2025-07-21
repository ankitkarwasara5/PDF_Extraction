FROM python:3.11.5-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev build-essential

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn main:app --bind 0.0.0.0:$PORT

