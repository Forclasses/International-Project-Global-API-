# By Christopher Bruce
#premlimary weather desplay
#display_forecast(data) – Displays hourly forecasts in the terminal and sends data to main.
# Returns: Hourly_report(dict)
#convert_temperature(value, unit) – 
# Converts Celsius into Fahrenheit or vice versa.
# Returns: Temp(Float)

def convert_temperature(value, unit):
    """
    Function: convert_temperature(value, unit)
    Does: Converts Celsius into Fahrenheit or vice versa.
    Returns: Temp (float)
    """
    target = unit.strip().upper()
    #simple math
    if target == "F":
        return round((float(value) * 9 / 5) + 32, 1)
    if target == "C":
        return round((float(value) - 32) * 5 / 9, 1)
    #if all else fails just return value
    return float(value)

def display_forecast(data):
    """
    Function: display_forecast(data)
    Does: Displays hourly forecasts in the terminal and formats data for main.
    Returns: Hourly_report (dict)
    """
    
    forecast_list = data.get("forecast", [])
    target_unit = data.get("selected_unit", "C").strip().upper()
    hourly_report = []
    #printing to temerinal for now
    print(f"\n--- Hourly Forecast for {data.get('city', 'Unknown')} (°{target_unit}) ---")
    print(f"{'Local Time':<18} | {'Temp':<8} | {'Precip':<8} | {'Wind (km/h)'}")
    print("-" * 55)
    #goes through list and stores the nessary arugments for the json
    for entry in forecast_list:
        temp = entry.get("temperature_2m")
        #coversion if nessary
        if target_unit == "F":
            temp = convert_temperature(temp, "F")
        #getting nessary stuff
        precip = entry.get("precipitation_probability")
        wind = entry.get("wind_speed_10m")
        raw_time = entry.get("time", "")

        record = {
            "time": raw_time,
            "temperature": temp,
            "unit": f"°{target_unit}",
            "precipitation_probability": precip,
            "wind_speed": wind
        } #making records
        hourly_report.append(record)

        clean_time = raw_time.replace("T", " ")
        print(f"{clean_time:<18} | {temp:>5}°{target_unit} | {precip:>6}% | {wind:>6}")

    return {"hourly_forecast": hourly_report}

#these two are pending testing
