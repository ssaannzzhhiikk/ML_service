Here's your updated README:

---

# ML FastAPI Docker — Full ML Pipeline

A complete ML system with Iris classification, featuring FastAPI backend, Streamlit frontend, MLflow experiment tracking, and Docker containerization.

## What's Included

- **FastAPI** — REST API serving ML predictions
- **Streamlit** — Interactive web UI for users
- **MLflow** — Experiment tracking and model registry
- **Docker Compose** — One-command deployment of all services

## Project Structure

```
ML_service/
├── main.py              # FastAPI app (loads model from MLflow Registry)
├── train.py             # Training script with MLflow tracking
├── frontend/
│   └── app.py           # Streamlit UI
├── Dockerfile           # FastAPI service image
├── Dockerfile.frontend  # Streamlit service image
├── docker-compose.yml   # Orchestrates API + frontend + MLflow
├── requirements.txt     # Python dependencies
├── model.joblib         # Trained model artifact
└── README.md
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
pip install -r requirements.txt
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

## Tech Stack

- Python 3.11
- FastAPI + Uvicorn
- Streamlit
- scikit-learn
- MLflow
- Docker & Docker Compose
