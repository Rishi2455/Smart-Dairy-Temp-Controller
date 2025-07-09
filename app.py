import streamlit as st
import pandas as pd
from utils.model_utils import load_model, predict_temperature

st.set_page_config(page_title="Smart Dairy Temp Controller", layout="centered")

# Load resources
products_df = pd.read_csv("data/dairy_products.csv")
product_list = products_df["product"].tolist()
model = load_model("model/temp_model.pkl")

st.title("🥛 Smart Dairy Room Temperature Controller")
st.markdown("Use this app to get the **ideal room temperature** for storing selected dairy items based on the current external temperature.")

st.sidebar.header("🔍 How to Use")
st.sidebar.markdown("""
1. Select one or more dairy items from the list.
2. Enter the current external temperature in °C.
3. Click the button to get the AI-recommended room temperature.
""")

# Sidebar Product Info Table
st.sidebar.markdown("---")
st.sidebar.subheader("🧊 Product Temp Requirements")

for _, row in products_df.iterrows():
    st.sidebar.markdown(
        f"**{row['product'].capitalize()}**: {row['min_temp']}°C to {row['max_temp']}°C"
    )

# Form input
selected_products = st.multiselect("Select Dairy Products", product_list)
ext_temp = st.number_input("External Temperature (°C)", min_value=-30.0, max_value=60.0, value=25.0)

if st.button("🔎 Get Recommended Room Temperature"):
    if not selected_products:
        st.warning("Please select at least one dairy product.")
    else:
        isolated_items = {"Ice cream", "Ghee"}
        selected_set = set(selected_products)

        if isolated_items & selected_set and len(selected_set) > 1:
            conflict_items = isolated_items & selected_set
            st.error(f"❌ These items are not recommended to be stored with others: {', '.join(conflict_items)}")
            
        else:
            result = predict_temperature(model, selected_products, ext_temp, product_list)
            st.success(f"✅ Recommended Storage Temperature: **{result:.2f}°C**")
