import joblib
import pandas as pd

# load pipeline
pipeline = joblib.load("notebooks/earthquake_pipeline.pkl")

model = pipeline["model"]
scaler = pipeline["scaler"]
encoder = pipeline["encoder"]
features = pipeline["features"]

# load dataset
df = pd.read_csv("data/clean_earthquake_data.csv")

# take random rows from dataset
samples = df.sample(10, random_state=42)

X = samples[features]
y = samples["alert"]

# scale
X_scaled = scaler.transform(X)

# predict
pred = model.predict(X_scaled)

pred_labels = encoder.inverse_transform(pred)

print("Actual alerts:")
print(y.values)

print("\nPredicted alerts:")
print(pred_labels)