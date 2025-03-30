# Use official Python image
FROM python:3.10

WORKDIR /code
COPY ./app ./app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

 
