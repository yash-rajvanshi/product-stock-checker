import requests
from bs4 import BeautifulSoup
import time
import smtplib
import os
import telegram

# ---- CONFIGURATION ----
URL = "https://hmtwatches.in/product_details?id=eyJpdiI6IjFQZ2Y0T2pQZ3Mvc1Q3RHY4YVVqaWc9PSIsInZhbHVlIjoiVmVRajRoOW4venBwNXJUWHpKU2l0UT09IiwibWFjIjoiNmQwOWI1YmZjYjc4ZDlkM2MxMGJiOGI4OTI1ZDY5ZGY4NWM1MGFmOTE3ODE0YjNiYmZiNjIzZmRiMzEwYzg2MiIsInRhZyI6IiJ9"
CHECK_INTERVAL = 300  # seconds
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ---- NOTIFY FUNCTIONS ----

def send_email(subject, message):
    sender_email = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, EMAIL_RECEIVER, f"Subject: {subject}\n\n{message}")
        print("✅ Email sent.")
    except Exception as e:
        print("Email error:", e)

def send_telegram(message):
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("✅ Telegram message sent.")
    except Exception as e:
        print("Telegram error:", e)

# ---- MAIN CHECK FUNCTION ----

def check_stock():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        strong_tags = soup.find_all("strong")

        for tag in strong_tags:
            if "out of stock" in tag.get_text(strip=True).lower():
                print("❌ Still out of stock.")
                return False

        # In stock
        notify_message = f"🎉 Product is back in stock!\n\nURL: {URL}"
        send_email("🕒 HMT Watch In Stock!", notify_message)
        send_telegram(notify_message)
        return True

    except Exception as e:
        print("Error:", e)
        return False

# ---- MAIN LOOP ----

while True:
    print("🔄 Checking stock...")
    if check_stock():
        break
    time.sleep(CHECK_INTERVAL)
