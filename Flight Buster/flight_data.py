import datetime
from pprint import pprint


class FlightData:
    def __init__(self, loc: dict):
        self.today = datetime.datetime.now()
        self.stay_time = {"from": 7, "to": 28}
        self.return_home_time = None

        self.flight_type = "round"
        self.stopovers = 0
        self.stopovers_via_city = None

        self.lowest_price = None
        self.price_threshhold = loc.get("lowestPrice")
        self.currency = "GBP"

        self.destination = loc.get("iataCode")
        self.arrival_city_name = None
        self.arrival_airport = None

        self.departure_airport = None
        self.departure_time = None
        self.departure_city_name = "London"
        self.departure_date_range = self.__departure_times()
        self.departure_from = "LON"

    def __departure_times(self):
        tommorow_date = (self.today + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
        after6_monthes_date = (self.today + datetime.timedelta(days=180)).strftime("%d/%m/%Y")
        return {"from": tommorow_date, "to": after6_monthes_date}

    def debug_all(self):
        pprint(vars(self))
