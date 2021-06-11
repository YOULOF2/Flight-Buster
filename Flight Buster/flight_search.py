from dotenv import load_dotenv
import os
import requests
from flight_data import FlightData

load_dotenv()


class FlightSearch:
    def __init__(self):
        self.flight_query_endpoint = os.getenv("FLIGHT_QUERY_ENDPOINT")
        self.flight_search_endpoint = os.getenv("FLIGHT_SEARCH_ENDPOINT")
        self.api_key = os.getenv("TEQUILA_API_KEY")

    def __flight_search(self, flight: FlightData):
        parameters = {
            "fly_from": flight.departure_from,
            "fly_to": flight.destination,
            "date_from": flight.departure_date_range.get("from"),
            "date_to": flight.departure_date_range.get("to"),
            "nights_in_dst_from": flight.stay_time.get("from"),
            "nights_in_dst_to": flight.stay_time.get("to"),
            "flight_type": flight.flight_type,
            "max_stopovers": flight.stopovers,
            "curr": flight.currency
        }
        response = requests.get(url=self.flight_search_endpoint, params=parameters,
                                headers={"apikey": self.api_key})
        response.raise_for_status()
        return response

    def iata_code(self, city: str) -> str:
        print(f"Finding Iata Code for {city}")
        parameters = {"term": city}
        response = requests.get(self.flight_query_endpoint, params=parameters, headers={"apikey": self.api_key})
        response.raise_for_status()
        iata_code = response.json().get("locations")[0].get("code")
        return iata_code

    def flight_search(self, city) -> FlightData:
        def redo_search():
            flight.stopovers += 1
            json_d = self.__flight_search(flight).json()
            while not json_d.get("data"):
                print(f"Researching for {flight.destination}")
                flight.stopovers += 1
                json_d = self.__flight_search(flight).json()
            return json_d

        print(f"Searching for flights to {city.get('city')}")
        flight = FlightData(city)
        response = self.__flight_search(flight)
        json_data = response.json()

        try:
            json_data.get("data")[0]
        except IndexError:
            json_data = redo_search()
            flight.stopovers_via_city = json_data.get("data")[0].get("route")[0].get("cityTo")

        flight.lowest_price = json_data.get("data")[0].get("price")

        flight.departure_airport = json_data.get("data")[0].get("flyFrom")

        flight.arrival_airport = json_data.get("data")[0].get("flyTo")
        flight.arrival_city_name = city.get("city")

        flight.departure_time = json_data.get("data")[0].get("route")[0].get("utc_departure").split("T")[0]
        flight.return_home_time = json_data.get("data")[0].get("route")[-1].get("utc_departure").split("T")[0]

        return flight
