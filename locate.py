import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

IQAIR_API_KEY = "8dadfa53-8d0d-454a-b491-16990aceb29c"

def get_aqi(lat, lon):
    url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={IQAIR_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and "current" in data["data"] and "pollution" in data["data"]["current"]:
            aqi = data["data"]["current"]["pollution"]["aqius"]
            city = data["data"]["city"]
            state = data["data"]["state"]
            country = data["data"]["country"]
            return {"aqi": aqi, "city": city, "state": state, "country": country}
    return {"error": "Failed to fetch AQI data"}
