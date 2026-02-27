import yfinance as yf

WATCHLIST = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS"
]

def get_stock_data():
    results = []

    for stock in WATCHLIST:
        try:
            data = yf.Ticker(stock).history(period="1d", interval="5m")

            if data.empty:
                continue

            price = float(data["Close"].iloc[-1])
            open_price = float(data["Open"].iloc[0])
            volume = int(data["Volume"].iloc[-1])

            change = ((price - open_price) / open_price) * 100 if open_price and open_price != 0 else 0

            results.append({
                "stock": stock,
                "price": round(price, 2),
                "change": round(change, 2),
                "volume": volume
            })

        except Exception as e:
            print(f"Skipping {stock}: {e}")

    return results