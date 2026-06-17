FROM python:3.11-slim

WORKDIR /app

# copy all requirements libraries
COPY requirements.txt .

RUN pip install --no-chache-dir -r requirements.txt

# copy project's file
COPY /app ./app
COPY fastapi_offline_docs ./fastapi_offline_docs

# port that project run on it
EXPOSE 8000

# to run project
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]