import json
from pprint import pprint

with open("26_10_2024_12_16_451014170085216825547.json", "r") as f:
    data = json.load(f)


# for key, value in data.items():
#     print(f"{key}: {type(value)}")

pprint(data)
