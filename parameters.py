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
        print(f"Error reading the functioning hours file: {e}")
        return []


# Function to get the hourly weather forecast for each opening hour
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
        print("No functioning hours available.")
        return

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
        print(f"Operating hours for {current_day} not found.")
        return

    # Get the hourly forecast for the next Monday to Sunday period
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude_value,
        "longitude": longitude_value,
        "hourly": ["temperature_2m", "precipitation"],  # Removed 'time' as it's returned by default
        "timezone": "auto",
        "start_date": start_date,
        "end_date": end_date
    }

    # Log the request details
    print(f"Requesting weather data for coordinates: {latitude_value}, {longitude_value}")
    print(f"API URL: {base_url}")
    print(f"Parameters: {params}")

    try:
        response = requests.get(base_url, params=params)

        # Log the status code and the response content
        print(f"API Response Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return

        data = response.json()

        # Check if 'hourly' data exists
        if "hourly" not in data:
            print("Error: 'hourly' data not found in the API response.")
            return

        # Get the list of times, temperatures, and precipitation
        times = data["hourly"]["time"]
        temperatures = data["hourly"]["temperature_2m"]
        precipitations = data["hourly"]["precipitation"]

        print(f"Weather forecast from {start_date} to {end_date} (only during operating hours):")

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
                print(f"{timestamp}: Temp: {temperatures[i]}°C, Precip: {precipitations[i]}mm")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


# Example usage: Antwerp, Belgium
get_weather_forecast_by_hour(latitude, longitude)
