import joblib
from db import SessionLocal, InputData, Prediction
from datetime import datetime

MODEL_PATH = "model.joblib"


def run_batch_prediction():
    model = joblib.load(MODEL_PATH)
    db = SessionLocal()

    try:
        inputs = db.query(InputData).all()
        new_predictions = 0

        for item in inputs:
            # Skip if already predicted
            exists = db.query(Prediction).filter(Prediction.input_id == item.id).first()
            if exists:
                continue

            features = [[item.sepal_length, item.sepal_width,
                         item.petal_length, item.petal_width]]
            pred = model.predict(features)[0]

            p = Prediction(
                input_id=item.id,
                prediction=str(pred),
                prediction_timestamp=datetime.utcnow()
            )
            db.add(p)
            new_predictions += 1

        db.commit()
        print(f"[{datetime.utcnow()}] Processed {len(inputs)} rows, "
              f"new predictions: {new_predictions}")

    except Exception as e:
        db.rollback()
        print(f"Error during batch prediction: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run_batch_prediction()