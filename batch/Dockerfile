FROM python:3.11-slim

WORKDIR /app

COPY batch/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY batch/*.py .
COPY ml/model.joblib .

CMD ["python", "scheduler.py"]