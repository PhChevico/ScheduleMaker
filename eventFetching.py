import requests
from config import event_token

import requests

def get_events():
    base_url = "https://api.predicthq.com/v1/events/"
    access_token = event_token  # Make sure you define `event_token` before calling this method

    # Example query parameters based on your provided input
    params = {
        'active.gt': '2025-03-10',
        'active.lte': '2025-03-16',
        'active.tz': 'Europe/Brussels',
        'category': 'concerts,sports',
        'country': 'BE',
        'city': 'Antwerp',
        'limit': 100,
        'sort': 'start'
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send GET request with headers and query parameters
    response = requests.get(base_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        events = response.json()

        # Filter events with predicted attendance greater than 3500 and clean the data
        high_attendance_events = [
            {
                'title': event.get('title'),
                'start': event.get('start_local'),
                'venue': event.get('entities', [{}])[0].get('name', 'Unknown Venue'),
                'attendance': event.get('phq_attendance', 0),
                'category': event.get('category'),
                'labels': event.get('labels', []),
            }
            for event in events.get('results', [])
            if event.get('phq_attendance', 0) > 3500
        ]

        return high_attendance_events
    else:
        print(f"Failed to fetch events. Status code: {response.status_code}")
        return []



def print_events(events):
    if events:
        for event in events:
            event_name = event.get('title', 'No title')
            event_start = event.get('start_local', 'No start time')
            event_end = event.get('end_local', 'No end time')
            event_attendance = event.get('phq_attendance', 'No predicted attendance')

            print(f"Event: {event_name}")
            print(f"Start: {event_start}")
            print(f"End: {event_end}")
            print(f"Predicted Attendance: {event_attendance}")
            print("-" * 50)
    else:
        print("No events with high attendance found.")


if __name__ == "__main__":
    # Get the high attendance events
    # events = get_events()

    # Print them outside the method
    # print_events(events)
    print(get_events())