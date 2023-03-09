import requests
import json

# URL to query
url = "https://api.opendota.com/api/heroes/1/matchups"

# Query the URL and get the JSON data
response = requests.get(url)
data = response.json()

# Process the data as needed
processed_data = {"processed_data": data}

# Write the processed data to a JSON file
with open("hero_data.json", "w") as outfile:
    json.dump(processed_data, outfile)
