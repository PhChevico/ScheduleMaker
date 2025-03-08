import requests
from datetime import datetime

# Eventbrite API endpoint for searching events
url = 'https://www.eventbriteapi.com/v3/events/search/'

# Your API token (replace it with the actual token you have)
token = 'YKQNNXTB65HL5AQZTYGA'

# Headers with the authorization token
headers = {
    'Authorization': f'Bearer {token}'
}


# Function to fetch and display events by location and date
def fetch_events(date=None, city="Antwerp"):
    try:
        # Parameters for the event search (searching events in Antwerp)
        params = {
            'location.address': city,  # Search for events in Antwerp (or any city)
            'start_date.range_start': datetime.now().isoformat(),  # Start from the current date
            'sort_by': 'date',  # Sort by date
        }

        # Send the GET request to the Eventbrite API for events
        response = requests.get(url, headers=headers, params=params)
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

        # Parse the response
        data = response.json()

        if 'events' in data:
            events = data['events']

            # Filter events by date if provided
            if date:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                filtered_events = [event for event in events if
                                   datetime.strptime(event['start']['local'], '%Y-%m-%dT%H:%M:%S') == date_obj]
            else:
                filtered_events = events

            # Print events
            if filtered_events:
                for event in filtered_events:
                    event_name = event['name']['text']
                    event_date = event['start']['local']
                    event_location = event['venue']['name'] if event['venue'] else 'No venue specified'

                    print(f"Event Name: {event_name}")
                    print(f"Event Date: {event_date}")
                    print(f"Event Location: {event_location}")
                    print("-" * 30)
            else:
                print(f"No events found for the date: {date if date else 'all dates'}")
        else:
            print("Error: No events found in the response.")
            print("Response Data:", data)  # Print the response data if 'events' is not found.

    except Exception as e:
        print(f"Error fetching data: {e}")


# Example: Fetch events happening on a specific date (e.g., '2025-03-15')
fetch_events('2025-03-15')  # Change the date as needed

# Example: Fetch all events without a date filter
# fetch_events()
