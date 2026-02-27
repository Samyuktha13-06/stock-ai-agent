import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
TO_EMAIL = os.getenv("EMAIL")  # your own email


def send_email(subject, body):
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": "AI Stock Agent <onboarding@resend.dev>",
        "to": [TO_EMAIL],
        "subject": subject,
        "text": body
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Email sent successfully.")
    else:
        print("Email failed:", response.text)