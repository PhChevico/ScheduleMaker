import json
import requests
from config import OPENROUTER_API_KEY, LONGITUDE, LATITUDE
from parameters import get_summarized_weather
from resources.data.dataloader import load_business_data

SCHEDULE_FILE = "resources/data/schedule.json"

def generate_schedule(additional_prompt=""):
    """Generates a weekly employee work schedule based on business data, weather, and events."""

    # 🏢 Load business data
    business_data = load_business_data()

    # 🌦️ Get external factors (weather, events)
    weather_forecast = get_summarized_weather(LATITUDE, LONGITUDE)

    # 📝 Format the base prompt
    base_prompt = f"""
    Please forget anything you have been told up until now.
    You are an AI assistant creating a weekly employee work schedule for {business_data['business']['name']} in {business_data['business']['location']}.

    **Business Hours:** 
    {json.dumps(business_data['opening_hours'], indent=2)}

    **Weather Forecast (Shift-wise Summary):** 
    {json.dumps(weather_forecast, indent=2)}  # e.g., "Monday": {{"morning": {{"temp": 15, "precip": 0.0}}, "afternoon": {{...}}}}

    **Employees & Availability:** 
    {json.dumps(business_data['employees'], indent=2)}

   Rules:

Each employee has individual contract hours. Ensure the total hours each employee works are as close as possible to their contract hours, but do not over-schedule any employee.
Assign employees based on their availability. Some employees may be available for certain shifts more than others.
The number of employees assigned to each shift may vary based on:
Employee availability
The weather forecast (e.g., higher demand on cold/rainy days might require more employees)
Business needs (based on opening hours and traffic/expected demand)

Distribute the shifts fairly, ensuring that no employee is overburdened or underutilized. Some shifts may require fewer employees, while others may need more.
Every shift requires at least one chef and two waiters.
If an employee has a preference for certain shifts, consider that in the scheduling if possible, but prioritize fairness and contract hours.
Generate a detailed shift schedule for the upcoming week, with the following format:

Shift Schedule

The columns should represent the days of the week (Monday, Tuesday, Wednesday, etc.).
The rows should represent the shift times (Morning, Afternoon, Evening).
For each shift, list the employees assigned to that shift. The number of employees per shift can vary based on business needs and availability, but try to match the number of employees to the business's expected requirements.
Please only output the schedule in markdown, do not include any other text.
    """

    # 🏗️ Combine base prompt with additional user input
    combined_prompt = f"{base_prompt}\n\n{additional_prompt}".strip()

    # 🔗 OpenRouter API Setup with requests
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "google/gemini-2.0-flash-thinking-exp:free",
        "messages": [
            {
                "role": "user",
                "content": combined_prompt
            }
        ]
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the generated schedule
        schedule = data["choices"][0]["message"]

        # 💾 Save the new schedule
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump({"schedule": data}, f, indent=2)

        return schedule
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
