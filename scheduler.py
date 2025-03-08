import json
import requests
from config import OPENROUTER_API_KEY, longitude, latitude

# Placeholder imports (these functions will be implemented by your teammates)
from parameters import get_summarized_weather
from resources.data.dataloader import load_business_data  # This will load JSON data

# 🤖 AI-Powered Schedule Generation
def generate_schedule():
    """Generates a weekly employee work schedule based on business data, weather, and events."""

    # 🏢 Load business data (JSON)
    business_data = load_business_data()

    # 🌦️ Get external factors (weather, events)
    weather_forecast = get_summarized_weather(latitude, longitude)  # Fetch summarized weather data for each shift

    # 📝 Format prompt for AI
    prompt = f"""
    You are an AI assistant creating a weekly employee work schedule for {business_data['business']['name']} in {business_data['business']['location']}.

    **Business Hours:** 
    {json.dumps(business_data['opening_hours'], indent=2)}

    **Weather Forecast (Shift-wise Summary):** 
    {json.dumps(weather_forecast, indent=2)}  # e.g., "Monday": {{"morning": {{"temp": 15, "precip": 0.0}}, "afternoon": {{...}}}}

    **Employees & Availability:** 
    {json.dumps(business_data['employees'], indent=2)}

    **Rules:** 
    - Assign shifts fairly based on availability and contract hours.
    - Prioritize extra staffing on busy days (good weather or big events).
    - Ensure compliance with working hours.

    Generate a detailed shift schedule for the upcoming week.
    """

    # 🔗 OpenRouter API Setup with requests
    url = "https://openrouter.ai/api/v1/chat/completions"  # Replace with the actual endpoint
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "google/gemini-2.0-flash-thinking-exp:free",  # Model name as per OpenRouter documentation
        "messages": [
            {
                "role": "user",  # 'user' role indicates a prompt from the user
                "content": prompt  # The question or message being asked
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

        # 💾 Save the generated schedule to a file
        with open("resources/data/schedule.json", "w") as f:
            json.dump({"schedule": data}, f, indent=2)

        return schedule
    else:
        # Handle errors (e.g., API call failure)
        print(f"Error: {response.status_code} - {response.text}")
        return None
