from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify

sys.path.append(str(Path(__file__).resolve().parent))
from common import run_edge_case_tests

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def tests(path: str = ''):
    results = run_edge_case_tests()
    return jsonify({'results': results, 'passed': all(r['passed'] for r in results)})
