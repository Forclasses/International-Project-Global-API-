# Group 1 Wetter Plan
# CMIS 130
# Christopher Bruce
# Arif Emre Güzel
# Alexander Felix Kirsten

#Functions for this file
#main() – Starts the application. Returns None
#handle_user_input() – Processes user selections.
#Returns: User_input (Dict)
#display_results(data) – Shows the final weather information and recommendations in the terminal while formatting it for the JSON.
#Returns: data (Dict)
#save_json(path, data) – Writes a JSON file to save data and show it to the user. Returns: None

#test function also needed
#got added

#This is by: Christopher Bruce
import io
import contextlib
import requests
import os
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
#taking functions
from weather_api import (
    search_location,
    get_coordinates,
    get_weather,
    process_weather_data
)
from weather_display import display_forecast, convert_temperature
from recommendation import recommend_activity, recommend_clothing


def handle_user_input():
    """
    Function: handle_user_input()
    Does: Prompts user for city and temperature unit, validates inputs, returns dict
    """
    while True:
        #this is a quick fix of minor issue, needed a second field so muitable cities with same name no break
        city = input("\nEnter city name (e.g., 'Paris, France' or 'Springfield, IL'): ").strip()
        if city and not city.isdigit():
            break
        print("Invalid input. Please enter a valid city name.")

    while True:
        unit = input("Select temperature unit (C or F): ").strip().upper()
        if unit in ("C", "F"):
            break
        print("Invalid choice. Please enter 'C' or 'F'.")

    return {"city": city, "unit": unit}

def display_results(data):
    """
    Function: display_results(data)
    Does: Shows final weather info and recommendations in terminal, returns formatted dict
    """
    summary = data["current_summary"]
    recs = data["recommendations"]
    unit = data["unit"]

    print("\n================ WetterPlan Summary ================")
    print(f"City: {data['city']} ({data['latitude']}, {data['longitude']})")
    print(f"Timezone: {data['timezone']}")
    print(f"Forecast Time: {summary['time'].replace('T', ' ')}")
    print(f"Temperature: {summary['temperature']}°{unit}")
    print(f"Precipitation Prob: {summary['precipitation_probability']}%")
    print(f"Total Precipitation: {summary['precipitation']}")
    print(f"Rain: {summary['rain']} | Showers: {summary['showers']} | Snowfall: {summary['snowfall']}")
    print(f"Wind Speed: {summary['wind_speed']} km/h")
    print(f"Recommended Activities: {', '.join(recs['activities'])}")
    print(f"Clothing Suggestion: {recs['clothing']}")
    print("====================================================")
    return data



#Starting function for later use
def save_json(path, data):
    '''
    Function: save_json(path, data)
    Does: takes a file path, and the data, writes data to the file
    uses indent=2 when writing
    '''
    try:
        with open(path, "w",  encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        print(f"\nResults saved to {path}:")
        #print(json.dumps(data, indent=2))
    #kinda unecessary but I like to have error checking
    except Exception as e:
        print(f"Error saving JSON to {path}: {e}")

#temp main
def main():
    """
    Function: main()
    Does: Controls overall program flow, cooldowns, and module integration
    """
    request_count = 0
    max_requests = 5

    while True:
        #a cool down for to prevent overuse
        if request_count >= max_requests:
            print("\nExcessive requests detected. Cooling down for 10 seconds...")
            time.sleep(10)
            request_count = 0
        print("\n================ WetterPlan ================")
        #getting user data
        user_input = handle_user_input()
        city = user_input["city"]
        unit = user_input["unit"]
        #counting requests
        request_count += 1

        #Location Module (Alex)
        matched_city = search_location(city)
        if matched_city is None:
            print("Location search failed. Please try another city.")
            continue

        coords = get_coordinates(city)
        if coords is None:
            print("Coordinate lookup failed. Please try again.")
            continue

        #Weather API Module (Alex)
        raw_data = get_weather(coords["latitude"], coords["longitude"])
        if raw_data is None:
            print("Weather service unavailable. Please try again later.")
            continue

        weather_data = process_weather_data(raw_data, matched_city)
        if weather_data is None or not weather_data.get("forecast"):
            print("Weather data processing failed.")
            continue
        
        #getting weather for forcaste starting at time of want
        try:
            local_now = datetime.now(ZoneInfo(weather_data["timezone"]))
            current_hour_str = local_now.strftime("%Y-%m-%dT%H:00")
            for i, entry in enumerate(weather_data["forecast"]):
                if entry.get("time") == current_hour_str:
                    start_idx = i
                    break
        except Exception:
            start_idx = 0
            
        weather_data["forecast"] = weather_data["forecast"][start_idx:]

        #Weather Display Module (Chris)
        weather_data["selected_unit"] = unit
        hourly_report = display_forecast(weather_data)

        # Pull first hour values for summary and recommendations
        current_hour = hourly_report["hourly_forecast"][0]
        rain_prob = current_hour["precipitation_probability"]
        wind = current_hour["wind_speed"]
        
        #making sure that F does not mess up Arifs stuff
        if unit == "F":
            temp_c = convert_temperature(current_hour["temperature"], "C")
        else:
            temp_c = current_hour["temperature"]

        #Recommendation Module (Arif)
        activities = recommend_activity(temp_c, rain_prob, wind)
        clothing = recommend_clothing(temp_c, rain_prob, wind)

        #Combine, display, and save to JSON
        final_data = {
            "city": matched_city,
            "latitude": weather_data["latitude"],
            "longitude": weather_data["longitude"],
            "timezone": weather_data["timezone"],
            "unit": unit,
            "current_summary": {
                "time": current_hour["time"],
                "temperature": current_hour["temperature"],
                "precipitation_probability": rain_prob,
                "precipitation": current_hour["precipitation"],
                "rain": current_hour["rain"],
                "showers": current_hour["showers"],
                "snowfall": current_hour["snowfall"],
                "wind_speed": wind
            },
            "recommendations": {
                "activities": activities,
                "clothing": clothing
            },
            "hourly_forecast": hourly_report["hourly_forecast"]
        }

        formatted_data = display_results(final_data)
        save_json("ForUser.json", formatted_data)

        #Repeat or exit
        again = input("\nWould you like to search another city? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting WetterPlan.")
            break

#test function

def run_tests():
    """
    Function: run_tests()
    Does: Runs 14 offline assert tests silently without cluttering the terminal.
    Returns: None
    """
    #silence so things don't print
    # if not you would see an error due to me on purposely setting one off
    with contextlib.redirect_stdout(io.StringIO()):
        # testing Temperature conversion 
        #Assert function(num, Which one) == float if fail prints string
        assert convert_temperature(0, "F") == 32.0, "0°C should be 32.0°F"
        assert convert_temperature(100, "F") == 212.0, "100°C should be 212.0°F"
        assert convert_temperature(32, "C") == 0.0, "32°F should be 0.0°C"
        assert convert_temperature("36.5 °F", "C") == 2.5, "Should parse unit string and convert to 2.5°C"

        # testing Weather API JSON processing tests
        sample_raw_api = {
            "latitude": 50.08,
            "longitude": 8.24,
            "timezone": "Europe/Berlin",
            "hourly_units": {
                "temperature_2m": "°C",
                "precipitation_probability": "%",
                "precipitation": "mm",
                "rain": "mm",
                "showers": "mm",
                "snowfall": "cm",
                "wind_speed_10m": "km/h"
            },
            "hourly": {
                "time": ["2026-11-27T12:00"],
                "temperature_2m": [10.0],
                "precipitation_probability": [0 + 0],
                "precipitation": [0.0],
                "rain": [0.0],
                "showers": [0.0],
                "snowfall": [0.0],
                "wind_speed_10m": [12.0]
            }
        }
        processed = process_weather_data(sample_raw_api, "Mainz")
        assert processed is not None and processed["city"] == "Mainz", "Should parse valid API dict"
        assert process_weather_data({"bad_key": 123}, "Mainz") is None, "Missing 'hourly' key should return None"

        # Testing Forecast formatting tests 
        processed["selected_unit"] = "F"
        report = display_forecast(processed)
        assert len(report["hourly_forecast"]) == 1, "Should contain 1 formatted hourly record"
        assert report["hourly_forecast"][-1]["temperature"] == 50.0, "10.0°C should format as 50.0°F"

        # Testing Recommendation logic tests
        assert "Visit a museum" in recommend_activity(-5, 0, 10), "Freezing temp should suggest indoor museum"
        assert "Go cycling" not in recommend_activity(22, 0, 35), "High wind (35 km/h) should filter out cycling"
        assert "umbrella" in recommend_clothing(12, 80, 10).lower(), "80% rain should suggest an umbrella"
        assert "sunscreen" in recommend_clothing(28, 0, 5).lower(), "28°C should suggest sunscreen and sunglasses"

        #Testing JSON file writing & verification tests
        test_file = "test_output.json"
        save_json(test_file, {"status": "ok", "temp": 50.0})
        assert os.path.exists(test_file), "JSON output file should exist on disk"
        with open(test_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded["status"] == "ok", "Saved JSON content should match input dictionary"
        os.remove(test_file)
    print ("All 14 assert tests passed!")

#main guard
if __name__ == "__main__":
    run_tests()
    main()

