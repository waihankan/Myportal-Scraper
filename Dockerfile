FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN apt-get update

ENV PYTHONPATH "/app/venv/bin/python3.8"

CMD ["python3", "botend/main_bot.py"]