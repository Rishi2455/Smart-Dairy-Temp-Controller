import streamlit as st
import pandas as pd
import joblib

DATASET_PATH = "data/dairy_products.csv"
MODEL_PATH = "model/temp_model.pkl"

df = pd.read_csv(DATASET_PATH)
model = joblib.load(MODEL_PATH)

st.title("🥛 Smart Dairy Room Temperature Recommender")

products = df['Product'].tolist()
selected = st.multiselect("Select products in storage:", products)
external_temp = st.slider("External temperature (°C):", -10, 40, 25)

if st.button("Predict Recommended Room Temperature"):
    if not selected:
        st.error("Please select at least one product!")
    else:
        features = {'ExternalTemp': [external_temp]}
        for p in products:
            features[f'Has_{p}'] = [1 if p in selected else 0]
        X_input = pd.DataFrame(features)

        prediction = model.predict(X_input)[0]
        st.success(f"✅ Recommended Room Temperature: **{prediction:.1f}°C**")
