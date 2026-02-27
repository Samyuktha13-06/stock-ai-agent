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
    <meta http-equiv="refresh" content="60">
    <style>
        body { font-family: Arial; background-color: #111; color: #eee; }
        table { border-collapse: collapse; width: 95%; margin: 20px auto; }
        th, td { border: 1px solid #444; padding: 10px; text-align: center; }
        th { background-color: #222; }
        tr:nth-child(even) { background-color: #1a1a1a; }
        h1 { text-align: center; }
        .buy { color: #00ff88; font-weight: bold; }
        .sell { color: #ff4d4d; font-weight: bold; }
        .hold { color: #ffaa00; font-weight: bold; }
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
            <th>Timestamp (IST)</th>
        </tr>
        {% for row in signals %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td class="{{ row[2]|lower }}">{{ row[2] }}</td>
            <td>{{ row[3] }}%</td>
            <td>{{ row[4] }}</td>
            <td>{{ row[5] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# =========================
# DASHBOARD ROUTE
# =========================
@app.route("/")
def home():
    signals = fetch_signals()
    return render_template_string(HTML_TEMPLATE, signals=signals)


# =========================
# AGENT EXECUTION ROUTE
# =========================
@app.route("/run")
def run_now():
    run_agent()
    return "Agent executed successfully."


# =========================
# MAIN AI LOGIC
# =========================
def run_agent():
    print("📊 Running market analysis...")

    stocks = get_stock_data()
    if not stocks:
        return

    alert_messages = []   # collect BUY/SELL alerts

    for stock in stocks:
        indicators = calculate_indicators(stock["stock"])
        if not indicators:
            continue

        ai_result = ai_decide(stock, indicators)

        decision_value = ai_result.get("decision", "HOLD")
        confidence_value = int(ai_result.get("confidence", 0))
        reason = ai_result.get("reason", "")

        insert_signal(
            stock['stock'],
            decision_value,
            confidence_value,
            stock['price']
        )

        message = f"""
Stock: {stock['stock']}
Price: {stock['price']}
Change: {stock['change']}%
Volume: {stock['volume']}

Trend: {indicators['trend']}
Volatility: {indicators['volatility']}
Strength: {indicators['strength']}

Decision: {decision_value}
Confidence: {confidence_value}%
Reason: {reason}

=================================
"""

        log_signal(message)

        # Collect alerts instead of sending immediately
        if decision_value in ["BUY", "SELL"]:
            alert_messages.append(message)

    # Send ONE combined email
    if alert_messages:
        combined_message = "\n\n".join(alert_messages)
        try:
            send_email("🚨 AI Stock Alerts (Combined)", combined_message)
            print("Combined email sent.")
        except Exception as e:
            print("Email failed:", e)

    print("✅ Cycle completed.")


# =========================
# RUN FLASK
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)