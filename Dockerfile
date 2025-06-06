FROM python:3.10

ENV PYTHONUNBUFFERED=1

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 40000

CMD ["gunicorn", "system.wsgi:application", "--bind", "0.0.0.0:40000"]