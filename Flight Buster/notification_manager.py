from dotenv import load_dotenv
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flight_data import FlightData

load_dotenv()


class NotificationManager:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.reciever_email = "youlof123@gmail.com"

        self.message = MIMEMultipart("alternative")
        self.message["subject"] = "Low Price Alert!"
        self.message["From"] = self.sender_email
        self.message["To"] = self.reciever_email

    def send_email(self, flight: FlightData, emails: list) -> None:
        print(f"Sending HTML email for flight to {flight.destination}")

        link = f"https://www.google.co.uk/flights?hl=en#flt=" \
               f"{flight.departure_airport}.{flight.arrival_airport}.{flight.departure_time}" \
               f"*{flight.arrival_airport}.{flight.departure_airport}.{flight.return_home_time}"

        if flight.stopovers > 0:
            text = f"Low Price alert!\n" \
                   f"Only £{flight.lowest_price} to fly from {flight.departure_city_name}-{flight.departure_airport}\n" \
                   f"to {flight.arrival_city_name}-{flight.arrival_airport}\n" \
                   f"from {flight.departure_time} to {flight.return_home_time}\n" \
                   f"Transit via {flight.stopovers_via_city} city\n" \
                   f"{link}"

            html = \
                f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                </head>
                <body style=""><h1><em>Low Price Alert</em></h1><br>
                <hr>
                <h2>Only £{flight.lowest_price}
                    to fly from {flight.departure_city_name}-{flight.departure_airport}
                    <br>
                    to {flight.arrival_city_name}-{flight.arrival_airport}
                    <br>
                    from {flight.departure_time} to {flight.return_home_time}</h2>
                    <h3>Transit via {flight.stopovers_via_city} city</h3>
                    <br>
                    <a href="{link}">Click here to book trip</a>
                </body>
                </html>"""
        else:
            text = f"Low Price alert!\n" \
                   f"Only £{flight.lowest_price} to fly from {flight.departure_city_name}-{flight.departure_airport}\n" \
                   f"to {flight.arrival_city_name}-{flight.arrival_airport}\n" \
                   f"from {flight.departure_time} to {flight.return_home_time}\n" \
                   f"{link}"

            html = \
                f"""<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                            </head>
                            <body style=""><h1><em>Low Price Alert</em></h1><br>
                            <hr>
                            <h2>Only £{flight.lowest_price}
                                to fly from {flight.departure_city_name}-{flight.departure_airport}
                                <br>
                                to {flight.arrival_city_name}-{flight.arrival_airport}
                                <br>
                                from {flight.departure_time} to {flight.return_home_time}</h2>
                                <br>
                                <a href="{link}">Click here to book trip</a>
                            </body>
                            </html>"""

        text_part = MIMEText(text, "plain")
        html_part = MIMEText(html, "html")

        self.message.attach(text_part)
        self.message.attach(html_part)

        context = ssl.create_default_context()
        for email in emails:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(
                    self.sender_email, email, self.message.as_string()
                )
