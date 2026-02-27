import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_decide(stock_data, indicators):

    prompt = f"""
You are a professional Indian stock market analyst.

Analyze the stock using the data below:

Stock: {stock_data['stock']}
Current Price: {stock_data['price']}
Daily Change: {stock_data['change']}%
Volume: {stock_data['volume']}

Trend: {indicators['trend']}
Volatility: {indicators['volatility']}
Strength vs SMA: {indicators['strength']}

Return ONLY valid JSON in this exact format:

{{
    "decision": "BUY or SELL or HOLD",
    "confidence": number between 0 and 100,
    "reason": "one short sentence explaining why"
}}

Do not include any extra text.
"""

    try:
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        reply = chat.choices[0].message.content.strip()

        # Try parsing JSON
        parsed = json.loads(reply)

        return parsed

    except Exception as e:
        print("AI error:", e)
        return {
            "decision": "HOLD",
            "confidence": 0,
            "reason": "AI parsing failed"
        }