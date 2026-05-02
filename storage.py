import json

FILE = "storage.json"

def load_data():
    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {"last_price": None, "diff": 0}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)