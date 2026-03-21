import re
import requests
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        error = "Invalid credentials. Please contact your IT Administrator or check your SSO configuration."
    return render_template('login.html', error=error)


@app.route("/docs")
def docs():
    return render_template('docs.html')


@app.route("/demo", methods=["GET", "POST"])
def demo():
    result = None
    if request.method == "POST":
        url = request.form.get("url", "")

        if re.search(r"(127\.0\.0\.1|localhost|0\.0\.0\.0|::1|@)", url, re.IGNORECASE):
            result = {
                "type": "warning",
                "title": "Security Violation Detected",
                "body": "Access to loopback or internal addresses is strictly prohibited by PhishGuard WAF."
            }
        else:
            try:
                resp = requests.get(url, timeout=3)
                result = {
                    "type": "success",
                    "title": f"Analysis Complete (HTTP {resp.status_code})",
                    "body": resp.text[:1500]
                }
            except Exception as e:
                result = {
                    "type": "error",
                    "title": "Analysis Failed",
                    "body": f"Target is unreachable, timed out, or connection was refused."
                }

    return render_template('demo.html', result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)