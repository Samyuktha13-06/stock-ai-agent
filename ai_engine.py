import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# initialize groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_decide(stock_data, indicators):

    prompt = f"""
You are a professional Indian stock market analyst.

Analyze the stock using given data.

Stock: {stock_data['stock']}
Current Price: {stock_data['price']}
Daily Change: {stock_data['change']}%
Volume: {stock_data['volume']}

Trend: {indicators['trend']}
Volatility: {indicators['volatility']}
Strength vs SMA: {indicators['strength']}

Give output in EXACT format:

Decision: BUY or SELL or HOLD
Confidence: number between 0-100
Reason: one line simple reason
"""

    try:
        chat = client.chat.completions.create(
           model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = chat.choices[0].message.content
        return reply

    except Exception as e:
        return f"AI error: {e}"