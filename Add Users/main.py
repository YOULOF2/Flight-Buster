import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEET_ENDPOINT = os.getenv("USERS_SHEET_ENDPOINT")

first_name = input("What is your first name? ").strip()
last_name = input("What is your last name? ").strip()
email = input("What is your email? ").strip()

sheet_data_response = requests.get(SHEET_ENDPOINT)
sheet_data_response.raise_for_status()

if email not in [row.get("email") for row in sheet_data_response.json().get("users")]:
    payload = \
        {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
    requests.post(url=SHEET_ENDPOINT, json=payload)
else:
    print("Already registered")
