FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 40001

CMD ["gunicorn", "system.wsgi:application", "--bind", "0.0.0.0:40001"]