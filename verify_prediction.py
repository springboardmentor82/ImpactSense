import joblib
import pandas as pd
import os

def verify():
    pipeline_path = "notebooks/earthquake_pipeline.pkl"
    if not os.path.exists(pipeline_path):
        print("Pipeline not found.")
        return

    pipeline = joblib.load(pipeline_path)
    model = pipeline["model"]
    scaler = pipeline["scaler"]
    encoder = pipeline["encoder"]
    features = pipeline["features"]

    # User input
    data = {
        "magnitude": 7.0,
        "depth": 15.0,
        "cdi": 8.0,
        "mmi": 8.0,
        "sig": 1500.0
    }

    input_df = pd.DataFrame([data])
    
    # Ensure correct order
    input_features = input_df[features]
    
    # Scale
    scaled_data = scaler.transform(input_features)
    
    # Predict
    pred = model.predict(scaled_data)
    model_label = encoder.inverse_transform(pred)[0]
    
    # --- SAFETY OVERRIDE LAYER ---
    label = model_label
    # Rule 1: Extreme Red (Severe Disasters)
    if data["magnitude"] >= 8.0 or data["sig"] >= 2000 or data["mmi"] >= 9.0:
        label = "red"
    # Rule 2: Strong Orange (Significant Impact)
    elif data["magnitude"] >= 7.0 or data["sig"] >= 1000 or data["mmi"] >= 8.0:
        if model_label != "red":
            label = "orange"
    # -----------------------------
    
    print(f"Inputs: {data}")
    print(f"Model Result (Raw): {model_label}")
    print(f"Final Prediction (Safe): {label}")

if __name__ == "__main__":
    verify()
