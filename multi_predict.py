import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# =========================
# LOAD MODELS
# =========================

flood_model = joblib.load(
    os.path.join(MODEL_DIR, "flood_model.pkl")
)

flood_features = joblib.load(
    os.path.join(MODEL_DIR, "flood_features.pkl")
)

landslide_model = joblib.load(
    os.path.join(MODEL_DIR, "landslide_model.pkl")
)

landslide_features = joblib.load(
    os.path.join(MODEL_DIR, "landslide_features.pkl")
)


# =========================
# FLOOD PREDICTION
# =========================

def predict_flood(data):

    values = {
        "rainfall_mm": data.get("rainfall_mm", 0),
        "rainfall_intensity": data.get("rainfall_intensity", 0),
        "river_level_m": data.get("river_level_m", 0),
        "river_level_change": data.get("river_level_change", 0),
        "soil_moisture": data.get("soil_moisture", 0),
        "humidity": data.get("humidity", 0),
        "temperature": data.get("temperature", 0),
        "elevation_m": data.get("elevation_m", 0),
        "historical_flood_count": data.get("historical_flood_count", 0)
    }

    df = pd.DataFrame([values])

    # Keep exact training feature order
    df = df[flood_features]

    prediction = flood_model.predict(df)[0]

    probabilities = flood_model.predict_proba(df)[0]

    classes = flood_model.classes_

    probability_dict = {
        str(cls): round(float(prob) * 100, 2)
        for cls, prob in zip(classes, probabilities)
    }

    # =========================
    # RISK SCORE
    # =========================

    score = 0

    score += min(values["rainfall_mm"] / 3, 25)
    score += min(values["rainfall_intensity"] / 3, 20)
    score += min(values["river_level_m"] * 3, 25)
    score += min(values["river_level_change"] * 8, 15)
    score += min(values["soil_moisture"] / 5, 10)
    score += min(values["historical_flood_count"] * 0.5, 5)

    score = max(0, min(100, round(score)))

    if score < 25:
        level = "LOW"
    elif score < 50:
        level = "MODERATE"
    elif score < 75:
        level = "HIGH"
    else:
        level = "CRITICAL"

    reasons = []

    if values["rainfall_mm"] > 100:
        reasons.append("High accumulated rainfall detected.")

    if values["rainfall_intensity"] > 35:
        reasons.append("Rainfall intensity is significantly elevated.")

    if values["river_level_m"] > 6:
        reasons.append("River level is approaching a dangerous range.")

    if values["river_level_change"] > 0.8:
        reasons.append("Rapid increase in river level detected.")

    if values["soil_moisture"] > 70:
        reasons.append("High soil saturation may increase flood risk.")

    if not reasons:
        reasons.append("Environmental indicators are currently within a relatively stable range.")

    return {
        "disaster": "FLOOD",
        "ml_prediction": str(prediction),
        "risk_score": score,
        "risk_level": level,
        "probabilities": probability_dict,
        "reasons": reasons
    }


# =========================
# LANDSLIDE PREDICTION
# =========================

def predict_landslide(data):

    values = {
        "rainfall_mm": data.get("rainfall_mm", 0),
        "rainfall_intensity": data.get("rainfall_intensity", 0),
        "soil_moisture": data.get("soil_moisture", 0),
        "slope_angle": data.get("slope_angle", 0),
        "elevation_m": data.get("elevation_m", 0),
        "temperature": data.get("temperature", 0),
        "humidity": data.get("humidity", 0),
        "ground_vibration": data.get("ground_vibration", 0),
        "historical_landslide_count": data.get(
            "historical_landslide_count", 0
        )
    }

    df = pd.DataFrame([values])

    # Keep exact training feature order
    df = df[landslide_features]

    prediction = landslide_model.predict(df)[0]

    probabilities = landslide_model.predict_proba(df)[0]

    classes = landslide_model.classes_

    probability_dict = {
        str(cls): round(float(prob) * 100, 2)
        for cls, prob in zip(classes, probabilities)
    }

    # =========================
    # RISK SCORE
    # =========================

    score = 0

    score += min(values["rainfall_mm"] / 3, 25)
    score += min(values["rainfall_intensity"] / 3, 15)
    score += min(values["soil_moisture"] / 4, 15)
    score += min(values["slope_angle"] / 2, 15)
    score += min(values["ground_vibration"] * 5, 10)
    score += min(values["historical_landslide_count"] * 1, 10)

    # High humidity adds a small contribution
    if values["humidity"] > 80:
        score += 5

    score = max(0, min(100, round(score)))

    if score < 25:
        level = "LOW"
    elif score < 50:
        level = "MODERATE"
    elif score < 75:
        level = "HIGH"
    else:
        level = "CRITICAL"

    reasons = []

    if values["rainfall_mm"] > 100:
        reasons.append(
            "High rainfall can increase slope instability."
        )

    if values["rainfall_intensity"] > 35:
        reasons.append(
            "High rainfall intensity may rapidly saturate the slope."
        )

    if values["soil_moisture"] > 70:
        reasons.append(
            "High soil moisture indicates increased ground saturation."
        )

    if values["slope_angle"] > 30:
        reasons.append(
            "Steep terrain increases potential landslide susceptibility."
        )

    if values["ground_vibration"] > 1:
        reasons.append(
            "Elevated ground vibration has been detected."
        )

    if not reasons:
        reasons.append(
            "Current landslide-related environmental indicators are relatively stable."
        )

    return {
        "disaster": "LANDSLIDE",
        "ml_prediction": str(prediction),
        "risk_score": score,
        "risk_level": level,
        "probabilities": probability_dict,
        "reasons": reasons
    }


def predict_disaster(disaster, data):

    disaster = disaster.upper().strip()

    if disaster == "FLOOD":
        return predict_flood(data)

    elif disaster == "LANDSLIDE":
        return predict_landslide(data)

    else:
        raise ValueError(
            "Unsupported disaster type. Use FLOOD or LANDSLIDE."
        )


if __name__ == "__main__":

    flood_demo = {
        "rainfall_mm": 180,
        "rainfall_intensity": 55,
        "river_level_m": 9,
        "river_level_change": 1.8,
        "soil_moisture": 82,
        "humidity": 90,
        "temperature": 24,
        "elevation_m": 120,
        "historical_flood_count": 5
    }

    landslide_demo = {
        "rainfall_mm": 160,
        "rainfall_intensity": 50,
        "soil_moisture": 85,
        "slope_angle": 42,
        "elevation_m": 1400,
        "temperature": 20,
        "humidity": 92,
        "ground_vibration": 1.8,
        "historical_landslide_count": 4
    }

    print("\n==============================")
    print("FLOOD PREDICTION")
    print("==============================")

    print(predict_disaster("FLOOD", flood_demo))

    print("\n==============================")
    print("LANDSLIDE PREDICTION")
    print("==============================")

    print(predict_disaster("LANDSLIDE", landslide_demo))