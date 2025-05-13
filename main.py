import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://letterboxd.com/sign-in/"
DATA_URL = "https://letterboxd.com/settings/data/"

USERNAME = "your_username"
PASSWORD = "your_password"

with requests.Session() as s:
    # 1. Get login page for CSRF token
    resp = s.get(LOGIN_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf"})["value"]

    # 2. Post login form
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "csrf": csrf_token,
        "remember": "on"
    }
    s.post(LOGIN_URL, data=payload)

    # 3. Go to data export page
    resp = s.get(DATA_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Find the export form/button and any required tokens

    # 4. Trigger export (may require another POST)
    # Example: s.post(EXPORT_URL, data=export_payload)
    # Download the file

    # Save the file
    with open("letterboxd_data.zip", "wb") as f:
        f.write(resp.content)