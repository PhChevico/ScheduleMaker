import requests
import datetime
import json
from config import latitude, longitude, base_url_weather


# Function to read the functioning hours from the JSON file
def load_functioning_hours():
    try:
        with open("resources/data/data.json", "r") as file:
            data = json.load(file)
        return data["opening_hours"]
    except Exception as e:
        return []


def get_weather_forecast_by_hour(latitude_value, longitude_value):
    # Get today's date and day of the week
    today = datetime.date.today()

    # Calculate the date for the next Monday
    days_until_monday = (7 - today.weekday()) % 7  # Days until next Monday
    next_monday = today + datetime.timedelta(days=days_until_monday)
    next_sunday = next_monday + datetime.timedelta(days=6)

    # Format the dates as strings (YYYY-MM-DD)
    start_date = next_monday.strftime('%Y-%m-%d')
    end_date = next_sunday.strftime('%Y-%m-%d')

    # Load functioning hours
    functioning_hours = load_functioning_hours()

    if not functioning_hours:
        return {}

    # Get the day of the week for the next Monday
    current_day = today.strftime("%A")  # Get the day of the week (e.g., Monday)
    opening_time = None
    closing_time = None
    for day in functioning_hours:
        if day["day"] == current_day:
            opening_time = day["opening"]
            closing_time = day["closing"]
            break

    if not opening_time or not closing_time:
        return {}

    # Get the hourly forecast for the next Monday to Sunday period
    params = {
        "latitude": latitude_value,
        "longitude": longitude_value,
        "hourly": ["temperature_2m", "precipitation"],  # Removed 'time' as it's returned by default
        "timezone": "auto",
        "start_date": start_date,
        "end_date": end_date
    }

    # Log the request details


    try:
        response = requests.get(base_url_weather, params=params)

        # Log the status code and the response content
        if response.status_code != 200:
            return {}

        data = response.json()

        # Check if 'hourly' data exists
        if "hourly" not in data:
            return {}

        # Get the list of times, temperatures, and precipitation
        times = data["hourly"]["time"]
        temperatures = data["hourly"]["temperature_2m"]
        precipitations = data["hourly"]["precipitation"]

        weather_data = {}

        # Convert opening and closing times to 24-hour format
        opening_hour = int(opening_time.split(":")[0])
        closing_hour = int(closing_time.split(":")[0])

        # Loop through each day and check if the time is within operating hours
        for i in range(len(times)):
            # Extract the hour from the timestamp
            timestamp = times[i]
            hour = int(timestamp.split("T")[1].split(":")[0])

            # Check if the hour is within operating hours
            if opening_hour <= hour < closing_hour:
                # Add the weather data to a dictionary with timestamp as key
                weather_data[timestamp] = {
                    "temp": temperatures[i],
                    "precip": precipitations[i]
                }

        return weather_data

    except requests.exceptions.RequestException as e:
        return {}


# Example usage: Antwerp, Belgium
def get_summarized_weather(latitude_value, longitude_value):
    """Summarizes weather data into morning, afternoon, and evening shifts."""
    raw_weather_data = get_weather_forecast_by_hour(latitude_value, longitude_value)

    if not raw_weather_data:
        return {}

    summarized_weather = {}

    # Summarizing the data into morning, afternoon, and evening shifts
    for timestamp, data in raw_weather_data.items():
        # Example: 2025-03-08T10:00: Temp: 11.4°C, Precip: 0.0mm
        hour = int(timestamp.split("T")[1].split(":")[0])  # Get the hour (e.g., 10 for "2025-03-08T10:00")

        if hour < 12:  # Morning (6 AM to 12 PM)
            time_of_day = "morning"
        elif hour < 18:  # Afternoon (12 PM to 6 PM)
            time_of_day = "afternoon"
        else:  # Evening (6 PM to 12 AM)
            time_of_day = "evening"

        # Initialize dictionary for each day
        date = timestamp.split("T")[0]
        if date not in summarized_weather:
            summarized_weather[date] = {
                "morning": {"temp": 0, "precip": 0, "count": 0},
                "afternoon": {"temp": 0, "precip": 0, "count": 0},
                "evening": {"temp": 0, "precip": 0, "count": 0}
            }

        # Update the appropriate shift
        summarized_weather[date][time_of_day]["temp"] += data["temp"]
        summarized_weather[date][time_of_day]["precip"] += data["precip"]
        summarized_weather[date][time_of_day]["count"] += 1

    # Calculate averages for each shift
    for date, shifts in summarized_weather.items():
        for shift, values in shifts.items():
            if values["count"] > 0:
                summarized_weather[date][shift]["temp"] /= values["count"]
                summarized_weather[date][shift]["precip"] /= values["count"]

    return summarized_weather


# Example usage: Antwerp, Belgium
summary = get_summarized_weather(latitude, longitude)

