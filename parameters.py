# weather
# event (around the location)


import requests
import datetime


def get_weather_forecast(latitude, longitude):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        days = data["daily"]["time"]
        max_temps = data["daily"]["temperature_2m_max"]
        min_temps = data["daily"]["temperature_2m_min"]
        precipitation = data["daily"]["precipitation_sum"]

        print("7-Day Weather Forecast:")
        for i in range(len(days)):
            print(f"{days[i]}: Max {max_temps[i]}°C, Min {min_temps[i]}°C, Precipitation {precipitation[i]}mm")
    else:
        print("Failed to fetch weather data.")


# Example usage: Antwerp, Belgium
get_weather_forecast(51.2194, 4.4025)
