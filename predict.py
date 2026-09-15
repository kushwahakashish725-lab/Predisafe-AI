import os
import sys
import joblib
import pandas as pd

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "flood_model.pkl"
)

FEATURE_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "flood_features.pkl"
)



if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Flood model not found. Run train_flood_model.py first."
    )

model = joblib.load(MODEL_PATH)

features = joblib.load(FEATURE_PATH)

def calculate_risk_score(values):
    """
    Converts environmental conditions into a 0-100
    demonstration risk score.

    This is a development/demo risk engine.
    It is not an official flood warning formula.
    """

    rainfall = values["rainfall_mm"]
    intensity = values["rainfall_intensity"]
    river_level = values["river_level_m"]
    river_change = values["river_level_change"]
    soil = values["soil_moisture"]
    humidity = values["humidity"]
    elevation = values["elevation_m"]
    history = values["historical_flood_count"]

    score = 0

    if rainfall >= 200:
        score += 25
    elif rainfall >= 120:
        score += 18
    elif rainfall >= 60:
        score += 10
    else:
        score += 3

    if intensity >= 60:
        score += 20
    elif intensity >= 40:
        score += 14
    elif intensity >= 20:
        score += 8
    else:
        score += 2

    if river_level >= 12:
        score += 20
    elif river_level >= 8:
        score += 14
    elif river_level >= 5:
        score += 8
    else:
        score += 2

    if river_change >= 2:
        score += 15
    elif river_change >= 1:
        score += 10
    elif river_change >= 0.5:
        score += 5

    if soil >= 80:
        score += 8
    elif soil >= 60:
        score += 5
    elif soil >= 40:
        score += 2

    if humidity >= 85:
        score += 5
    elif humidity >= 70:
        score += 3

    if history >= 7:
        score += 5
    elif history >= 4:
        score += 3

    if elevation < 100:
        score += 5
    elif elevation < 300:
        score += 3

    score = max(0, min(100, score))

    return score


def get_risk_level(score):

    if score < 25:
        return "LOW"

    elif score < 50:
        return "MODERATE"

    elif score < 75:
        return "HIGH"

    else:
        return "CRITICAL"

def generate_explanation(values):

    reasons = []

    if values["rainfall_mm"] >= 120:
        reasons.append(
            "Heavy rainfall detected"
        )

    if values["rainfall_intensity"] >= 40:
        reasons.append(
            "High rainfall intensity"
        )

    if values["river_level_m"] >= 8:
        reasons.append(
            "River level is elevated"
        )

    if values["river_level_change"] >= 1:
        reasons.append(
            "River level is rising rapidly"
        )

    if values["soil_moisture"] >= 75:
        reasons.append(
            "Soil moisture is high"
        )

    if values["humidity"] >= 85:
        reasons.append(
            "High atmospheric humidity"
        )

    if values["historical_flood_count"] >= 5:
        reasons.append(
            "Area has previous flood history"
        )

    if values["elevation_m"] < 100:
        reasons.append(
            "Low-elevation area increases vulnerability"
        )

    if not reasons:
        reasons.append(
            "No major environmental risk signals detected"
        )

    return reasons

def predict_flood_risk(values):

    # Create dataframe in correct feature order
    input_data = pd.DataFrame(
        [[values[feature] for feature in features]],
        columns=features
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    probability_map = dict(
        zip(
            model.classes_,
            probabilities
        )
    )

    risk_score = calculate_risk_score(values)

    risk_level = get_risk_level(
        risk_score
    )

    reasons = generate_explanation(
        values
    )

    return {
        "disaster": "FLOOD",

        "ml_prediction": str(
            prediction
        ),

        "risk_score": risk_score,

        "risk_level": risk_level,

        "confidence": round(
            float(max(probabilities)) * 100,
            2
        ),

        "probabilities": {
            key: round(
                float(value) * 100,
                2
            )
            for key, value in probability_map.items()
        },

        "reasons": reasons
    }

if __name__ == "__main__":

    test_values = {

        "rainfall_mm": 180,

        "rainfall_intensity": 55,

        "river_level_m": 9,

        "river_level_change": 1.8,

        "soil_moisture": 82,

        "humidity": 90,

        "temperature": 25,

        "elevation_m": 120,

        "historical_flood_count": 6
    }

    result = predict_flood_risk(
        test_values
    )

    print("\n================================")
    print("       PREDISAFE AI")
    print("     FLOOD RISK ANALYSIS")
    print("================================")

    print(
        f"\nML Prediction: "
        f"{result['ml_prediction']}"
    )

    print(
        f"Risk Score: "
        f"{result['risk_score']}/100"
    )

    print(
        f"Risk Level: "
        f"{result['risk_level']}"
    )

    print(
        f"Model Confidence: "
        f"{result['confidence']}%"
    )

    print("\nWhy is the risk high?")

    for reason in result["reasons"]:
        print(f"  • {reason}")

    print("\n================================")