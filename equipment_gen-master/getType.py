
import json

with open('static/json/col_exceptions.json') as f:
    data = json.load(f)
print("Col exceptions:",str(data))
# return str(data)

    