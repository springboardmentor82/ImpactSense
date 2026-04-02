"""
ImpactSense — Flask Backend API
ML Model: GradientBoostingClassifier (98.6% accuracy)
Input: z-score normalized features (same scale as training CSV)
Features: magnitude, depth, cdi, mmi, sig
Classes: 0=green, 1=yellow, 2=orange, 3=red
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "impact_model.pkl")
model = joblib.load(MODEL_PATH)

ALERT_MAP  = {0: "green", 1: "yellow", 2: "orange", 3: "red"}
ALERT_COLORS = {"green":"#22c55e","yellow":"#facc15","orange":"#fb923c","red":"#ef4444"}
ALERT_DESC = {
    "green":  "Low impact — minimal damage expected",
    "yellow": "Moderate alert — light damage possible",
    "orange": "Significant alert — moderate damage expected",
    "red":    "Critical alert — severe damage expected",
}
FEATURES = ["magnitude", "depth", "cdi", "mmi", "sig"]

# Z-score → approximate raw value for display hints
ZSCORE_HINTS = {
    "magnitude": {"-2":"M2.5","-1":"M4.0","0":"M5.5","1":"M7.0","2":"M8.5"},
    "depth":     {"-1":"5km","0":"35km","1":"80km","2":"125km","3":"170km"},
    "cdi":       {"-2":"1.0","-1":"2.7","0":"4.5","1":"6.2","2":"8.0"},
    "mmi":       {"-3":"I","-2":"II","-1":"III","0":"IV","1":"VI","2":"VIII"},
    "sig":       {"-2":"~100","-1":"~400","0":"~700","1":"~1000","2":"~1300"},
}

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "ImpactSense ML API",
        "model":   "GradientBoostingClassifier",
        "accuracy":"98.6%",
        "note":    "Accepts z-score normalized inputs (same scale as training data)",
        "features": FEATURES,
        "input_range": "Typically -3 to +3 (z-scores)",
        "zscore_hints": ZSCORE_HINTS,
        "classes": ALERT_MAP,
        "endpoints": {
            "GET  /health":         "Health check",
            "GET  /model/info":     "Model metadata + feature ranges",
            "POST /predict":        "Single prediction (z-score inputs)",
            "POST /predict/batch":  "Batch predictions (array, max 500)",
        }
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "model_type": type(model).__name__,
        "accuracy": "98.6%",
    })

@app.route("/model/info", methods=["GET"])
def model_info():
    params = model.get_params()
    return jsonify({
        "type":          type(model).__name__,
        "n_estimators":  params.get("n_estimators"),
        "learning_rate": params.get("learning_rate"),
        "max_depth":     params.get("max_depth"),
        "features":      FEATURES,
        "n_features":    int(model.n_features_in_),
        "classes":       ALERT_MAP,
        "accuracy":      "98.6%",
        "training_data": "414 USGS earthquake events (z-score normalized)",
        "input_format":  "z-score normalized values, typically in range [-3, +3]",
        "zscore_hints":  ZSCORE_HINTS,
    })

@app.route("/predict", methods=["POST"])
def predict():
    """
    POST /predict
    Accepts z-score normalized inputs (same scale as training CSV):

    {
        "magnitude": 0.78,   // z-score: ~0 = M5.5, +1 = M7.0
        "depth":    -0.69,   // z-score: ~0 = 35km, -1 = 5km
        "cdi":       0.81,   // z-score: ~0 = CDI 4.5
        "mmi":       1.03,   // z-score: ~0 = MMI IV
        "sig":       0.92    // z-score: ~0 = SIG 700
    }
    """
    data = request.get_json(force=True)
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing features: {missing}",
                        "required": FEATURES,
                        "hint": "Values should be z-score normalized (range approx -3 to +3)"}), 400
    try:
        vals = [float(data[f]) for f in FEATURES]
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input: {e}"}), 400

    # Validate reasonable z-score range
    for f, v in zip(FEATURES, vals):
        if abs(v) > 6:
            return jsonify({"error": f"'{f}' value {v} seems extreme. Expected z-score in [-3, +3] range."}), 400

    X = np.array([vals])
    pred_class = int(model.predict(X)[0])
    proba      = model.predict_proba(X)[0].tolist()
    alert      = ALERT_MAP[pred_class]

    return jsonify({
        "alert":       alert,
        "alert_code":  pred_class,
        "color":       ALERT_COLORS[alert],
        "description": ALERT_DESC[alert],
        "confidence":  round(float(proba[pred_class]) * 100, 1),
        "probabilities": {
            "green":  round(proba[0] * 100, 2),
            "yellow": round(proba[1] * 100, 2),
            "orange": round(proba[2] * 100, 2),
            "red":    round(proba[3] * 100, 2),
        },
        "input_normalized": {f: round(v, 4) for f, v in zip(FEATURES, vals)},
    })

@app.route("/predict/batch", methods=["POST"])
def predict_batch():
    """
    POST /predict/batch
    { "events": [ {"magnitude":0.78,"depth":-0.69,"cdi":0.81,"mmi":1.03,"sig":0.92}, ... ] }
    Max 500 events per call.
    """
    data   = request.get_json(force=True)
    events = data.get("events", [])
    if not events or not isinstance(events, list):
        return jsonify({"error": "Provide an 'events' array"}), 400
    if len(events) > 500:
        return jsonify({"error": "Max 500 events per batch"}), 400

    X_batch = []
    for i, ev in enumerate(events):
        missing = [f for f in FEATURES if f not in ev]
        if missing:
            return jsonify({"error": f"Event {i}: missing {missing}"}), 400
        try:
            X_batch.append([float(ev[f]) for f in FEATURES])
        except (ValueError, TypeError) as e:
            return jsonify({"error": f"Event {i}: {e}"}), 400

    X      = np.array(X_batch)
    preds  = model.predict(X).tolist()
    probas = model.predict_proba(X).tolist()
    results = []
    for i, (pred_class, proba) in enumerate(zip(preds, probas)):
        alert = ALERT_MAP[pred_class]
        results.append({
            "index":    i,
            "alert":    alert,
            "alert_code": pred_class,
            "confidence": round(float(proba[pred_class]) * 100, 1),
            "probabilities": {
                "green":  round(proba[0]*100,2), "yellow": round(proba[1]*100,2),
                "orange": round(proba[2]*100,2), "red":    round(proba[3]*100,2),
            },
        })

    return jsonify({
        "total": len(results),
        "results": results,
        "summary": {
            k: sum(1 for r in results if r["alert"] == k)
            for k in ["green","yellow","orange","red"]
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
