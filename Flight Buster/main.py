from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

datamanager = DataManager()
flightsearch = FlightSearch()
notificationmanager = NotificationManager()

sheet_data = datamanager.sheet_data()

for city in sheet_data.get("prices"):
    print("==============================================")
    if city.get("iataCode") == "":
        print("No IATA codes found.")
        iatacode = flightsearch.iata_code(city.get("city"))
        city["iataCode"] = iatacode
        datamanager.put_iatacode(city)
    flight = flightsearch.flight_search(city)
    if flight.lowest_price < flight.price_threshhold:
        print(f"Flight to {city.get('city')} found.")
        notificationmanager.send_email(flight, datamanager.user_emails())

