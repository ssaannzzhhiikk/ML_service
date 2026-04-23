import mlflow
import mlflow.sklearn
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# Config
MLFLOW_TRACKING_URI = "http://localhost:5001"
EXPERIMENT_NAME = "iris_classification"
MODEL_NAME = "iris-rf-model"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

# Load data
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Hyperparameters
params = {
    "n_estimators": 100,
    "random_state": 42,
    "max_depth": None,
}

with mlflow.start_run(run_name="rf_run_v1") as run:
    # Train
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="weighted")

    print(f"Accuracy: {acc:.4f}")
    print(f"F1-score: {f1:.4f}")

    # Log to MLflow
    mlflow.log_params(params)
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("f1_score", f1)

    # Save local copy
    joblib.dump(model, "model.joblib")
    mlflow.log_artifact("model.joblib")

    # Log model for Registry (ПРАВИЛЬНЫЙ СПОСОБ)
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MODEL_NAME
    )

    print(f"Run ID: {run.info.run_id}")
    print(f"Model registered as: {MODEL_NAME}")

print("Done.")