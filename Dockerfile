FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 40000

CMD ["gunicorn", "system.wsgi:application", "--bind", "0.0.0.0:40000"]
