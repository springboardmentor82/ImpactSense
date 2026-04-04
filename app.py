from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("earthquake_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        data["magnitude"],
        data["depth"],
        data["mmi"],
        data["cdi"],
        data["sig"]
    ]])

    prediction = model.predict(features)[0]

    return jsonify({"prediction": float(prediction)})

if __name__ == "__main__":
    app.run(debug=True)