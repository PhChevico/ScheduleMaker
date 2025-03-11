# config.py

from dotenv import load_dotenv
import os

# Explicitly load the config.env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config.env'))

# Retrieve the values from the environment variables
LATITUDE = float(os.getenv("LATITUDE"))  # Default to 0.0 if not found
LONGITUDE = float(os.getenv("LONGITUDE"))  # Default to 0.0 if not found

BASE_URL_WEATHER = os.getenv("BASE_URL_WEATHER", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
EVENT_TOKEN = os.getenv("EVENT_TOKEN", "")

MY_EMAIL = os.getenv("MY_EMAIL", "")
MY_EMAIL_PASSWORD = os.getenv("MY_EMAIL_PASSWORD", "")
