from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Any
from functools import wraps

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

FEATURES = ["magnitude", "depth", "cdi", "mmi", "sig", "depth_mag_ratio"]
LABEL_MAP = {0: "green", 1: "yellow", 2: "orange", 3: "red"}
SEVERITY_WEIGHTS = {"green": 25, "yellow": 50, "orange": 75, "red": 100}
MODEL_PATH = os.path.join("saved_models", "gb_custom.pkl")

# Validation ranges tuned for practical earthquake-reporting bounds.
BOUNDS = {
    "magnitude": (0.0, 10.0),
    "depth": (0.0, 700.0),
    "cdi": (0.0, 12.0),
    "mmi": (0.0, 12.0),
    "sig": (0.0, 1200.0),
}


@dataclass
class PredictionResult:
    predicted_class: str
    impact_score: float
    risk_level: str
    probabilities: dict[str, float]
    features_used: dict[str, float]
    target_color: str
    shake_class: str


def load_model() -> Any:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at '{MODEL_PATH}'. Run the advanced modeling notebook first."
        )
    return joblib.load(MODEL_PATH)


MODEL = load_model()
app = Flask(__name__)
app.secret_key = os.environ.get("IMPACT_APP_SECRET", "retro-impact-predictor-secret")


def login_required(view_func):
    @wraps(view_func)
    def _wrapped(*args, **kwargs):
        if not session.get("display_name"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return _wrapped


def _to_float(payload: dict[str, Any], key: str) -> float:
    value = payload.get(key, "")
    if value in (None, ""):
        raise ValueError(f"'{key}' is required")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"'{key}' must be numeric") from exc


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def sanitize_inputs(payload: dict[str, Any]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for key in ["magnitude", "depth", "cdi", "mmi", "sig"]:
        val = _to_float(payload, key)
        lo, hi = BOUNDS[key]
        cleaned[key] = _clamp(val, lo, hi)

    # Improvement: derive depth_mag_ratio to keep engineered feature consistent.
    denom = cleaned["magnitude"] if cleaned["magnitude"] > 0.01 else 0.01
    cleaned["depth_mag_ratio"] = cleaned["depth"] / denom
    return cleaned


def compute_prediction(cleaned: dict[str, float]) -> PredictionResult:
    x = np.array([[cleaned[f] for f in FEATURES]], dtype=float)
    x_df = pd.DataFrame(x, columns=FEATURES)

    pred_idx = int(MODEL.predict(x_df)[0])
    pred_class = LABEL_MAP[pred_idx]

    proba_arr = MODEL.predict_proba(x_df)[0]
    probabilities = {
        LABEL_MAP[i]: round(float(proba_arr[i]) * 100.0, 2) for i in range(len(proba_arr))
    }

    impact_score = round(
        sum((probabilities[label] / 100.0) * weight for label, weight in SEVERITY_WEIGHTS.items()),
        2,
    )

    if impact_score >= 80:
        risk_level = "Severe"
        shake_class = "shake-heavy"
    elif impact_score >= 60:
        risk_level = "High"
        shake_class = "shake-medium"
    elif impact_score >= 40:
        risk_level = "Moderate"
        shake_class = "shake-light"
    else:
        risk_level = "Low"
        shake_class = "shake-min"

    target_color_map = {
        "green": "#2e8b57",
        "yellow": "#f2c94c",
        "orange": "#f2994a",
        "red": "#d7263d",
    }

    return PredictionResult(
        predicted_class=pred_class,
        impact_score=impact_score,
        risk_level=risk_level,
        probabilities=probabilities,
        features_used={k: round(v, 4) for k, v in cleaned.items()},
        target_color=target_color_map[pred_class],
        shake_class=shake_class,
    )


@app.route("/", methods=["GET"])
def landing() -> str:
    return render_template("landing.html", user=session.get("display_name"))


@app.route("/login", methods=["GET", "POST"])
def login() -> Any:
    if request.method == "POST":
        name = (request.form.get("display_name") or "").strip()
        if not name:
            return render_template("login.html", error="Please enter a name."), 400

        # Basic login only: store display name in session with no password/auth check.
        session["display_name"] = name
        return redirect(url_for("predictor"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout() -> Any:
    session.pop("display_name", None)
    return redirect(url_for("landing"))


@app.route("/app", methods=["GET"])
@login_required
def predictor() -> str:
    return render_template("predictor.html", user=session.get("display_name"))


@app.route("/predict", methods=["POST"])
@login_required
def predict() -> Any:
    payload = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})

    try:
        cleaned = sanitize_inputs(payload)
        result = compute_prediction(cleaned)
    except ValueError as exc:
        message = str(exc)
        if request.is_json:
            return jsonify({"error": message}), 400
        return render_template(
            "predictor.html",
            error=message,
            values=payload,
            user=session.get("display_name"),
        ), 400

    if request.is_json:
        return jsonify(result.__dict__)

    return render_template(
        "predictor.html",
        result=result,
        values=payload,
        user=session.get("display_name"),
    )


def run_edge_case_tests() -> list[dict[str, Any]]:
    cases = [
        {
            "name": "Typical moderate event",
            "payload": {"magnitude": 5.8, "depth": 18, "cdi": 4.5, "mmi": 4.1, "sig": 420},
            "expect_ok": True,
        },
        {
            "name": "Very small event",
            "payload": {"magnitude": 0.2, "depth": 2, "cdi": 0.1, "mmi": 0.1, "sig": 5},
            "expect_ok": True,
        },
        {
            "name": "Extreme values (clamped)",
            "payload": {"magnitude": 11, "depth": 999, "cdi": 15, "mmi": 15, "sig": 2500},
            "expect_ok": True,
        },
        {
            "name": "Zero magnitude fallback",
            "payload": {"magnitude": 0, "depth": 50, "cdi": 3, "mmi": 3, "sig": 150},
            "expect_ok": True,
        },
        {
            "name": "Missing field",
            "payload": {"magnitude": 5.0, "depth": 20, "cdi": 3, "mmi": 3},
            "expect_ok": False,
        },
        {
            "name": "Non-numeric input",
            "payload": {"magnitude": "bad", "depth": 20, "cdi": 3, "mmi": 3, "sig": 200},
            "expect_ok": False,
        },
    ]

    results: list[dict[str, Any]] = []
    for case in cases:
        ok = True
        details = "pass"
        try:
            cleaned = sanitize_inputs(case["payload"])
            pred = compute_prediction(cleaned)
            if not (0 <= pred.impact_score <= 100):
                ok = False
                details = "impact score out of range"
        except Exception as exc:  # noqa: BLE001
            ok = False
            details = str(exc)

        passed = ok if case["expect_ok"] else (not ok)
        results.append({
            "name": case["name"],
            "expected_success": case["expect_ok"],
            "passed": passed,
            "details": details,
        })

    return results


@app.route("/tests", methods=["GET"])
def tests() -> Any:
    results = run_edge_case_tests()
    return jsonify({"results": results, "passed": all(r["passed"] for r in results)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Week 6+7 Impact Predictor UI")
    parser.add_argument("--run-tests", action="store_true", help="Run edge-case tests and exit")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.run_tests:
        results = run_edge_case_tests()
        for item in results:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"[{status}] {item['name']}: {item['details']}")
        print(f"\nOverall: {'PASS' if all(x['passed'] for x in results) else 'FAIL'}")
        return

    app.run(debug=True, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
