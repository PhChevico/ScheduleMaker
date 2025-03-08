import json
import openai
from openai import OpenAI
from config import OPENROUTER_API_KEY, longitude, latitude

# Placeholder imports (these functions will be implemented by your teammates)
from parameters import get_summarized_weather
from resources.data.dataloader import load_business_data  # This will load JSON data

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # URL for OpenRouter API
    api_key=OPENROUTER_API_KEY,  # Replace with your OpenRouter API key
)


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

    # 🔗 OpenRouter API Setup
    openai.api_key = OPENROUTER_API_KEY

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-zero:free",  # Model name as per OpenRouter documentation
        messages=[  # The messages the AI will respond to
            {
                "role": "user",  # 'user' role indicates a prompt from the user
                "content": prompt  # The question or message being asked
            }
        ]
    )


    # Extract the generated schedule
    schedule = response["choices"][0]["message"]["content"].strip()

    # 💾 Save the generated schedule to a file
    with open("data/schedule.json", "w") as f:
        json.dump({"schedule": schedule}, f, indent=2)

    return schedule
