from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, request

sys.path.append(str(Path(__file__).resolve().parent))
from common import compute_prediction, sanitize_inputs

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def predict(path: str = ''):
    if request.method == 'OPTIONS':
        return ('', 204)

    if request.method == 'GET':
        return jsonify(
            {
                'message': 'Use POST /api/predict with JSON body containing magnitude, depth, cdi, mmi, sig'
            }
        )

    payload = request.get_json(silent=True) or {}

    try:
        cleaned = sanitize_inputs(payload)
        result = compute_prediction(cleaned)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        return jsonify({'error': f'Prediction failed: {exc}'}), 500

    return jsonify(result.__dict__)
