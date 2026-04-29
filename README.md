
# ML FastAPI Docker — Full ML Pipeline

A complete ML system with Iris classification, featuring FastAPI backend, Streamlit frontend, MLflow experiment tracking, **batch prediction pipeline**, and Docker containerization.

## What's Included

- **FastAPI** — REST API serving real-time ML predictions
- **Streamlit** — Interactive web UI for users
- **MLflow** — Experiment tracking and model registry
- **Batch Prediction Pipeline** — Scheduled offline predictions with PostgreSQL
- **Docker Compose** — One-command deployment of all services

## Project Structure

```
ML_service/
├── api/                      # FastAPI service
│   ├── main.py               # REST API (loads model.joblib)
│   ├── Dockerfile            # API container image
│   └── requirements.txt      # FastAPI dependencies
├── batch/                    # Batch prediction pipeline
│   ├── batch_predict.py      # Read DB → predict → write DB
│   ├── scheduler.py          # APScheduler (runs every 5 min)
│   ├── db.py                 # SQLAlchemy models
│   ├── init_db.py            # Create database tables
│   ├── seed_data.py          # Populate input_data
│   ├── Dockerfile            # Batch container image
│   └── requirements.txt      # Batch dependencies
├── frontend/                 # Streamlit UI
│   ├── app.py                # Web interface
│   ├── Dockerfile            # Frontend container image
│   └── requirements.txt      # Streamlit dependencies
├── ml/                       # Training & artifacts
│   ├── train.py              # Training script with MLflow tracking
│   └── model.joblib          # Trained model artifact
├── docker-compose.yml        # Orchestrates all services
├── README.md
├── .dockerignore
└── .gitignore
```

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local training)

## Step 1 — Train and register the model

Start MLflow first (needed for model registration):

```bash
docker-compose up -d mlflow
```

Then train locally:

```bash
pip install -r requirements-api.txt
python train.py
```

This will:
- Train a RandomForest classifier
- Log hyperparameters, accuracy, and F1-score to MLflow
- Register the model as `iris-rf-model` in the Model Registry
- Save `model.joblib` locally

Verify in MLflow UI: `http://127.0.0.1:5001/`

## Step 2 — Launch full stack

```bash
docker-compose up --build -d
```

Services will be available at:

| Service | URL | Description |
|---------|-----|-------------|
| FastAPI | `http://127.0.0.1:8000/` | Health check |
| FastAPI Docs | `http://127.0.0.1:8000/docs` | Swagger UI |
| Streamlit | `http://127.0.0.1:8501/` | Web UI for predictions |
| MLflow | `http://127.0.0.1:5001/` | Experiment tracking & registry |

> **Note:** On Windows with Docker Desktop, use `127.0.0.1` instead of `localhost`.

## Step 3 — Initialize batch prediction pipeline

After the stack is running, create tables and seed input data:

```bash
# Create tables
docker-compose run --rm batch python init_db.py

# Insert sample input data
docker-compose run --rm batch python seed_data.py
```

Run the batch pipeline manually once to verify:

```bash
docker-compose run --rm batch python batch_predict.py
```

You should see:
```
[2026-04-29 19:37:01] Processed 5 rows, new predictions: 5
```

Check predictions in the database:

```bash
docker-compose exec db psql -U mluser -d mlservice -c "SELECT * FROM predictions;"
```

The `batch` service is already running via `scheduler.py` and will automatically execute every **5 minutes**.

View scheduler logs:

```bash
docker-compose logs -f batch
```

## Batch Prediction Pipeline (Practice 7)

This module implements an automated batch prediction system:

1. **Database** — PostgreSQL stores `input_data` (features) and `predictions` (results + timestamp)
2. **Batch Script** — `batch_predict.py` connects to DB, loads `model.joblib`, generates predictions, and writes results back
3. **Scheduling** — `scheduler.py` uses APScheduler to run the batch pipeline automatically every 5 minutes
4. **Idempotency** — The script skips rows that already have predictions, preventing duplicates

### Database Schema

| Table | Columns |
|-------|---------|
| `input_data` | `id`, `sepal_length`, `sepal_width`, `petal_length`, `petal_width` |
| `predictions` | `id`, `input_id`, `prediction`, `prediction_timestamp` |

## Tech Stack

- Python 3.11
- FastAPI + Uvicorn
- Streamlit
- scikit-learn
- MLflow
- SQLAlchemy + PostgreSQL
- APScheduler
- Docker & Docker Compose
