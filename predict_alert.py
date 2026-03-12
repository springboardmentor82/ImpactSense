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

samples = df.sample(20, random_state=42)

X_samples = samples[features]
y_actual = samples["alert"]

samples_scaled = scaler.transform(X_samples)
samples_scaled = pd.DataFrame(samples_scaled, columns=features)

pred = model.predict(samples_scaled)
alerts = encoder.inverse_transform(pred)

for i in range(len(samples)):
    print("Actual:", y_actual.iloc[i], "| Predicted:", alerts[i])