import requests
import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "weather_cache.json"

LATITUDE = 52.2298
LONGITUDE = 21.0118

API_URL = "https://api.open-meteo.com/v1/forecast"


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file, indent=2)


def get_tomorrow():
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")


def get_date_from_user():
    date_input = input("Enter date (YYYY-MM-DD) or press Enter: ").strip()

    if not date_input:
        tomorrow = get_tomorrow()
        print(f"Using tomorrow: {tomorrow}")
        return tomorrow

    try:
        datetime.strptime(date_input, "%Y-%m-%d")
        return date_input
    except ValueError:
        print("Wrong format!")
        return None


def fetch_precipitation(date):
    url = (
        f"{API_URL}?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=precipitation_sum"
        f"&timezone=Europe/London"
        f"&start_date={date}&end_date={date}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("Error with API")
        return None

    data = response.json()

    try:
        precipitation = data["daily"]["precipitation_sum"][0]
        return precipitation
    except:
        return None


def display_result(date, precipitation):
    print(f"\nWeather on {date}:")

    if precipitation is None or precipitation < 0:
        print("I don't know")
    elif precipitation == 0.0:
        print("It will not rain")
    else:
        print(f"It will rain ({precipitation} mm)")


def main():
    date = get_date_from_user()

    if date is None:
        return

    cache = load_cache()

    if date in cache:
        print("(Using cached data)")
        precipitation = cache[date]
    else:
        print("Fetching from API...")
        precipitation = fetch_precipitation(date)
        cache[date] = precipitation
        save_cache(cache)

    display_result(date, precipitation)


if __name__ == "__main__":
    main()
