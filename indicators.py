import yfinance as yf

def calculate_indicators(stock):
    try:
        data = yf.Ticker(stock).history(period="5d", interval="15m")

        if data.empty:
            return None

        # moving average
        sma20 = data["Close"].rolling(window=20).mean().iloc[-1]

        latest_price = data["Close"].iloc[-1]

        # trend detection
        trend = "UPTREND" if latest_price > sma20 else "DOWNTREND"

        # volatility
        volatility = data["Close"].pct_change().std() * 100

        # strength score
        strength = abs(latest_price - sma20)

        return {
            "trend": trend,
            "sma20": round(float(sma20),2),
            "volatility": round(float(volatility),2),
            "strength": round(float(strength),2)
        }

    except Exception as e:
        print(f"Indicator error for {stock}: {e}")
        return None