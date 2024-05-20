FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 6000

CMD ["python", "manage.py", "runserver", "0.0.0.0:6000"]