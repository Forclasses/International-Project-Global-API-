# By Christopher Bruce
#premlimary weather desplay
#display_forecast(data) – Displays hourly forecasts in the terminal and sends data to main.
# Returns: Hourly_report(dict)
#convert_temperature(value, unit) – 
# Converts Celsius into Fahrenheit or vice versa.
# Returns: Temp(Float)

# Function: clean)_number
# helper function,
# dose strips letters and otehr characters input
# returns cleaned number
def clean_number(value):
    """
    Function: clean)_number
    helper function,
    does: strips letters and otehr characters from input
    returns cleaned number
    """
    
    if isinstance(value, (int, float)):
        return float(value)
    return float(str(value).split()[0])

def convert_temperature(value, unit):
    """
    Function: convert_temperature(value, unit)
    Does: Converts Celsius into Fahrenheit or vice versa.
    Returns: Temp (float)
    """
    clean_val = clean_number(value)
    target = unit.strip().upper()
    #simple math
    if target == "F":
        return round((clean_val * 9 / 5) + 32, 1)
    if target == "C":
        return round((clean_val - 32) * 5 / 9, 1)
    #if all else fails just return  clean value
    return clean_val

def display_forecast(data):
    """
    Function: display_forecast(data)
    Does: Displays hourly forecasts in the terminal and formats data for main.
    Returns: Hourly_report (dict)
    """
    
    forecast_list = data.get("forecast", [])
    target_unit = data.get("selected_unit", "C").strip().upper()
    
    #checking if output from api is producing fancy
    raw_temp_unit = data.get("units", {}).get("temperature_2m", "°C")
    if "F" in raw_temp_unit.upper():
        source_unit = "F"
    else:
        source_unit = "C"
    hourly_report = []
    #printing to temerinal for now
    print(f"\n--- Hourly Forecast for {data.get('city', 'Unknown')} (°{target_unit}) ---")
    print(
        f"{'Local Time':<17} | {'Temp':<7} | {'Prob':<5} | {'Wind':<10} | "
        f"{'Precip':<8} | {'Rain':<8} | {'Showers':<8} | {'Snow':<8}"
    )
    print("-" * 88)
    #goes through list and stores the nessary arugments for the json
    for entry in forecast_list:
        temp_num = clean_number(entry.get("temperature_2m", 0))
        #coversion if nessary
        if target_unit != source_unit:
            temp_num = convert_temperature(temp_num, target_unit)
        #getting nessary stuff
        precip_num = int(clean_number(entry.get("precipitation_probability", 0)))
        wind_num = clean_number(entry.get("wind_speed_10m", 0))
        
        precip_str = entry.get("precipitation", "0.0 mm")
        rain_str = entry.get("rain", "0.0 mm")
        showers_str = entry.get("showers", "0.0 mm")
        snow_str = entry.get("snowfall", "0.0 cm")
        
        raw_time = entry.get("time", "")

        record = {
            "time": raw_time,
            "temperature": temp_num,
            "unit": f"°{target_unit}",
            "precipitation_probability": precip_num,
            "wind_speed": wind_num,
            "precipitation": precip_str,
            "rain": rain_str,
            "showers": showers_str,
            "snowfall": snow_str
        } #making records
        hourly_report.append(record)

        clean_time = raw_time.replace("T", " ")
        wind_display = f"{wind_num} km/h"
        print(
            f"{clean_time:<16} | {temp_num:>5}°{target_unit} | {precip_num:>4}% | {wind_display:<10} | "
            f"{precip_str:<7} | {rain_str:<7} | {showers_str:<7} | {snow_str}"
        )

    return {"hourly_forecast": hourly_report}

#these two are pending testing
