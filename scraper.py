import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://www.investing.com/commodities/us-cocoa"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

# -----------------------------
# Fallback: last known price
# -----------------------------
def get_last_known_price():
    try:
        with open("storage.json", "r") as f:
            data = json.load(f)
        return data.get("last_price")
    except:
        return None


# -----------------------------
# Core scraper (Investing.com)
# -----------------------------
def fetch_from_investing():
    res = requests.get(URL, headers=HEADERS, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    # Primary selector (most common on Investing.com)
    price_element = soup.select_one("span[data-test='instrument-price-last']")

    # Fallback selector (they change UI often)
    if not price_element:
        price_element = soup.select_one(".text-2xl")

    if not price_element:
        raise ValueError("Cocoa price element not found on Investing.com page")

    price_text = price_element.text.strip().replace(",", "")
    return float(price_text)


# -----------------------------
# Retry wrapper
# -----------------------------
def fetch_with_retry(retries=3, delay=2):
    last_error = None

    for i in range(retries):
        try:
            return fetch_from_investing()
        except Exception as e:
            last_error = e
            time.sleep(delay)

    raise RuntimeError(f"Failed after retries: {last_error}")


# -----------------------------
# MAIN ENTRY FUNCTION
# -----------------------------
def get_cocoa_price():
    try:
        # 1. Try Investing.com
        return fetch_with_retry()

    except Exception as e:
        print(f"[WARN] Primary scrape failed: {e}")

        # 2. Fallback to stored value
        fallback = get_last_known_price()

        if fallback is not None:
            print("[INFO] Using last known price as fallback")
            return float(fallback)

        # 3. Hard fail-safe (prevents crashing pipeline)
        raise RuntimeError(
            "All cocoa price sources failed (scraper + fallback)"
        )
