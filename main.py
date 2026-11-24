#starter code for project
#add your needed import files


#Functions for this file
#main() – Starts the application. Returns None
#handle_user_input() – Processes user selections.
#Returns: User_input (Dict)
#display_results(data) – Shows the final weather information and recommendations in the terminal while formatting it for the JSON.
#Returns: data (Dict)
#save_json(path, data) – Writes a JSON file to save data and show it to the user. Returns: None

#test function also needed

import requests
import os
import json
import time
from weather_api import (
    search_location,
    get_coordinates,
    get_weather,
    process_weather_data
)
from weather_display import display_forecast
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
    print(f"Current Temp: {summary['temperature']}°{unit}")
    print(f"Precipitation Prob: {summary['precipitation_probability']}%")
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
        print(json.dumps(data, indent=2))
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

        #Weather Display Module (Chris)
        weather_data["selected_unit"] = unit
        hourly_report = display_forecast(weather_data)

        # Pull first hour values for summary and recommendations
        first_raw = weather_data["forecast"][0]
        first_formatted = hourly_report["hourly_forecast"][0]

        temp_c = first_raw["temperature_2m"]
        rain = first_raw["precipitation_probability"]
        wind = first_raw["wind_speed_10m"]

        #Recommendation Module (Arif)
        activities = recommend_activity(temp_c, rain, wind)
        clothing = recommend_clothing(temp_c, rain, wind)

        #Combine, display, and save to JSON
        final_data = {
            "city": matched_city,
            "latitude": weather_data["latitude"],
            "longitude": weather_data["longitude"],
            "timezone": weather_data["timezone"],
            "unit": unit,
            "current_summary": {
                "time": first_formatted["time"],
                "temperature": first_formatted["temperature"],
                "precipitation_probability": rain,
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

#main guard
if __name__ == "__main__":
    main()
    print("temphold")

