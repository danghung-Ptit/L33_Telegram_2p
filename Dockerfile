FROM python:3.9

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY main.py /app/main.py

COPY config.yml /app/config.yml


CMD ["python", "/app/main.py"]