import requests
import json

url = "https://api.insurhack.com/gi/PolicyPeriod_Set/zde.actions.GetRating"
headers = {'KeyId': 'b4d1ee3b-3abf-41bb-97c7-80ba3a34fa87', 'Content-Type':'application/json'}

with open('liability_rating.json') as json_data:
	d = json_data.read()

print d
r = requests.post(url, headers=headers, data=d)

print r.text
