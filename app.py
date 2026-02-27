import threading
import time
import schedule
import re
import os
from flask import Flask, render_template_string
from data_fetcher import get_stock_data
from indicators import calculate_indicators
from ai_engine import ai_decide
from mailer import send_email
from logger import log_signal
from database import init_db, insert_signal, fetch_signals

# Initialize DB
init_db()

app = Flask(__name__)

# =========================
# DASHBOARD TEMPLATE
# =========================
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

# =========================
# BACKGROUND AI ENGINE
# =========================

def run_agent():
    print("📊 Running market analysis...")

    stocks = get_stock_data()
    if not stocks:
        return

    for stock in stocks:
        indicators = calculate_indicators(stock["stock"])
        if not indicators:
            continue

        decision = ai_decide(stock, indicators)

        decision_match = re.search(r"Decision:\s*(BUY|SELL|HOLD)", decision)
        confidence_match = re.search(r"Confidence:\s*(\d+)", decision)

        decision_value = decision_match.group(1) if decision_match else "HOLD"
        confidence_value = int(confidence_match.group(1)) if confidence_match else 0

        insert_signal(
            stock['stock'],
            decision_value,
            confidence_value,
            stock['price']
        )

        message = f"{stock['stock']} → {decision_value} ({confidence_value}%)"
        log_signal(message)

        if decision_value in ["BUY", "SELL"]:
            send_email("🚨 AI Stock Alert", message)

    print("✅ Cycle completed.")


def scheduler_loop():
    schedule.every(60).minutes.do(run_agent)
    run_agent()

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print("Recovered:", e)
            time.sleep(5)

# Start background thread
threading.Thread(target=scheduler_loop, daemon=True).start()

# =========================
# RUN FLASK
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)