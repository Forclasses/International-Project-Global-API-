#taking Alex Rough draft
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
    Function: process_weather_data(data, city=None) 
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