import re
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>PhishGuard Enterprise</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-dark bg-dark text-white p-3">
    <div class="container">
        <h4> &#128737; PhishGuard Enterprise</h4>
        <div>
            <a href="/login" class="text-white me-3">Login</a>
            <a href="/docs" class="text-white me-3">Docs</a>
            <a href="/demo" class="btn btn-primary">Free Demo</a>
        </div>
    </div>
</nav>
<div class="container mt-5">
    {{ content|safe }}
</div>
</body>
</html>
"""


@app.route("/")
def index():
    content = "<h1>Защитите бизнес от APT-атак</h1><p>Наш ИИ-движок анализирует фишинг за миллисекунды.</p>"
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route("/login")
def login():
    content = """
    <h3>Login to Dashboard</h3>
    <form>
        <input type="text" class="form-control mb-2" placeholder="Username">
        <input type="password" class="form-control mb-2" placeholder="Password">
        <button class="btn btn-dark">Log In</button>
    </form>
    """
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route("/docs")
def docs():
    content = """
    <h3>API Documentation</h3>
    <p>Обратите внимание: Внутренний движок (v2) работает на порту 5000 и недоступен из внешней сети (Strict Firewall Rules).</p>
    """
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route("/demo", methods=["GET", "POST"])
def demo():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")

        if re.search(r"(127\.0\.0\.1|localhost|0\.0\.0\.0|::1|@)", url, re.IGNORECASE):
            result = '<div class="alert alert-danger">[Security Violation] Access to loopback addresses is strictly prohibited by PhishGuard WAF!</div>'
        else:
            try:
                resp = requests.get(url, timeout=3)
                result = f'<div class="alert alert-success"><b>Response ({resp.status_code}):</b><br><pre>{resp.text[:500]}</pre></div>'
            except Exception as e:
                result = f'<div class="alert alert-warning">Failed to fetch URL.</div>'

    form = """
    <h3>Demo: URL Analyzer</h3>
    <p>Введите URL для безопасного предпросмотра:</p>
    <form method="POST">
        <input type="text" name="url" class="form-control mb-2" placeholder="http://example.com">
        <button class="btn btn-primary">Analyze</button>
    </form>
    <hr>
    """
    return render_template_string(HTML_TEMPLATE, content=form + result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)