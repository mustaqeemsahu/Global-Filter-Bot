import json

def load_filters():
    try:
        with open("filters.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_filters(data):
    with open("filters.json", "w") as f:
        json.dump(data, f, indent=4)
