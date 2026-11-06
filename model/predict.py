import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from model.config import MODEL_FILE


def load_predictor():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "Model not found. Train it first with: python -m model.train"
        )

    return joblib.load(MODEL_FILE)


def predict_weather(weather_data):
    """
    Predict the configured target from a dictionary.

    Example:
        {
            "humidity": 72,
            "pressure": 1008,
            "wind_speed": 14,
            "wind_direction": 180,
            "rainfall": 3.2,
            "cloud_cover": 65
        }
    """
    artifact = load_predictor()

    features = artifact["features"]
    model = artifact["model"]
    imputer = artifact["imputer"]
    scaler = artifact["scaler"]

    row = pd.DataFrame([weather_data])

    missing = [feature for feature in features if feature not in row.columns]
    if missing:
        raise ValueError(f"Missing prediction features: {missing}")

    row = row[features]

    for col in features:
        row[col] = pd.to_numeric(row[col], errors="coerce")

    row = imputer.transform(row)
    row = scaler.transform(row)

    prediction = model.predict(row)[0]

    return {
        "target": artifact["target"],
        "prediction": float(prediction),
    }


if __name__ == "__main__":
    sample = {
        "humidity": 72,
        "pressure": 1008,
        "wind_speed": 14,
        "wind_direction": 180,
        "rainfall": 3.2,
        "cloud_cover": 65,
    }

    print(predict_weather(sample))
