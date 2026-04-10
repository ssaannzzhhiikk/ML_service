# ML FastAPI Docker

A simple Iris classification model served via FastAPI and containerized with Docker.

## Project Structure

```
ml-fastapi-docker/
├── main.py           # FastAPI application
├── train.py          # Model training script
├── model.joblib      # Saved model artifact
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container instructions
└── README.md
```

## Step 1 — Train the model

```bash
pip install -r requirements.txt
python train.py
```

This creates `model.joblib`.

## Step 2 — Run locally

```bash
uvicorn main:app --reload
```

Test endpoints:
- `GET  http://localhost:8000/`          → health check
- `POST http://localhost:8000/predict`   → prediction
- `GET  http://localhost:8000/docs`      → Swagger UI

Example request body for /predict:
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

## Step 3 — Build Docker image

```bash
docker build -t ml-fastapi .
```

## Step 4 — Run Docker container

```bash
docker run -p 8000:8000 ml-fastapi
```

The same endpoints are now available from inside the container.