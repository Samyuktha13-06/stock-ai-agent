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
    print("\n📊 Running market analysis...\n")

    stocks = get_stock_data()

    if not stocks:
        print("No stock data received.")
        return

    for stock in stocks:
        indicators = calculate_indicators(stock["stock"])

        if not indicators:
            continue

        decision = ai_decide(stock, indicators)

        # --- Parse Decision ---
        decision_match = re.search(r"Decision:\s*(BUY|SELL|HOLD)", decision)
        confidence_match = re.search(r"Confidence:\s*(\d+)", decision)

        decision_value = decision_match.group(1) if decision_match else "HOLD"
        confidence_value = int(confidence_match.group(1)) if confidence_match else 0

        # --- Store in Database ---
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

AI RESULT:
{decision}
=================================
"""

        print(message)

        log_signal(message)

        if decision_value in ["BUY", "SELL"]:
            send_email("🚨 AI Stock Alert", message)

    print("\n✅ Cycle completed.\n")


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