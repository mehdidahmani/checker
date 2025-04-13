import requests
from bs4 import BeautifulSoup
import time
import traceback

# CONFIGURATION
RESEND_API_KEY = "re_79eFqCZv_fUWSeebAwqFfCGJW6ozYmp8S"
TO_EMAIL = "mehdidahmani2003@gmail.com"
FROM_EMAIL = "Agropraktika <onboarding@resend.dev>"

def check_vacancies():
    try:
        url = "https://agropraktika.eu/vacancies"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"❌ Failed to fetch page. Status code: {response.status_code}")
            return False

        soup = BeautifulSoup(response.text, "html.parser")
        vacancies_list = soup.find("ul", class_="vacancies-list")

        if vacancies_list and vacancies_list.find_all("li"):
            print("✅ Vacancies found!")
            return True
        else:
            print("❌ No vacancies available.")
            return False
    except Exception as e:
        print("⚠️ Error while checking vacancies:")
        traceback.print_exc()
        return False

def send_email():
    try:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "from": FROM_EMAIL,
            "to": [TO_EMAIL],
            "subject": "📢 New Vacancies Available on Agropraktika!",
            "html": """
                <h2>🚀 Hello Mehdi!</h2>
                <p>New internship or work opportunities have just been posted on <a href='https://agropraktika.eu/vacancies'>Agropraktika</a>.</p>
                <p>Check them out ASAP!</p>
                <br>
                <small>This is an automated alert from your vacancy watcher script.</small>
            """
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)

        if response.status_code == 200:
            print("📩 Email sent successfully.")
        else:
            print(f"❌ Failed to send email. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print("⚠️ Error while sending email:")
        traceback.print_exc()

print("🌀 Vacancy watcher started. Checking every 5 seconds...\n")

while True:
    try:
        if check_vacancies():
            send_email()
        time.sleep(5)
    except KeyboardInterrupt:
        print("🛑 Script manually stopped by user.")
        break
    except Exception as e:
        print("🚨 Unexpected error in main loop:")
        traceback.print_exc()
        time.sleep(10)  # delay before next try to avoid hammering if something is broken
