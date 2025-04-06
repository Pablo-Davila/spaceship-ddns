FROM python:3.13-slim

WORKDIR /app

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
ADD . .

CMD ["python3", "spaceship_ddns.py"]
