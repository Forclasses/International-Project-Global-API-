# starter code for project
# add your needed import files

# Functions for this file
# main() - Starts the application. Returns None
# handle_user_input() - Processes user selections.
# Returns: User_input (Dict)
# search_location(city) - Searches for a city nearby.
# Returns: City (str, or None)
# get_coordinates(city) - Returns latitude and longitude.
# Returns: Lat_long (dict) or None if Error
# get_weather(latitude, longitude) - Requests weather data from Open-Meteo API.
# Returns: Raw_data (dict) or None if Error
# process_weather_data(data, city=None) - Extracts required weather info from JSON response.
# Returns: Weather_data (dict) or None if Error
# display_results(data) - Shows the final weather information and recommendations in the terminal while formatting it for the JSON.
# Returns: data (Dict)
# save_json(path, data) - Writes a JSON file to save data and show it to the user. Returns: None

import requests
import os
import json
import time


# ==================== Location Module ====================
def search_location(city):
    """
    Function: search_location(city) (by Alex)
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
    Function: get_coordinates(city) (by Alex)
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
    Function: get_weather(latitude, longitude) (by Alex)
    Does: Requests hourly weather data from the Open-Meteo API for given coordinates.
    Returns: Raw_data (dict) or None if Error
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation_probability,wind_speed_10m",
        "timezone": "Europe/Berlin",
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
    Function: process_weather_data(data, city=None) (by Alex)
    Does: Extracts the required information from the JSON response.
    Returns: Weather_data (dict) or None if Error
    """
    if not data or not isinstance(data, dict):
        print("Error: No valid weather data provided.")
        return None

    try:
        hourly = data["hourly"]
        times = hourly["time"]
        temperatures = hourly["temperature_2m"]
        precipitation = hourly["precipitation_probability"]
        wind_speeds = hourly["wind_speed_10m"]

        forecast_list = []
        for time_str, temp, precip, wind in zip(
            times, temperatures, precipitation, wind_speeds
        ):
            forecast_list.append({
                "time": time_str,
                "temperature_2m": temp,
                "precipitation_probability": precip,
                "wind_speed_10m": wind,
            })

        weather_data = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "city": city,
            "timezone": data.get("timezone"),
            "units": data.get("hourly_units", {}),
            "forecast": forecast_list,
        }
        return weather_data

    except (KeyError, TypeError) as e:
        print(f"Error processing weather data: {e}")
        return None
# ==================== Weather API Module ====================


# Starting function for later use
def save_json(path, data):
    """
    Function: save_json(path, data)
    Does: takes a file path, and the data, writes data to the file
    uses indent=2 when writing
    """
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    # kinda unnecessary but I like to have error checking
    except Exception as e:
        print(f"Error saving JSON to {path}: {e}")


# temp main
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
            print(f"\n--- Update at {time.strftime('%H:%M:%S')} ---")

            raw_data = get_weather(coords["latitude"], coords["longitude"])
            if raw_data is None:
                print("Weather data request failed. Next attempt in 10 minutes...")
            else:
                weather_data = process_weather_data(raw_data, matched_city)
                if weather_data is None:
                    print("Weather data processing failed.")
                else:
                    print(json.dumps(weather_data, indent=4))
                    save_json("ForUser.txt", weather_data)

            # Pause for 600 seconds = 10 minutes
            time.sleep(600)

    except KeyboardInterrupt:
        print("\nWeather polling stopped manually.")


# main guard
if __name__ == "__main__":
    main()