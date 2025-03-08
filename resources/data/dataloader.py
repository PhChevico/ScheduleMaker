import json

def load_business_data():
    with open("./resources/data/data.json", "r") as fileData:
        return json.load(fileData)