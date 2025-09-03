import requests
import json
API_KEY = ""
SEARCH_ENGINE_ID = ""
query = '''("data engineer" OR "ML engineer") AND ("python" OR "tensorflow") AND ("San Francisco" OR "California") AND ("Google" OR "Meta") AND (gmail OR "@gmail.com" OR "@outlook.com") AND (phone OR "contact" OR "mobile") -intitle:"profiles" -inurl:"dir/" site:linkedin.com/in/ OR site:linkedin.com/pub/'''

url = f"https://www.googleapis.com/customsearch/v1"
params = {
    "key": API_KEY,
    "cx": SEARCH_ENGINE_ID,
    "q": query
}

response = requests.get(url, params=params)

results = response.json()
with open('data.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)
print(results)


