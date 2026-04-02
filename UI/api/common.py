from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

FEATURES = ["magnitude", "depth", "cdi", "mmi", "sig", "depth_mag_ratio"]
LABEL_MAP = {0: "green", 1: "yellow", 2: "orange", 3: "red"}
SEVERITY_WEIGHTS = {"green": 25, "yellow": 50, "orange": 75, "red": 100}

BOUNDS = {
    "magnitude": (0.0, 10.0),
    "depth": (0.0, 700.0),
    "cdi": (0.0, 12.0),
    "mmi": (0.0, 12.0),
    "sig": (0.0, 1200.0),
}

# Vercel project root is repository root. This API lives under UI/api.
MODEL_PATH = Path(__file__).resolve().parents[2] / "saved_models" / "gb_custom.pkl"
_MODEL: Any | None = None


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
    global _MODEL
    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at '{MODEL_PATH}'")
        _MODEL = joblib.load(MODEL_PATH)
    return _MODEL


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

    denom = cleaned["magnitude"] if cleaned["magnitude"] > 0.01 else 0.01
    cleaned["depth_mag_ratio"] = cleaned["depth"] / denom
    return cleaned


def compute_prediction(cleaned: dict[str, float]) -> PredictionResult:
    model = load_model()

    x = np.array([[cleaned[f] for f in FEATURES]], dtype=float)
    x_df = pd.DataFrame(x, columns=FEATURES)

    pred_idx = int(model.predict(x_df)[0])
    pred_class = LABEL_MAP[pred_idx]

    proba_arr = model.predict_proba(x_df)[0]
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
        results.append(
            {
                "name": case["name"],
                "expected_success": case["expect_ok"],
                "passed": passed,
                "details": details,
            }
        )

    return results
