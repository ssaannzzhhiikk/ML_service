import os
import joblib
import numpy as np
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Iris ML API")

# MLflow config
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001")
MODEL_NAME = "iris-rf-model"
MODEL_VERSION = "1"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Load model from MLflow Model Registry
try:
    model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"
    model = mlflow.sklearn.load_model(model_uri)
    print(f"Loaded model: {model_uri}")
except Exception as e:
    print(f"Registry load failed ({e}), falling back to local model.joblib")
    model = joblib.load("../model.joblib")

LABELS = ["setosa", "versicolor", "virginica"]


class Features(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/")
def root():
    return {"message": "ML API is running", "model": MODEL_NAME}


@app.post("/predict")
def predict(features: Features):
    data = np.array([[features.sepal_length, features.sepal_width,
                      features.petal_length, features.petal_width]])
    prediction = model.predict(data)[0]
    proba = model.predict_proba(data)[0].tolist()
    return {
        "prediction": int(prediction),
        "label": LABELS[prediction],
        "confidence": round(max(proba), 4),
        "probabilities": {LABELS[i]: round(p, 4) for i, p in enumerate(proba)},
    }