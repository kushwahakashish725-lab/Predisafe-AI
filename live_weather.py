import requests
from datetime import datetime


# =========================================================
# OPEN-METEO LIVE WEATHER
# No API key required
# =========================================================

def get_live_weather(latitude=27.7172, longitude=85.3240):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "showers,"
            "wind_speed_10m"
        ),
        "hourly": (
            "precipitation,"
            "rain,"
            "soil_moisture_0_to_1cm"
        ),
        "forecast_days": 1,
        "timezone": "auto"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        current = data.get("current", {})

        return {
            "success": True,
            "source": "Open-Meteo",
            "mode": "LIVE",

            "latitude": latitude,
            "longitude": longitude,

            "temperature": current.get(
                "temperature_2m"
            ),

            "humidity": current.get(
                "relative_humidity_2m"
            ),

            "precipitation": current.get(
                "precipitation"
            ),

            "rain": current.get(
                "rain"
            ),

            "showers": current.get(
                "showers"
            ),

            "wind_speed": current.get(
                "wind_speed_10m"
            ),

            "updated_at": datetime.now().isoformat()
        }

    except Exception as e:

        return {
            "success": False,
            "mode": "ERROR",
            "error": str(e)
        }


# =========================================================
# DEMO FALLBACK
# =========================================================

def get_demo_weather():

    return {

        "success": True,

        "source": "PrediSafe Demo Environment",

        "mode": "DEMO",

        "latitude": 27.7172,

        "longitude": 85.3240,

        "temperature": 24,

        "humidity": 78,

        "precipitation": 8,

        "rain": 6,

        "showers": 2,

        "wind_speed": 12,

        "updated_at": datetime.now().isoformat()
    }


# =========================================================
# LIVE + FALLBACK
# =========================================================

def get_weather(
    latitude=27.7172,
    longitude=85.3240
):

    live_data = get_live_weather(
        latitude,
        longitude
    )

    if live_data.get("success"):

        return live_data

    return get_demo_weather()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    weather = get_weather()

    print("\n================================")
    print("PrediSafe Weather Module")
    print("================================")

    print(
        "Mode:",
        weather.get("mode")
    )

    print(
        "Temperature:",
        weather.get("temperature")
    )

    print(
        "Humidity:",
        weather.get("humidity")
    )

    print(
        "Rain:",
        weather.get("rain")
    )

    print(
        "Wind:",
        weather.get("wind_speed")
    )

    print("================================")