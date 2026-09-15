from flask import Flask, render_template, request, jsonify
from ml.multi_predict import predict_disaster
from ml.risk_engine import analyze_risk
from ml.alert_engine import analyze_alert
from ml.live_weather import get_weather
import requests
import math
from datetime import datetime

app = Flask(__name__)

risk_history = {"FLOOD": [], "LANDSLIDE": []}

EMERGENCY_SERVICES = [
    {"name": "National Emergency", "type": "Emergency Response", "number": "112"},
    {"name": "Police", "type": "Law Enforcement", "number": "100"},
    {"name": "Fire & Rescue", "type": "Fire & Rescue", "number": "101"},
    {"name": "Ambulance", "type": "Medical Emergency", "number": "108"}
]

SCENARIOS = {
    "FLOOD": {
        "normal": [20, 5, 2, 0.1, 35, 55, 25, 500, 1],
        "moderate": [130, 45, 7, 1.1, 70, 82, 24, 180, 4],
        "critical": [260, 75, 13, 2.5, 92, 96, 23, 60, 8]
    },
    "LANDSLIDE": {
        "normal": [20, 5, 35, 12, 500, 25, 55, 0.1, 0],
        "moderate": [110, 35, 68, 30, 1100, 22, 80, 0.7, 2],
        "critical": [220, 70, 90, 45, 1800, 19, 94, 5, 6]
    }
}

def process_prediction(disaster, data):
    prediction = predict_disaster(disaster, data)

    score = float(prediction.get("risk_score", 0))

    try:
        confidence = float(prediction.get("confidence", 0))
        if not math.isfinite(confidence):
            confidence = 0
    except:
        confidence = 0

    if confidence <= 1:
        confidence *= 100

    if confidence == 0:
        try:
            confidence = max(
                float(v) for v in prediction.get("probabilities", {}).values()
            ) * 100
        except:
            confidence = 85

    prediction["confidence"] = round(confidence, 1)

    history = risk_history[disaster]
    history.append(score)

    if len(history) > 10:
        history.pop(0)

    analysis = analyze_risk(score, history)

    try:
        alert = analyze_alert(score, analysis["trend"], disaster)
    except:
        alert = {}

    if not isinstance(alert, dict):
        alert = {}

    if score >= 75:
        stage = "EMERGENCY"
    elif score >= 50:
        stage = "WARNING"
    elif score >= 25:
        stage = "MONITOR"
    else:
        stage = "NORMAL"

    alert["stage"] = alert.get("stage") or stage

    return {
        "success": True,
        "disaster": disaster,
        "prediction": prediction,
        "analysis": analysis,
        "alert": alert,
        "environment": data,
        "history": history,
        "timestamp": datetime.now().isoformat()
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/simulate", methods=["POST"])
def simulate():
    body = request.get_json() or {}

    disaster = body.get("disaster", "FLOOD").upper()
    scenario = body.get("scenario", "normal").lower()

    if disaster not in SCENARIOS or scenario not in SCENARIOS[disaster]:
        return jsonify({"success": False}), 400

    if disaster == "FLOOD":
        keys = [
            "rainfall_mm",
            "rainfall_intensity",
            "river_level_m",
            "river_level_change",
            "soil_moisture",
            "humidity",
            "temperature",
            "elevation_m",
            "historical_flood_count"
        ]
    else:
        keys = [
            "rainfall_mm",
            "rainfall_intensity",
            "soil_moisture",
            "slope_angle",
            "elevation_m",
            "temperature",
            "humidity",
            "ground_vibration",
            "historical_landslide_count"
        ]

    data = dict(zip(keys, SCENARIOS[disaster][scenario]))

    return jsonify(process_prediction(disaster, data))

@app.route("/api/live-weather")
def live_weather():
    try:
        lat = float(request.args.get("lat", 27.7172))
        lng = float(request.args.get("lng", 85.3240))
        return jsonify(get_weather(lat, lng))
    except:
        return jsonify(get_weather())

@app.route("/api/live-predict", methods=["POST"])
def live_predict():
    body = request.get_json() or {}

    disaster = body.get("disaster", "FLOOD").upper()
    lat = float(body.get("lat") or 27.7172)
    lng = float(body.get("lng") or 85.3240)

    weather = get_weather(lat, lng)

    rain = weather.get("rain") or 0
    humidity = weather.get("humidity") or 60
    temperature = weather.get("temperature") or 25

    if disaster == "FLOOD":
        data = {
            "rainfall_mm": rain * 6,
            "rainfall_intensity": rain * 3,
            "river_level_m": 3 + rain * 0.15,
            "river_level_change": rain * 0.03,
            "soil_moisture": min(95, humidity * 0.8),
            "humidity": humidity,
            "temperature": temperature,
            "elevation_m": 300,
            "historical_flood_count": 2
        }
    else:
        data = {
            "rainfall_mm": rain * 6,
            "rainfall_intensity": rain * 3,
            "soil_moisture": min(95, humidity * 0.8),
            "slope_angle": 30,
            "elevation_m": 1000,
            "temperature": temperature,
            "humidity": humidity,
            "ground_vibration": 0.3,
            "historical_landslide_count": 2
        }

    result = process_prediction(disaster, data)
    result["live_weather"] = weather
    result["location"] = {"lat": lat, "lng": lng}

    return jsonify(result)

@app.route("/api/nearby")
def nearby():
    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))

        places = []

        query = f"""
        [out:json][timeout:20];
        (
          nwr(around:10000,{lat},{lng})["amenity"~"hospital|clinic|shelter"];
          nwr(around:10000,{lat},{lng})["healthcare"~"hospital|clinic"];
        );
        out center tags;
        """

        servers = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter"
        ]

        for server in servers:
            try:
                r = requests.post(
                    server,
                    data={"data": query},
                    headers={"User-Agent": "PrediSafe-AI"},
                    timeout=20
                )

                if r.ok:
                    for x in r.json().get("elements", []):
                        tags = x.get("tags", {})
                        name = tags.get("name")

                        if not name:
                            continue

                        if "lat" in x:
                            plat, plng = x["lat"], x["lon"]
                        elif "center" in x:
                            plat, plng = x["center"]["lat"], x["center"]["lon"]
                        else:
                            continue

                        places.append({
                            "name": name,
                            "type": tags.get(
                                "amenity",
                                tags.get("healthcare", "Support Location")
                            ).replace("_", " ").title(),
                            "lat": plat,
                            "lng": plng,
                            "distance": round(
                                haversine(lat, lng, plat, plng), 2
                            )
                        })

                    if places:
                        break

            except:
                continue

        if not places:
            for search in ["hospital", "clinic", "shelter"]:
                try:
                    r = requests.get(
                        "https://nominatim.openstreetmap.org/search",
                        params={
                            "q": search,
                            "format": "json",
                            "limit": 6,
                            "lat": lat,
                            "lon": lng,
                            "zoom": 12
                        },
                        headers={"User-Agent": "PrediSafe-AI/1.0"},
                        timeout=15
                    )

                    if r.ok:
                        for x in r.json():
                            plat = float(x["lat"])
                            plng = float(x["lon"])

                            places.append({
                                "name": x["display_name"].split(",")[0],
                                "type": search.title(),
                                "lat": plat,
                                "lng": plng,
                                "distance": round(
                                    haversine(lat, lng, plat, plng), 2
                                )
                            })
                except:
                    continue

        unique = {}
        for x in places:
            unique[x["name"]] = x

        places = sorted(
            unique.values(),
            key=lambda x: x["distance"]
        )[:4]

        return jsonify({
            "success": True,
            "safe_places": places,
            "emergency_services": EMERGENCY_SERVICES
        })

    except Exception as e:
        print("Nearby error:", e)

        return jsonify({
            "success": False,
            "safe_places": [],
            "emergency_services": EMERGENCY_SERVICES
        })

@app.route("/api/history")
def history():
    disaster = request.args.get("disaster", "FLOOD").upper()

    return jsonify({
        "history": risk_history.get(disaster, [])
    })

@app.route("/api/reset", methods=["POST"])
def reset():
    risk_history["FLOOD"] = []
    risk_history["LANDSLIDE"] = []

    return jsonify({"success": True})

def haversine(lat1, lon1, lat2, lon2):
    r = 6371

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2 +
        math.cos(p1) *
        math.cos(p2) *
        math.sin(dl / 2) ** 2
    )

    return 2 * r * math.asin(math.sqrt(a))

if __name__ == "__main__":
    print("PrediSafe AI running at http://127.0.0.1:5000")
    app.run(debug=True)