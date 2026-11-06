
#done by Christopher Bruce 11/6/2016
#getting jason test
import json
import requests
import os

# get string from url
url= "https://api.open-meteo.com/v1/forecast?latitude=50.0826&longitude=8.2493&hourly=temperature_2m,precipitation_probability,wind_speed_10m&timezone=Europe%2FBerlin&forecast_days=1"
response = requests.get(url)
data = json.loads(response.text)
#print(data)
#formate
print(json.dumps(data, indent=4))
#for key, value in data.items():
    
    #print(f"{key}: {value}")
#creat text file
with open("weather_data.txt", "w") as file:
    json.dump(data, file, indent=4)
    
