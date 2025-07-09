import joblib
import pandas as pd

def load_model(path):
    return joblib.load(path)

def predict_temperature(model, selected_products, external_temp, product_list):
    data = {p: (1 if p in selected_products else 0) for p in product_list}
    data["external_temp"] = external_temp
    df = pd.DataFrame([data])
    return model.predict(df)[0]
