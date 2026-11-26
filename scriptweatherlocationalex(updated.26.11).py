import requests
import os
import json
import time


# ==================== Location Module ====================
def search_location(city):
    """
    Function: search_location(city) 
    Does: Searches for a matching city via the Open-Meteo Geocoding API.
    Returns: City (str, or None)
    """
    if not city or not isinstance(city, str) or not city.strip():
        print("Error: Invalid city name provided.")
        return None

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city.strip(),
        "count": 1,
        "language": "de",
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results")
        if not results:
            print(f"No matching city found for '{city}'.")
            return None

        matched_city = results[0].get("name")
        return str(matched_city) if matched_city else None

    except requests.exceptions.RequestException as e:
        print(f"Error searching location: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding location JSON response: {e}")
        return None


def get_coordinates(city):
    """
    Function: get_coordinates(city) 
    Does: Fetches latitude and longitude for a given city name.
    Returns: Lat_long (dict) or None if Error
    """
    if not city or not isinstance(city, str) or not city.strip():
        print("Error: Invalid city name provided.")
        return None

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city.strip(),
        "count": 1,
        "language": "de",
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results")
        if not results:
            print(f"No coordinates found for '{city}'.")
            return None

        first_match = results[0]
        latitude = first_match.get("latitude")
        longitude = first_match.get("longitude")

        if latitude is None or longitude is None:
            return None

        lat_long = {
            "latitude": latitude,
            "longitude": longitude,
        }
        return lat_long

    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding coordinates JSON response: {e}")
        return None
# ==================== Location Module ====================


# ==================== Weather API Module ====================
def get_weather(latitude, longitude):
    """
    Function: get_weather(latitude, longitude) 
    Does: Requests hourly weather data from the Open-Meteo API for given coordinates.
    Returns: Raw_data (dict) or None if Error
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation_probability,precipitation,rain,showers,snowfall,wind_speed_10m",
        "timezone": "auto",
        "forecast_days": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
        return raw_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data from API: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding JSON response: {e}")
        return None


def process_weather_data(data, city=None):
    """
    Function: process_weather_data(data, city=None) 
    Does: Extracts the required information from the JSON response.
    Returns: Weather_data (dict) or None if Error
    """
    if not data or not isinstance(data, dict):
        print("Error: No valid weather data provided.")
        return None

    try:
        hourly = data["hourly"]
        units = dict(data.get("hourly_units", {}))
        timezone_str = data.get("timezone", "")
        is_america = timezone_str.startswith("America/")

        if is_america:
            units["temperature_2m"] = "°F"

        times = hourly["time"]
        temperatures = hourly["temperature_2m"]
        precipitation_probs = hourly["precipitation_probability"]
        precipitations = hourly["precipitation"]
        rains = hourly["rain"]
        showers = hourly["showers"]
        snowfalls = hourly["snowfall"]
        wind_speeds = hourly["wind_speed_10m"]

        forecast_list = []
        for (
            time_str,
            temp,
            precip_prob,
            precip,
            rain,
            shower,
            snow,
            wind,
        ) in zip(
            times,
            temperatures,
            precipitation_probs,
            precipitations,
            rains,
            showers,
            snowfalls,
            wind_speeds,
        ):
            if is_america and temp is not None:
                temp_value = round((temp * 9 / 5) + 32, 1)
            else:
                temp_value = temp

            forecast_list.append({
                "time": time_str,
                "temperature_2m": f"{temp_value} {units.get('temperature_2m', '')}".strip(),
                "precipitation_probability": f"{precip_prob} {units.get('precipitation_probability', '')}".strip(),
                "precipitation": f"{precip} {units.get('precipitation', '')}".strip(),
                "rain": f"{rain} {units.get('rain', '')}".strip(),
                "showers": f"{shower} {units.get('showers', '')}".strip(),
                "snowfall": f"{snow} {units.get('snowfall', '')}".strip(),
                "wind_speed_10m": f"{wind} {units.get('wind_speed_10m', '')}".strip(),
            })

        weather_data = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "city": city,
            "timezone": timezone_str,
            "units": units,
            "forecast": forecast_list,
        }
        return weather_data

    except (KeyError, TypeError) as e:
        print(f"Error processing weather data: {e}")
        return None
# ==================== Weather API Module ====================


def save_json(path, data):
    """
    Function: save_json(path, data)
    Does: takes a file path, and the data, writes data to the file
    uses indent=2 when writing
    """
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving JSON to {path}: {e}")


def main():
    user_city = "Mainz"

    matched_city = search_location(user_city)
    if matched_city is None:
        print("Location search failed.")
        return

    coords = get_coordinates(matched_city)
    if coords is None:
        print("Coordinate lookup failed.")
        return

    print(f"Starting 10-minute polling for {matched_city} (Press Ctrl + C to stop)...")

    try:
        while True:
            print(f"\n--- Update at {time.strftime('%H:%M:%S %Z')} ---")

            raw_data = get_weather(coords["latitude"], coords["longitude"])
            if raw_data is None:
                print("Weather data request failed. Next attempt in 10 minutes...")
            else:
                weather_data = process_weather_data(raw_data, matched_city)
                if weather_data is None:
                    print("Weather data processing failed.")
                else:
                    print(json.dumps(weather_data, indent=4, ensure_ascii=False))
                    save_json("ForUser.txt", weather_data)

            # Pause for 600 seconds = 10 minutes
            time.sleep(600)

    except KeyboardInterrupt:
        print("\nWeather polling stopped manually.")


if __name__ == "__main__":
    main()