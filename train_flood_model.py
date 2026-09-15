import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

np.random.seed(42)

N = 3000

data = pd.DataFrame({
    "rainfall_mm": np.random.uniform(0, 300, N),
    "rainfall_intensity": np.random.uniform(0, 80, N),
    "river_level_m": np.random.uniform(0, 15, N),
    "river_level_change": np.random.uniform(-1, 3, N),
    "soil_moisture": np.random.uniform(10, 100, N),
    "humidity": np.random.uniform(30, 100, N),
    "temperature": np.random.uniform(5, 45, N),
    "elevation_m": np.random.uniform(20, 3000, N),
    "historical_flood_count": np.random.randint(0, 10, N)
})

risk_score = (
    data["rainfall_mm"] * 0.25
    + data["rainfall_intensity"] * 0.20
    + data["river_level_m"] * 2.5
    + data["river_level_change"] * 8
    + data["soil_moisture"] * 0.12
    + data["humidity"] * 0.05
    + data["historical_flood_count"] * 2
    - data["elevation_m"] * 0.003
)
noise = np.random.normal(0, 8, N)
risk_score = risk_score + noise


data["flood_risk"] = pd.cut(
    risk_score,
    bins=[-np.inf, 35, 60, 80, np.inf],
    labels=[
        "LOW",
        "MODERATE",
        "HIGH",
        "CRITICAL"
    ]
)

os.makedirs("data", exist_ok=True)

data.to_csv(
    "data/demo_flood_data.csv",
    index=False
)

print("\n✅ Demo dataset created:")
print("data/demo_flood_data.csv")


features = [
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

X = data[features]
y = data["flood_risk"]


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

print("\n🧠 Training Flood Risk Model...")

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n==============================")
print("FLOOD MODEL RESULTS")
print("==============================")

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance.to_string(index=False))


os.makedirs("models", exist_ok=True)

model_path = "models/flood_model.pkl"

joblib.dump(
    model,
    model_path
)

print("\n✅ Flood model saved:")
print(model_path)


joblib.dump(
    features,
    "models/flood_features.pkl"
)

print("✅ Feature list saved:")
print("models/flood_features.pkl")

print("\n🎉 FLOOD MODEL TRAINING COMPLETE!")