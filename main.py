import schedule
import time
import re
from data_fetcher import get_stock_data
from indicators import calculate_indicators
from ai_engine import ai_decide
from mailer import send_email
from logger import log_signal
from database import init_db, insert_signal

init_db()

print("🚀 Autonomous Stock AI Agent Started...")

def run_agent():
    print("📊 Running market analysis...")

    stocks = get_stock_data()
    if not stocks:
        return

    alert_messages = []   # collect all BUY/SELL messages

    for stock in stocks:
        indicators = calculate_indicators(stock["stock"])
        if not indicators:
            continue

        ai_result = ai_decide(stock, indicators)

        decision_value = ai_result.get("decision", "HOLD")
        confidence_value = int(ai_result.get("confidence", 0))
        reason = ai_result.get("reason", "")

        # Insert into database
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

        # Collect only BUY/SELL alerts
        if decision_value in ["BUY", "SELL"]:
            alert_messages.append(message)

    # Send ONE combined email
    if alert_messages:
        combined_message = "\n\n".join(alert_messages)
        try:
            send_email("🚨 AI Stock Alerts (Combined)", combined_message)
        except Exception as e:
            print("Email failed:", e)

    print("✅ Cycle completed.")

# Run once immediately
run_agent()

# Run every 60 minutes (better for cloud stability)
schedule.every(60).minutes.do(run_agent)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"Main loop recovered: {e}")
        time.sleep(5)