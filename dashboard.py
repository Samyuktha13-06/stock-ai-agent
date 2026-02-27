from flask import Flask, render_template_string
from database import fetch_signals

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Stock Dashboard</title>
    <style>
        body { font-family: Arial; background-color: #111; color: #eee; }
        table { border-collapse: collapse; width: 90%; margin: 20px auto; }
        th, td { border: 1px solid #444; padding: 10px; text-align: center; }
        th { background-color: #222; }
        tr:nth-child(even) { background-color: #1a1a1a; }
        h1 { text-align: center; }
    </style>
</head>
<body>
    <h1>📊 AI Stock Signals Dashboard</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Stock</th>
            <th>Decision</th>
            <th>Confidence</th>
            <th>Price</th>
            <th>Timestamp</th>
        </tr>
        {% for row in signals %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}%</td>
            <td>{{ row[4] }}</td>
            <td>{{ row[5] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def home():
    signals = fetch_signals()
    return render_template_string(HTML_TEMPLATE, signals=signals)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)