import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Iris ML API")

# Load model once at startup
model = joblib.load("model.joblib")

# Label names for human-readable output
LABELS = ["setosa", "versicolor", "virginica"]


class Features(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/")
def root():
    return {"message": "ML API is running"}


@app.post("/predict")
def predict(features: Features):
    data = np.array([[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]])
    prediction = model.predict(data)[0]
    return {
        "prediction": int(prediction),
        "label": LABELS[prediction],
    }