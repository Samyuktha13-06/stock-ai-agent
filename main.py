import schedule
import time
from data_fetcher import get_stock_data
from indicators import calculate_indicators
from ai_engine import ai_decide
from mailer import send_email
from logger import log_signal

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

        # log always
        log_signal(message)

        # send email only if BUY or SELL
        if "BUY" in decision or "SELL" in decision:
            send_email("🚨 AI Stock Alert", message)

    print("\n✅ Cycle completed.\n")


# Run once immediately for testing
run_agent()

# Then run every 30 minutes automatically
schedule.every(30).minutes.do(run_agent)

while True:
    schedule.run_pending()
    time.sleep(1)