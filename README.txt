CMIS 130 Section 092
SIUE

Contributors:
Christopher Edward Bruce

Alexander Felix Kirsten

Arif Emre Guezel

Name: WetterPlan
Explaination:
WetterPlan is a command-line weather planning prototype that fetches real-time hourly forecasts from the Open-Meteo API and provides 
temperature-unit conversion along with activity and clothing recommendations.

Make sure all four Python modules are in the same project directory:
- `main.py` – Entry point, user input validation, cooldown handling, JSON export, and built in `assert` tests.
- `weather_api.py` – Location search (Open-Meteo Geocoding API) and hourly forecast retrieval/parsing (Open-Meteo Forecast API).
- `weather_display.py` – Temperature conversion (`C`/`F`) and formatted hourly terminal table display.
- `recommendation.py` – Weather-based activity and clothing suggestions.
Note: Running the program will automatically generate `ForUser.json` in the same folder with your latest forecast and recommendations.


Setup:
1. Ensure Python 3.9 or higher is installed.
2. Open a terminal in the project folder and install the required packages:
   
   pip install requests tzdata
   
   (If `pip` is not recognized on Windows, run `python -m pip install requests tzdata`.)

How to Run:
Start the application from the project directory:

python main.py


Testing and Usage
- Built-in Tests: When `main.py` starts, it automatically runs 14 offline `assert` tests to verify temperature conversion, JSON parsing,
     formatting, recommendations, and file saving before prompting for input.
- City Input: Enter a city name—optionally with a state or country for disambiguation (e.g., `Springfield, IL`, `Paris, France`, or `Mainz`).
- Temperature Unit: Enter `C` for Celsius or `F` for Fahrenheit.
- Output: View the hourly forecast and recommendations in the terminal, or open `ForUser.json` to inspect the saved JSON output.

Other:
- No API Keys Required: Uses the free Open-Meteo API over HTTPS; no accounts, passwords, or API keys are needed or stored.
- Rate-Limit Cooldown: Searching more than 5 cities in a single session triggers a 10-second cooldown to prevent excessive API requests.