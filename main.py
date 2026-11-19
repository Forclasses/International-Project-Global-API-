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
    #kinda unecessary but I like to have error checking
    except Exception as e:
        print(f"Error saving JSON to {path}: {e}")

#temp main
def main():
    # get string from url
    url= "https://api.open-meteo.com/v1/forecast?latitude=50.0826&longitude=8.2493&hourly=temperature_2m,precipitation_probability,wind_speed_10m&timezone=Europe%2FBerlin&forecast_days=1"
    response = requests.get(url)
    data = json.loads(response.text)
    #print(data)
    #formate
    print(json.dumps(data, indent=4))
    save_json("ForUser.txt", data)

#main guard
if __name__ == "__main__":
    main();
    print("temphold")
