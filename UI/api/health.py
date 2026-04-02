from __future__ import annotations

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def health(path: str = ''):
    return jsonify({'status': 'ok', 'service': 'impact-predictor-api'})
