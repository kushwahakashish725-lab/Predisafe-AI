import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

np.random.seed(42)

N = 3000

data = pd.DataFrame({

    "rainfall_mm":
        np.random.uniform(0, 300, N),

    "rainfall_intensity":
        np.random.uniform(0, 80, N),

    "soil_moisture":
        np.random.uniform(10, 100, N),

    "slope_angle":
        np.random.uniform(0, 60, N),

    "elevation_m":
        np.random.uniform(50, 3500, N),

    "temperature":
        np.random.uniform(5, 45, N),

    "humidity":
        np.random.uniform(30, 100, N),

    "ground_vibration":
        np.random.uniform(0, 10, N),

    "historical_landslide_count":
        np.random.randint(0, 10, N)
})


risk_score = (

    data["rainfall_mm"] * 0.22

    + data["rainfall_intensity"] * 0.18

    + data["soil_moisture"] * 0.16

    + data["slope_angle"] * 0.65

    + data["humidity"] * 0.04

    + data["ground_vibration"] * 2

    + data["historical_landslide_count"] * 2

    - data["elevation_m"] * 0.002

)

noise = np.random.normal(
    0,
    8,
    N
)

risk_score += noise

data["landslide_risk"] = pd.cut(

    risk_score,

    bins=[
        -np.inf,
        35,
        60,
        80,
        np.inf
    ],

    labels=[
        "LOW",
        "MODERATE",
        "HIGH",
        "CRITICAL"
    ]
)

os.makedirs(
    "data",
    exist_ok=True
)

data.to_csv(

    "data/demo_landslide_data.csv",

    index=False
)

print(
    "\n✅ Demo landslide dataset created."
)

features = [

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


X = data[features]

y = data["landslide_risk"]


X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)

model = RandomForestClassifier(

    n_estimators=250,

    max_depth=12,

    min_samples_split=5,

    random_state=42,

    class_weight="balanced"

)


print(
    "\n🧠 Training Landslide AI Model..."
)


model.fit(

    X_train,

    y_train

)


predictions = model.predict(
    X_test
)


accuracy = accuracy_score(

    y_test,

    predictions

)


print("\n==============================")

print(
    "LANDSLIDE MODEL RESULTS"
)

print("==============================")


print(
    f"\nAccuracy: {accuracy:.4f}"
)


print(
    "\nClassification Report:"
)


print(

    classification_report(

        y_test,

        predictions

    )

)

importance = pd.DataFrame({

    "feature":
        features,

    "importance":
        model.feature_importances_

})


importance = importance.sort_values(

    by="importance",

    ascending=False

)


print(
    "\nFeature Importance:"
)


print(
    importance.to_string(
        index=False
    )
)

os.makedirs(

    "models",

    exist_ok=True

)


model_path = (

    "models/"
    "landslide_model.pkl"

)


joblib.dump(

    model,

    model_path

)


print(
    "\n✅ Landslide model saved:"
)

print(
    model_path
)


joblib.dump(

    features,

    "models/"
    "landslide_features.pkl"

)


print(
    "\n✅ Feature list saved:"
)

print(
    "models/"
    "landslide_features.pkl"
)


print(
    "\n🎉 LANDSLIDE MODEL TRAINING COMPLETE!"
)