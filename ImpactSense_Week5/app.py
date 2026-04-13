import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from flask import Flask, request, jsonify

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("preprocessed_earthquake_data.csv")

# ==============================
# PREPROCESSING
# ==============================
df = df.fillna(df.mean(numeric_only=True))

df['magnitude_category'] = pd.cut(
    df['mag'],
    bins=[0, 2.5, 5, 10],
    labels=['Low', 'Medium', 'High']
)

df = df.dropna(subset=['magnitude_category'])

X = df[['latitude', 'longitude', 'depth_km', 'sig']]
y = df['magnitude_category']

# ==============================
# TRAIN MODEL
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# ==============================
# SAVE MODEL
# ==============================
joblib.dump(model, "earthquake_model.pkl")
print("Model saved successfully")

# ==============================
# FLASK API
# ==============================
app = Flask(__name__)

loaded_model = joblib.load("earthquake_model.pkl")

@app.route('/')
def home():
    return "API Running Successfully"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    sample = pd.DataFrame([{
        'latitude': data['latitude'],
        'longitude': data['longitude'],
        'depth_km': data['depth_km'],
        'sig': data['sig']
    }])

    prediction = loaded_model.predict(sample)

    return jsonify({"prediction": prediction[0]})

# ==============================
# RUN SERVER
# ==============================
if __name__ == '__main__':
    app.run(debug=True)