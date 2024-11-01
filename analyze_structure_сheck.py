import json
from pprint import pprint

with open("26_10_2024_12_16_451014170085216825547.json", "r") as f:
    data = json.load(f)

# print(data[0]['ticket'])
print(type(data[0]))
for key, value in data[0].items():
    print(f"{key}: {type(value)}")

for key, value in data[0]['ticket']['document']['receipt'].items():
    print(f"{key}: {type(value)}")
# print(type(data))
# pprint(data)
