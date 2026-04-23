import os
import streamlit as st
import requests

# Берём из env (для Docker) или дефолт (для локального запуска)
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

st.set_page_config(page_title="Iris Classifier", page_icon="🌸")
st.title("🌸 Iris Flower Classifier")
st.markdown("Enter flower measurements to get a prediction.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        sepal_length = st.number_input("Sepal Length (cm)", 4.0, 8.0, 5.1, 0.1)
        sepal_width = st.number_input("Sepal Width (cm)", 2.0, 5.0, 3.5, 0.1)
    with col2:
        petal_length = st.number_input("Petal Length (cm)", 1.0, 7.0, 1.4, 0.1)
        petal_width = st.number_input("Petal Width (cm)", 0.1, 3.0, 0.2, 0.1)

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()

        st.success(f"**Prediction: {result['label'].upper()}**")
        st.write(f"Class index: {result['prediction']}")
        st.write(f"Confidence: **{result['confidence']*100:.2f}%**")

        st.bar_chart(result["probabilities"])

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Is the FastAPI service running?")
    except Exception as e:
        st.error(f"❌ Error: {e}")