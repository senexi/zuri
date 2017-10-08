import json

with open('household_rating.json') as json_data:
    d = json_data.read()
print(d)
