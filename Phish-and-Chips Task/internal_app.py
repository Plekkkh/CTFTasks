import os
import re
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Phish Analyzer v2.0 - INTERNAL USE ONLY</h1><p>Send suspicious URLs to /api/v2/analyze?target=&lt;url&gt;</p>"


@app.route("/api/v2/analyze")
def analyze():
    target = request.args.get("target", "")
    if not target:
        return jsonify({"error": "Target parameter required"}), 400

    if re.search(r"[;|&\n]", target):
        return jsonify({"error": "Security Violation: Invalid characters detected in target URL"}), 403

    report_id = uuid.uuid4().hex
    report_path = f"/var/www/html/reports/{report_id}.html"

    cmd = f'curl -sL "{target}" > {report_path}'
    os.system(cmd)

    return jsonify({
        "status": "success",
        "message": "Analysis complete. Report saved internally.",
        "report_id": report_id
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)