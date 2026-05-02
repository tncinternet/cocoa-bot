import nasdaqdatalink
import os

API_KEY = os.getenv("NASDAQ_API_KEY")

nasdaqdatalink.ApiConfig.api_key = API_KEY


def get_cocoa_price():
    return float(3200)
    # try:
        # ICE Cocoa Futures (front month)
        # data = nasdaqdatalink.get("ICE/CC1")

        # Get latest close price
        latest = 3200
        # data["Settle"].iloc[-1]

        #return float(latest)

    #except Exception as e:
        #raise RuntimeError(f"Nasdaq cocoa fetch failed: {str(e)}")
