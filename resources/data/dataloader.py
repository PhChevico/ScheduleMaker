import json
import pandas as pd
from tabulate import tabulate


def visualize_json(json_data):
    # Business Info Table
    business_info = pd.DataFrame([json_data['business']])
    print("\nBusiness Information:")
    print(tabulate(business_info, headers='keys', tablefmt='grid'))

    # Opening Hours Table
    opening_hours = pd.DataFrame(json_data['opening_hours'])
    print("\nOpening Hours:")
    print(tabulate(opening_hours, headers='keys', tablefmt='grid'))

    # Shifts Table
    shifts = pd.DataFrame(json_data['shifts'])
    print("\nShifts:")
    print(tabulate(shifts, headers='keys', tablefmt='grid'))

    # Employees Table
    employees_list = []
    for name, details in json_data['employees'].items():
        for availability in details['availability']:
            employees_list.append({
                "Name": name,
                "Role": details['role'],
                "Contract Hours": details['contract_hours'],
                "Day": availability['day'],
                "Time": availability['time']
            })

    employees_df = pd.DataFrame(employees_list)
    print("\nEmployees:")
    print(tabulate(employees_df, headers='keys', tablefmt='grid'))

#Use this to load the json file
with open("./resources/data/data.json", 'r') as file:
     json_data = json.load(file)

# visualize_json(json_data)

def load_business_data():
    with open("./resources/data/data.json", "r") as fileData:
        return json.load(fileData)