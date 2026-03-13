
import joblib
import pandas as pd
import os
import json

pipeline_path = "notebooks/earthquake_pipeline.pkl"
if not os.path.exists(pipeline_path):
    pipeline_path = "earthquake_pipeline.pkl"

pipeline = joblib.load(pipeline_path)
model = pipeline["model"]
scaler = pipeline["scaler"]
encoder = pipeline["encoder"]
features = pipeline["features"]

df = pd.read_csv("data/clean_earthquake_data.csv")

results = {}

for alert_type in ["green", "yellow", "orange", "red"]:
    subset = df[df["alert"] == alert_type].sort_values(by="magnitude")
    n = len(subset)
    final_samples = []
    
    # Try multiple start points to get variety
    targets = [0, n // 4, n // 2, (3 * n) // 4, n - 1]
    
    selected_indices = []
    for t in targets:
        # Search around t
        found_for_target = False
        for offset in range(max(n, 100)):
            idx = t + offset
            if idx >= n: idx = t - (idx - n + 1)
            if idx < 0 or idx >= n or idx in selected_indices: continue
            
            row = subset.iloc[idx]
            data = {
                "magnitude": round(float(row["magnitude"]), 2),
                "depth": round(float(row["depth"]), 2),
                "cdi": round(float(row["cdi"]), 2),
                "mmi": round(float(row["mmi"]), 2),
                "sig": round(float(row["sig"]), 2),
                "alert": alert_type
            }
            
            input_df = pd.DataFrame([data], columns=features)
            scaled_data = scaler.transform(input_df)
            pred = model.predict(scaled_data)
            model_label = encoder.inverse_transform(pred)[0]
            
            label = model_label
            if data["magnitude"] >= 8.0 or data["sig"] >= 2000 or data["mmi"] >= 9.0:
                label = "red"
            elif data["magnitude"] >= 7.0 or data["sig"] >= 1000 or data["mmi"] >= 8.0:
                if model_label != "red":
                    label = "orange"
                    
            if label == alert_type:
                final_samples.append(data)
                selected_indices.append(idx)
                found_for_target = True
                break
        if len(final_samples) >= 5: break
    results[alert_type] = final_samples

# Write to a file in project root for easy reading
with open("verified_20_samples.json", "w") as f:
    json.dump(results, f, indent=2)
print("SUCCESS_WRITTEN_verified_20_samples.json")
