import requests

def get_usdidr():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    data = requests.get(url).json()
    return data["rates"]["IDR"]