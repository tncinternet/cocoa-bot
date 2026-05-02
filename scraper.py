import requests
from bs4 import BeautifulSoup

def get_cocoa_price():
    url = "https://www.tradingview.com/symbols/ICEUS-CC1!/"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    price_element = soup.find("div", class_="tv-symbol-price-quote__value")
    if price_element is None:
        raise RuntimeError("Could not find the cocoa price element on TradingView page")

    price_text = price_element.get_text(strip=True).replace(",", "")
    try:
        return float(price_text)
    except ValueError as exc:
        raise ValueError(f"Unable to parse cocoa price from '{price_text}'") from exc