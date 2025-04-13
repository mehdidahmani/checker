import requests
from bs4 import BeautifulSoup
import time
import traceback

# CONFIGURATION
RESEND_API_KEY = "re_79eFqCZv_fUWSeebAwqFfCGJW6ozYmp8S"
TO_EMAIL = "mehdidahmani2003@gmail.com"
FROM_EMAIL = "Agropraktika <onboarding@resend.dev>"

# COOKIES TO INCLUDE IN THE REQUEST
COOKIES = {
    "XSRF-TOKEN": "eyJpdiI6IjV3TDYvOXMwUWhUR0NoNUxJZ1JBd2c9PSIsInZhbHVlIjoid..."
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}


def check_vacancies():
    try:
        url = "https://agropraktika.eu/vacancies"
        response = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=10)

        if response.status_code != 200:
            print(f"❌ Failed to fetch page. Status code: {response.status_code}")
            return False

        soup = BeautifulSoup(response.text, "html.parser")

        # Save a debug dump of the HTML in Railway (for troubleshooting)
        with open("dump.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        vacancies_list = soup.find("ul", class_="vacancies-list")

        if vacancies_list:
            vacancies = vacancies_list.find_all("li")
            if vacancies:
                print(f"✅ {len(vacancies)} vacancy(ies) found!")
                for i, vacancy in enumerate(vacancies, 1):
                    title = vacancy.find("h4")
                    if title:
                        print(f"  {i}. {title.text.strip()}")
                        print(vacancy)
                return True
            else:
                print("❌ No vacancies found in <ul> list.")
        else:
            print("❌ 'vacancies-list' not found.")
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
        time.sleep(5)
