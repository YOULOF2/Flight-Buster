import requests
from dotenv import load_dotenv
import os

load_dotenv()


class DataManager:
    def __init__(self):
        self.prices_sheet_endpoint = os.getenv("PRICES_SHEET_ENDPOINT")
        self.users_sheet_endpoint = os.getenv("USERS_SHEET_ENDPOINT")

    def sheet_data(self) -> dict:
        print("GETing the sheet data from Sheety.")
        response = requests.get(self.prices_sheet_endpoint)
        response.raise_for_status()
        return response.json()

    def put_iatacode(self, city) -> None:
        print("PUTing the iataCodes into Sheety.")
        parameters = {
            "price": {
                "iataCode": city.get("iataCode")
            }
        }
        url = f"{self.prices_sheet_endpoint}/{city.get('id')}"
        response = requests.put(url=url, json=parameters)
        response.raise_for_status()

    def user_emails(self):
        response = requests.get(url=self.users_sheet_endpoint)
        return [row.get("email") for row in response.json().get("users")]
